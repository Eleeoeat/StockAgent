#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
增强版应用 - 整合多维度估值模型和历史股息分位分析
"""

import streamlit as st
import akshare as ak
from openai import OpenAI  
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 1. 网页标题与基础配置
st.set_page_config(page_title="AI 价值投资分析助手", layout="wide")
st.title("📊 A股价值投资 AI 分析助手")

# 2. 侧边栏：配置 DeepSeek
st.sidebar.header("⚙️ 配置中心")

# 先尝试从 .env 文件读取，如果没有则从侧边栏输入
default_api_key = os.getenv("DEEPSEEK_API_KEY", "")
api_key = st.sidebar.text_input(
    "请输入 DeepSeek API Key",
    value=default_api_key,
    type="password"
)

# 模型选择
selected_model = st.sidebar.selectbox(
    "选择 AI 模型",
    ["deepseek-chat", "deepseek-reasoner"],
    index=0,
    help="💡 deepseek-chat (V3): 快速响应，适合快速分析\n🧠 deepseek-reasoner (R1): 深度推理，适合复杂决策"
)

base_url = "https://api.deepseek.com"

# ============================================================================
# 数据获取函数集
# ============================================================================

# 2.1 获取近一年最高/最低价
@st.cache_data(ttl=3600)
def get_52week_price_range(stock_code):
    """获取近一年（52周）的最高价和最低价"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        hist_df = ak.stock_zh_a_hist(symbol=stock_code, 
                                      start_date=start_date.strftime("%Y%m%d"),
                                      end_date=end_date.strftime("%Y%m%d"),
                                      adjust="")
        
        if hist_df is not None and not hist_df.empty:
            # 使用位置索引而不是列名，避免中文编码问题
            # 第3列是最高价（高），第4列是最低价（低）
            high_52w = hist_df.iloc[:, 2].max()
            low_52w = hist_df.iloc[:, 3].min()
            return {
                "high_52w": high_52w,
                "low_52w": low_52w,
                "range": high_52w - low_52w,
                "ratio": (high_52w - low_52w) / low_52w * 100 if low_52w > 0 else 0
            }
    except Exception as e:
        st.warning(f"⚠️ 获取近一年价格范围失败: {str(e)}")
    
    return {"high_52w": None, "low_52w": None, "range": None, "ratio": None}

# 2.2 获取最新股息数据
@st.cache_data(ttl=3600)
def get_dividend_data(stock_code):
    """获取最新的每股股息数据"""
    try:
        dividend_df = ak.stock_dividend_cninfo(symbol=stock_code)
        
        if dividend_df is not None and not dividend_df.empty:
            if '公告日期' in dividend_df.columns:
                dividend_df['公告日期'] = pd.to_datetime(dividend_df['公告日期'], errors='coerce')
                dividend_df = dividend_df.sort_values('公告日期', ascending=False)
            
            latest_dividend = dividend_df.iloc[0]
            
            result = {
                "dividend_per_share": None,
                "transfer_share": None,
                "payout_ratio": None,
                "record_date": None,
                "history": []
            }
            
            for col in dividend_df.columns:
                if '派息' in col or '每股' in col:
                    val = latest_dividend[col]
                    # 类型检查：只接受数字类型
                    if isinstance(val, (int, float)):
                        if '派息' in col and '转增' not in col:
                            result["dividend_per_share"] = val
                        if '转增' in col:
                            result["transfer_share"] = val
                    elif val is not None:
                        # 尝试转换为 float
                        try:
                            float_val = float(str(val).replace('元', '').strip())
                            if '派息' in col and '转增' not in col:
                                result["dividend_per_share"] = float_val
                            if '转增' in col:
                                result["transfer_share"] = float_val
                        except (ValueError, TypeError):
                            pass
                
                if '派息率' in col or '分配率' in col:
                    result["payout_ratio"] = latest_dividend[col]
                
                if '记录日' in col or '除权日' in col:
                    result["record_date"] = latest_dividend[col]
            
            # 提取历史派息数据用于分位分析（与财报数据保持10年）
            dividend_values = []
            for idx, row in dividend_df.iterrows():
                try:
                    for col in dividend_df.columns:
                        if '派息' in col and '转增' not in col:
                            val = row[col]
                            # 检查是否为数字类型
                            if isinstance(val, (int, float)) and not isinstance(val, bool):
                                if val > 0:  # 只记录有效派息
                                    dividend_values.append(float(val))
                                break
                            elif val is not None:
                                # 尝试转换
                                try:
                                    str_val = str(val).replace('元', '').strip()
                                    if str_val and str_val.replace('.', '', 1).isdigit():
                                        float_val = float(str_val)
                                        if float_val > 0:  # 只记录有效派息
                                            dividend_values.append(float_val)
                                        break
                                except (ValueError, TypeError):
                                    pass
                except:
                    pass
            
            # 保留10年历史数据（与财报数据一致）
            if len(dividend_values) >= 1:
                result["history"] = dividend_values[:10]  # 最多保留10年
                result["history_years"] = len(result["history"])  # 记录实际年数
                
            return result
    except Exception as e:
        st.warning(f"⚠️ 获取分红数据失败: {str(e)}")
    
    return {"dividend_per_share": None, "transfer_share": None, "payout_ratio": None, "history": []}

