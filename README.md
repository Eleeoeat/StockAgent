# 📊 AI 价值投资分析助手 (StockAgent)

一个基于 Streamlit 的 A股股票价值投资分析工具，集成 DeepSeek AI、akshare 数据源和多维度估值模型。
## 🖼️ 界面演示（以“贵州茅台”为例）

![Step 1 - 输入与财务摘要](https://github.com/Eleeoeat/StockAgent/raw/main/screenshots/step1.png)
![Step 2 - 核心指标与AI报告开头](https://github.com/Eleeoeat/StockAgent/raw/main/screenshots/step2.png)
![Step 3 - 多维度估值与趋势分析](https://github.com/Eleeoeat/StockAgent/raw/main/screenshots/step3.png)
![Step 4 - 风险与投资建议](https://github.com/Eleeoeat/StockAgent/raw/main/screenshots/step4.png)

> 💡 报告包含：核心量化指标、四大估值模型对比、利弗莫尔趋势信号、股息策略分析、三大风险提示、明确操作建议。
## 🚀 快速开始

### 1. 安装依赖
```bash
pip install streamlit akshare openai pandas numpy
```

### 2. 获取 API Key
- 访问 [DeepSeek 官网](https://www.deepseek.com) 获取 API Key

### 3. 运行应用

**方式一：双击启动（推荐）** ⭐
- Windows: 双击 `run.bat` 文件
- 或双击 `run.py` 文件

**方式二：命令行启动**
```bash
streamlit run app_v2_enhanced.py
```

## 📊 核心功能

### 数据获取
- **近一年价格范围** - 52周最高/最低价（用于 Livermore 趋势分析）
- **实时股价数据** - 最新价格、市盈率、涨跌幅
- **股息数据** - 最新派息、分配率、历史股息分位

### 估值模型（多维对比）
- **PE 估值模型** - 市盈率法估值
- **PB 估值模型** - 市净率法估值
- **ROE 估值模型** - 净资产收益率法估值
- **PEG 估值模型** - 增长率调整市盈率法

### AI 分析
- **三大投资流派** - Graham（基本面）、Buffett（护城河）、Livermore（技术面）
- **多维度估值对比** - 四种模型估值结果对比
- **综合投资建议** - 基于数据的智能分析

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `run.bat` | ⭐ Windows 一键启动（双击打开） |
| `run.py` | ⭐ 通用启动脚本（双击打开） |
| `app_v2_enhanced.py` | 主应用程序 |
| `test_data_fetch.py` | 数据源验证工具 |
| `README.md` | 本文件 |

## ⚙️ 最近修复

### v2.0.1 (2026-01-16)
- ✅ 修复近一年价格范围获取失败（中文列名编码问题）
  - 改用位置索引 `iloc[:, 2]`（最高价）和 `iloc[:, 3]`（最低价）
- ✅ 修复 None 值格式化错误
  - 添加安全的条件格式化替代不安全的 `.2f` 格式
  - 缺失数据显示"数据暂无"而不是崩溃
- ✅ 改进股息数据提取
  - 确保提取数字型数据而不是日期对象

## 🐛 故障排查

### 问题：获取近一年价格范围失败
**解决方案**：已在 v2.0.1 修复，使用位置索引替代列名

### 问题：显示"数据暂无"
**原因**：数据源（akshare）暂时无法获取该数据
**解决方案**：稍后重试或检查网络连接

## 📝 使用流程

1. 启动应用后，在侧边栏输入 DeepSeek API Key
2. 输入股票代码（如 600519 表示贵州茅台）
3. 应用自动获取并展示：
   - 价格范围卡片
   - 实时市场数据
   - 四种估值模型结果
   - AI 综合分析报告
4. 基于报告制定投资决策

## 💡 投资建议

该工具仅供参考，不构成投资建议。投资前请：
- 审阅公司财报
- 了解行业动态
- 综合多方信息
- 咨询专业顾问

## 📦 快速安装（通过 git clone）

```bash
# 克隆项目
git clone https://github.com/Eleeoeat/StockAgent.git
cd StockAgent

# 安装依赖
pip install -r requirements.txt

# 运行应用
python run.py
```

## 🙏 致谢与参考

本项目是基于 [ValueCell-ai/valuecell](https://github.com/ValueCell-ai/valuecell) 项目的简化版本，主要功能包括：
- 核心数据获取功能（52周价格范围、股息数据等）
- 多维度估值模型分析
- AI 投资分析助手

感谢原项目的开源贡献！

## 📄 许可证

本项目采用 MIT License，详见 [LICENSE](LICENSE) 文件

---

**最后更新**：2026年1月16日
