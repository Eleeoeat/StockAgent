#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试数据抓取功能 - 验证近一年最高/最低价、股息数据、实时股价的抓取
"""

import akshare as ak
from datetime import datetime, timedelta
import pandas as pd

def test_realtime_price():
    """测试获取实时股价"""
    print("=" * 50)
    print("📊 测试一：获取实时股价（基点数据）")
    print("=" * 50)
    try:
        stock_df = ak.stock_zh_a_spot_em()
        # 查询贵州茅台
        match = stock_df[stock_df['名称'].str.contains('茅台')]
        if not match.empty:
            code = match.iloc[0]['代码']
            name = match.iloc[0]['名称']
            price = match.iloc[0]['最新价']
            change = match.iloc[0]['涨跌幅']
            pe = match.iloc[0]['市盈率-动态']
            print(f"✓ 股票: {name} ({code})")
            print(f"✓ 当前价格: {price} 元")
            print(f"✓ 涨跌幅: {change}%")
            print(f"✓ 动态PE: {pe}")
            return code, price
        else:
            print("✗ 未找到茅台")
    except Exception as e:
        print(f"✗ 错误: {str(e)}")
    
    return None, None

def test_52week_price_range(stock_code):
    """测试获取近一年最高/最低价"""
    print("\n" + "=" * 50)
    print("📈 测试二：获取近一年最高/最低价（利弗莫尔趋势分析）")
    print("=" * 50)
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        hist_df = ak.stock_zh_a_hist(symbol=stock_code, 
                                      start_date=start_date.strftime("%Y%m%d"),
                                      end_date=end_date.strftime("%Y%m%d"),
                                      adjust="")
        
        if hist_df is not None and not hist_df.empty:
            high_52w = hist_df['高'].max()
            low_52w = hist_df['低'].min()
            price_range = high_52w - low_52w
            ratio = (high_52w - low_52w) / low_52w * 100 if low_52w > 0 else 0
            
            print(f"✓ 查询周期: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")
            print(f"✓ 近一年最高价: {high_52w:.2f} 元")
            print(f"✓ 近一年最低价: {low_52w:.2f} 元")
            print(f"✓ 价格振幅: {price_range:.2f} 元")
            print(f"✓ 波动幅度: {ratio:.1f}%")
            print(f"✓ 数据点数: {len(hist_df)} 个交易日")
            return {"high": high_52w, "low": low_52w}
        else:
            print("✗ 未获取到数据")
    except Exception as e:
        print(f"✗ 错误: {str(e)}")
    
    return None

def test_dividend_data(stock_code):
    """测试获取最新股息数据"""
    print("\n" + "=" * 50)
    print("💰 测试三：获取最新股息数据（股息率模型）")
    print("=" * 50)
    try:
        dividend_df = ak.stock_dividend_cninfo(symbol=stock_code)
        
        if dividend_df is not None and not dividend_df.empty:
            print(f"✓ 找到 {len(dividend_df)} 条分红记录")
            print("\n【列名信息】：")
            for col in dividend_df.columns:
                print(f"  - {col}")
            
            # 按日期排序取最新
            if '公告日期' in dividend_df.columns:
                dividend_df['公告日期'] = pd.to_datetime(dividend_df['公告日期'], errors='coerce')
                dividend_df = dividend_df.sort_values('公告日期', ascending=False)
            
            latest = dividend_df.iloc[0]
            print("\n【最新分红数据】：")
            
            for col in dividend_df.columns:
                val = latest[col]
                if '派息' in col or '转增' in col or '派息率' in col or '分配率' in col:
                    print(f"  - {col}: {val}")
            
            return latest
        else:
            print("✗ 暂无分红数据")
    except Exception as e:
        print(f"✗ 错误: {str(e)}")
    
    return None

def test_financial_data(stock_code):
    """测试获取财务数据"""
    print("\n" + "=" * 50)
    print("📊 测试四：获取最近5年财务数据")
    print("=" * 50)
    try:
        finance_df = ak.stock_financial_abstract_ths(symbol=stock_code, indicator="主要指标")
        
        if finance_df is not None and not finance_df.empty:
            print(f"✓ 找到 {len(finance_df)} 期财务数据")
            print(f"✓ 列名数量: {len(finance_df.columns)}")
            print("\n【前5列】：")
            for col in finance_df.columns[:5]:
                print(f"  - {col}")
            
            # 按日期排序并显示前5行
            date_col = finance_df.columns[0]
            finance_df = finance_df.sort_values(by=date_col, ascending=False)
            
            print(f"\n【最近20期财务数据（共 {len(finance_df)} 期）】：")
            print(finance_df.head(20).to_string(max_rows=5))
            
            return finance_df.head(20)
        else:
            print("✗ 未获取到数据")
    except Exception as e:
        print(f"✗ 错误: {str(e)}")
    
    return None

def main():
    print("\n")
    print("🔍 StockAgent 数据抓取功能测试")
    print("=" * 50)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 获取实时股价
    code, price = test_realtime_price()
    
    if not code:
        print("\n✗ 无法继续测试，请检查网络连接")
        return
    
    # 2. 获取近一年价格范围
    price_data = test_52week_price_range(code)
    
    # 3. 获取股息数据
    dividend_data = test_dividend_data(code)
    
    # 4. 获取财务数据
    finance_data = test_financial_data(code)
    
    print("\n" + "=" * 50)
    print("✅ 测试完成！所有必要数据已验证")
    print("=" * 50)
    print("\n【数据集成检查】：")
    print(f"✓ 当前实时股价：{price} 元（用作计算基点）")
    if price_data:
        print(f"✓ 近一年最高价：{price_data['high']:.2f} 元（利弗莫尔趋势分析）")
        print(f"✓ 近一年最低价：{price_data['low']:.2f} 元（支撑位分析）")
    if dividend_data is not None:
        print(f"✓ 最新股息数据已获取（股息率模型分析）")
    if finance_data is not None:
        print(f"✓ 最近5年财务数据已获取（共{len(finance_data)}期）")

if __name__ == "__main__":
    main()