# 2.3 计算股息率
def calculate_dividend_yield(dividend_per_share, current_price):
    """计算股息率（年度分红 / 现价）"""
    # 类型检查和转换
    if dividend_per_share is None or current_price is None:
        return None
    
    try:
        div_value = float(dividend_per_share)
        price_value = float(current_price)
        
        if price_value > 0:
            return (div_value / price_value) * 100
    except (ValueError, TypeError):
        pass
    
    return None

# 2.4 股息率分位分析
def analyze_dividend_percentile(dividend_history, current_yield):
    """分析当前股息率在历史中的分位"""
    if not dividend_history or len(dividend_history) < 3 or current_yield is None:
        return None
    
    div_array = np.array(dividend_history)
    
    # 基于历史派息计算的平均股息率（需要当前价格，这里简化处理）
    return {
        "mean_dividend": float(np.mean(div_array)),
        "median_dividend": float(np.median(div_array)),
        "q25_dividend": float(np.percentile(div_array, 25)),
        "q75_dividend": float(np.percentile(div_array, 75)),
        "max_dividend": float(np.max(div_array)),
        "min_dividend": float(np.min(div_array)),
    }

# ============================================================================
# 估值模型函数集
# ============================================================================

def estimate_by_pe_model(current_pe, current_price):
    """PE 倍数估值（调整阈值适配A股市场）"""
    # A股市场PE阈值：参考历史数据和价值投资理念
    # 低估：<15（格雷厄姆标准）
    # 合理：15-25（巴菲特可接受范围）
    # 偏高：25-35（成长股可接受）
    # 高估：>35（需要高成长支撑）
    if current_pe < 15:
        assessment = "低估"
    elif current_pe < 25:
        assessment = "合理"
    elif current_pe < 35:
        assessment = "偏高"
    else:
        assessment = "高估"
    
    return {
        "model": "PE倍数法",
        "current_pe": current_pe,
        "assessment": assessment,
        "reference_range": "低估<15 | 合理15-25 | 偏高25-35 | 高估>35",
        "market_avg": 25,  # A股市场平均PE约25
        "premium": ((current_pe - 25) / 25 * 100) if current_pe > 0 else 0
    }

def estimate_by_pb_model(current_price, book_value_per_share=None):
    """PB 倍数估值"""
    if book_value_per_share is None or book_value_per_share <= 0:
        return None
    
    pb = current_price / book_value_per_share
    return {
        "model": "PB倍数法",
        "current_pb": pb,
        "assessment": "极低" if pb < 0.8 else "低" if pb < 1.2 else "中" if pb < 2 else "高",
    }

def estimate_by_roe_model(roe, eps, current_price):
    """ROE 倍数估值"""
    if not roe or roe <= 0 or not eps:
        return None
    
    reasonable_pe = 10 + (roe - 8) * 2
    reasonable_price = eps * reasonable_pe
    
    return {
        "model": "ROE倍数法",
        "roe": roe,
        "reasonable_pe": reasonable_pe,
        "reasonable_price": reasonable_price,
        "discount_or_premium": ((current_price - reasonable_price) / reasonable_price * 100)
    }

def estimate_by_peg_model(current_pe, growth_rate=None, finance_df=None):
    """PEG 估值（尝试从财务数据提取真实增长率）"""
    # 尝试从财务数据计算真实净利润增长率
    calculated_growth = None
    if finance_df is not None and not finance_df.empty:
        try:
            # 查找净利润相关列
            for col in finance_df.columns:
                if '净利润' in col and '增长率' in col:
                    # 获取最近的增长率数据
                    growth_val = finance_df.iloc[0][col]
                    if isinstance(growth_val, (int, float)):
                        calculated_growth = abs(float(growth_val))  # 取绝对值
                        break
                    elif growth_val is not None:
                        try:
                            # 去除%符号并转换
                            str_val = str(growth_val).replace('%', '').strip()
                            calculated_growth = abs(float(str_val))
                            break
                        except:
                            pass
        except:
            pass
    
    # 使用计算出的增长率，如果没有则使用传入的growth_rate，都没有则默认10%
    final_growth = calculated_growth if calculated_growth and calculated_growth > 0 else (growth_rate if growth_rate else 10)
    
    if current_pe <= 0 or final_growth <= 0:
        return None
    
    peg = current_pe / final_growth
    
    # PEG判断标准：<1优秀，1-1.5合理，1.5-2偏高，>2高估
    if peg < 1:
        assessment = "低估"
    elif peg < 1.5:
        assessment = "合理"
    elif peg < 2:
        assessment = "偏高"
    else:
        assessment = "高估"
    
    return {
        "model": "PEG模型",
        "peg": peg,
        "growth_rate": final_growth,
        "growth_source": "财报数据" if calculated_growth else "预估值",
        "assessment": assessment,
        "reference": "低估<1 | 合理1-1.5 | 偏高1.5-2 | 高估>2"
    }

# ============================================================================
# AI 分析函数
# ============================================================================

def call_deepseek_agent(api_key, stock_name, data_string, current_date, current_price, 
                        current_pe, current_change_pct, price_range_data, dividend_data, valuation_models, ai_model="deepseek-chat"):
    """调用 DeepSeek 进行 AI 分析"""
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # 构建估值信息（包含详细标准）
    valuation_info = "【多维度估值模型结论】\n"
    for model in valuation_models:
        if model:
            assessment = model['assessment']
            if model['model'] == "PE倍数法":
                valuation_info += f"- PE倍数法: {assessment} (当前PE={model['current_pe']:.2f}, 参考: {model['reference_range']})\n"
            elif model['model'] == "PEG模型":
                growth_source = model.get('growth_source', '预估值')
                valuation_info += f"- PEG模型: {assessment} (PEG={model['peg']:.2f}, 增长率={model['growth_rate']:.1f}% [{growth_source}], 参考: {model['reference']})\n"
            else:
                valuation_info += f"- {model['model']}: {assessment}\n"
    
    # 安全处理 None 值
    high_52w = price_range_data.get('high_52w') if price_range_data else None
    low_52w = price_range_data.get('low_52w') if price_range_data else None
    
    # 构建价格范围信息
    price_info = ""
    if high_52w is not None and low_52w is not None:
        price_info = f"近一年高：{high_52w:.2f} 元 | 低：{low_52w:.2f} 元"
    else:
        price_info = "近一年高：数据暂无 | 低：数据暂无"
    
    # 构建股息分位信息
    dividend_percentile_info = ""
    dividend_history = dividend_data.get("history") if dividend_data else None
    dividend_per_share = dividend_data.get("dividend_per_share") if dividend_data else None
    
    if dividend_history and len(dividend_history) >= 3:
        div_yield = calculate_dividend_yield(dividend_per_share, current_price)
        percentile_data = analyze_dividend_percentile(dividend_history, div_yield)
        
        if percentile_data:
            dividend_percentile_info = f"""
    【历史股息率分位分析】
    - 历史平均派息: {percentile_data['mean_dividend']:.2f} 元
    - 历史中位派息: {percentile_data['median_dividend']:.2f} 元
    - 历史最高派息: {percentile_data['max_dividend']:.2f} 元
    - 历史最低派息: {percentile_data['min_dividend']:.2f} 元
    """
    
    # 安全处理 PE 值
    pe_str = f"{current_pe:.2f}" if current_pe is not None else "数据暂无"
    change_str = f"{current_change_pct}%" if current_change_pct is not None else "数据暂无"
    
    prompt = f"""
    你是顶级对冲基金经理，今天是 {current_date}，标的：{stock_name}。
    现价：{current_price} 元 | PE：{pe_str} | 涨跌：{change_str}
    
    【关键数据】
    {price_info}
    当前派息：{dividend_per_share if dividend_per_share else 'N/A'} 元
    {dividend_percentile_info}
    {valuation_info}
    
    【估值标准说明】
    - PE估值: A股市场调整后标准 (低估<15 | 合理15-25 | 偏高25-35 | 高估>35)
    - PEG估值: 基于真实财报增长率或预估值 (低估<1 | 合理1-1.5 | 偏高1.5-2 | 高估>2)
    - 股息数据: 最多包含近10年历史数据（与财报周期一致），数据不足时会提示
    
    【财务数据】
    {data_string}
    
    【报告要求】
    1. 给出【核心量化指标清单】：ROE、毛利率、PE、PB、PEG、股息率等
    2. 给出【多维度估值对比】：综合分析 PE/PEG/股息率 等模型，解释估值结论合理性
    3. 给出【利弗莫尔趋势信号】：价格位置、高低点距离
    4. 给出【股息策略分析】：分红吸引力、历史分位（注意数据年限）
    5. 给出【风险与不买入理由】：至少 3 条
    6. 给出【投资建议】：买入/观望/卖出
    7. 用具体数字论证，严禁空泛形容词
    """
    
    response = client.chat.completions.create(
        model=ai_model,
        messages=[
            {"role": "system", "content": "你是硬核资深投研专家，数据驱动、逻辑严谨。"},
            {"role": "user", "content": prompt},
        ],
        stream=True
    )
    return response

# ============================================================================
# 主应用界面
# ============================================================================

user_input = st.text_input("请输入企业名称", value="贵州茅台")

if st.button("开始深度分析"):
    if not api_key:
        st.error("❌ 请先输入 DeepSeek API Key！")
    else:
        with st.status("正在执行多智能体协作分析...", expanded=True) as status:
            # 第一步：匹配股票
            st.write("🔍 正在检索股票代码...")
            stock_df = ak.stock_zh_a_spot_em()
            match = stock_df[stock_df['名称'].str.contains(user_input)]
            
            if not match.empty:
                target_code = match.iloc[0]['代码']
                target_name = match.iloc[0]['名称']
                current_price = match.iloc[0]['最新价']
                current_pe = match.iloc[0]['市盈率-动态']
                current_change_pct = match.iloc[0]['涨跌幅']
                current_date = datetime.now().strftime("%Y-%m-%d")
                
                status.update(label=f"已找到：{target_name} ({target_code})", state="running")
                
                # 第二步：获取财务数据
                st.write("📂 正在抓取财报数据...")
                finance_df = ak.stock_financial_abstract_ths(symbol=target_code, indicator="主要指标")
                date_col = finance_df.columns[0]
                finance_df = finance_df.sort_values(by=date_col, ascending=False)
                
                # 优化：减少数据量从20条到10条，且筛选关键指标
                finance_recent = finance_df.head(10)
                
                # 筛选关键指标列（如果存在）
                key_indicators = [date_col]  # 先加入日期列
                possible_indicators = [
                    'ROE', '净资产收益率', '净利润', '营业收入', '营业总收入',
                    '毛利率', '净利率', '资产负债率', '每股收益', 'EPS',
                    '净利润增长率', '营收增长率', '流动比率'
                ]
                
                for indicator in possible_indicators:
                    for col in finance_df.columns:
                        if indicator in col and col not in key_indicators:
                            key_indicators.append(col)
                            break
                
                # 如果有关键指标，只使用这些；否则使用全部
                if len(key_indicators) > 1:
                    finance_for_ai = finance_recent[key_indicators]
                else:
                    finance_for_ai = finance_recent
                
                core_data_for_ai = finance_for_ai.to_string()
                
                # 第三步：获取额外数据
                st.write("📊 正在获取价格和股息数据...")
                price_range_data = get_52week_price_range(target_code)
                dividend_data = get_dividend_data(target_code)
                
                # 第四步：计算估值模型
                st.write("🔢 正在计算多维度估值模型...")
                valuation_models = [
                    estimate_by_pe_model(current_pe, current_price),
                    estimate_by_peg_model(current_pe, growth_rate=None, finance_df=finance_recent),  # 传入财务数据
                ]
                
                # 显示数据面板
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.subheader("📈 利弗莫尔趋势")
                    if price_range_data.get("high_52w"):
                        st.metric("52周最高价", f"{price_range_data['high_52w']:.2f} 元")
                        st.metric("52周最低价", f"{price_range_data['low_52w']:.2f} 元")
                        st.metric("当前PE", f"{current_pe:.2f}x")
                
                with col2:
                    st.subheader("💰 股息率模型")
                    if dividend_data.get("dividend_per_share"):
                        div_yield = calculate_dividend_yield(dividend_data["dividend_per_share"], current_price)
                        st.metric("每股派息", f"{dividend_data['dividend_per_share']:.2f} 元")
                        if div_yield:
                            st.metric("当前股息率", f"{div_yield:.2f}%")
                        history_years = dividend_data.get("history_years", len(dividend_data.get("history", [])))
                        st.metric("历史数据", f"{history_years} 年" if history_years else "数据不足")
                    else:
                        st.info("⚠️ 暂无分红数据")
                
                with col3:
                    st.subheader("📊 估值对比")
                    for model in valuation_models:
                        if model:
                            st.metric(model['model'], model['assessment'])
                
                # 第五步：AI 分析
                st.write("🤖 正在调用 AI 进行深度分析...")
                st.subheader("💡 专家级价值评估报告")
                
                report_placeholder = st.empty()
                full_content = ""
                
                response_stream = call_deepseek_agent(
                    api_key=api_key,
                    stock_name=target_name,
                    data_string=core_data_for_ai,
                    current_date=current_date,
                    current_price=current_price,
                    current_pe=current_pe,
                    current_change_pct=current_change_pct,
                    price_range_data=price_range_data,
                    dividend_data=dividend_data,
                    valuation_models=valuation_models,
                    ai_model=selected_model
                )
                
                for chunk in response_stream:
                    if chunk.choices[0].delta.content:
                        full_content += chunk.choices[0].delta.content
                        report_placeholder.markdown(full_content + "▌")
                
                report_placeholder.markdown(full_content)
                status.update(label="✅ 分析完成！", state="complete")
            else:
                st.error("❌ 未找到匹配的股票")
        
        # 在 status 完成后显示财务数据（避免嵌套问题）
        if 'target_name' in locals() and 'finance_recent' in locals():
            st.subheader(f"{target_name} 财务摘要（最近10期）")
            st.dataframe(finance_recent)
            
            # 显示给AI的简化数据（可收起）
            with st.expander("🤖 查看 AI 分析用数据（已精简）"):
                st.dataframe(finance_for_ai)
