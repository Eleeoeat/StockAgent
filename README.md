# 📊 AI 价值投资分析助手 (StockAgent)

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.45.1-FF4B4B.svg)
![DeepSeek](https://img.shields.io/badge/AI-DeepSeek-purple.svg)

一个基于 **Streamlit** 的 A股股票价值投资分析工具  
集成 **DeepSeek AI**、**akshare** 数据源和多维度估值模型  
助力投资者进行数据驱动的理性投资决策

[快速开始](#-快速开始) • [功能特性](#-核心功能) • [界面演示](#-界面演示) • [更新日志](#️-最近更新)

</div>

---

## 🖼️ 界面演示

<div align="center">

### 📈 完整分析流程展示（以"贵州茅台"为例）

</div>

<table>
<tr>
<td width="50%">

**Step 1: 输入与财务摘要**  
![输入与财务摘要](https://github.com/Eleeoeat/StockAgent/raw/main/screenshots/step1.png)
*展示财务数据获取和关键指标筛选*

</td>
<td width="50%">

**Step 2: 核心指标与AI报告开头**  
![核心指标与AI报告](https://github.com/Eleeoeat/StockAgent/raw/main/screenshots/step2.png)
*多维度估值模型对比分析*

</td>
</tr>
<tr>
<td width="50%">

**Step 3: 多维度估值与趋势分析**  
![估值与趋势](https://github.com/Eleeoeat/StockAgent/raw/main/screenshots/step3.png)
*利弗莫尔趋势信号+股息策略分析*

</td>
<td width="50%">

**Step 4: 风险与投资建议**  
![风险与建议](https://github.com/Eleeoeat/StockAgent/raw/main/screenshots/step4.png)
*风险提示+明确的买入/持有/卖出建议*

</td>
</tr>
</table>

<div align="center">

> 💡 **报告包含**：核心量化指标清单 • 四大估值模型对比 • 利弗莫尔趋势信号  
> 股息策略分析 • 三大风险提示 • 明确操作建议

</div>

---

## 🚀 快速开始

### 前置要求
- **Python 3.8+** （推荐 3.10 或更高版本）
- **pip** 或 **conda** 包管理器

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

**推荐方式：创建 .env 文件（自动识别）** ⭐

#### 如何创建 .env 文件

**方法一：使用 PowerShell（推荐）**
```powershell
# 在项目文件夹打开 PowerShell，运行：
Copy-Item .env.example .env
```

**方法二：手动创建**
1. 找到项目文件夹中的 `.env.example` 文件
2. 复制该文件
3. 将复制的文件重命名为 `.env`（注意：文件名就是 `.env`，没有任何后缀）

#### 填写 API Key

1. 用文本编辑器（记事本、VS Code 等）打开 `.env` 文件
2. 将 `sk-your-api-key-here` 替换为你的真实 API Key：
   ```
   DEEPSEEK_API_KEY=sk-你的真实API-Key
   ```
3. 保存文件

#### 获取 API Key
访问 [DeepSeek 官网](https://www.deepseek.com) 注册并获取 API Key

**备选方式：手动输入**
- 如果没有 `.env` 文件，启动应用后在侧边栏直接输入 API Key

⚠️ **注意**：`.env` 文件包含敏感信息，已添加到 `.gitignore`，不会被上传到 GitHub

### 3. 运行应用

#### 方式一：使用启动脚本（推荐）⭐

**步骤 1：配置 Conda 环境名称**

1. 用文本编辑器（如 VSCode、记事本）打开 `run.bat` 文件
2. 找到第 5 行：
   ```bat
   set ENV_NAME=myenv
   ```
3. 将 `myenv` 改为你实际的 conda 环境名称，例如：
   ```bat
   set ENV_NAME=data_work     # 如果你的环境名是 data_work
   set ENV_NAME=stock_analysis # 如果你的环境名是 stock_analysis
   ```
4. 保存文件（Ctrl+S）

**步骤 2：运行应用**

- **Windows 用户**：直接双击 `run.bat` 文件
  - 脚本会自动激活指定的 conda 环境
  - 自动启动 Streamlit 应用
  - 浏览器会自动打开应用界面

- **或者**：双击 `run.py` 文件（需提前手动激活环境）

**可能遇到的问题**：
- 如果提示 `[ERROR] Failed to activate environment`，请检查：
  1. Anaconda/Miniconda 是否已正确安装
  2. 环境名称是否拼写正确（使用 `conda env list` 查看所有环境）
  3. 是否在正确的目录运行脚本

💡 **提示**：由于 Windows 批处理文件的编码限制，脚本提示信息使用英文显示

---

#### 方式二：命令行启动

如果你熟悉命令行，可以手动执行：

```bash
<table>
<tr>
<td width="50%">

### 🤖 AI 模型选择
- **DeepSeek-Chat (V3)**  
  ⚡ 快速响应模式，适合日常快速分析  
  ⏱️ 通常2-5秒生成完整报告
  
- **DeepSeek-Reasoner (R1)**  
  🧠 深度推理模式，适合复杂投资决策  
  🔍 逻辑链完整，分析更深入

💡 可在侧边栏一键切换

</td>
<td width="50%">

### 📈 数据获取能力
- **实时行情数据**  
  最新价、涨跌幅、市盈率、成交量
  
- **历史价格数据**  
  52周最高/最低价（利弗莫尔趋势分析）
  
- **财务报表数据**  
  近10年年报关键指标（ROE、净利润、毛利率等）
  
- **分红历史数据**  
  近10年派息记录及股息率分析

</td>
</tr>
<tr>
<td width="50%">

### 💰 估值模型（多维对比）

#### 1️⃣ PE倍数法
- 基于市盈率估值
- **A股标准**：低估<15 | 合理15-25 | 偏高25-35 | 高估>35

#### 2️⃣ PEG模型  
- 增长率调整市盈率
- **自动提取**财报真实增长率
- 标准：低估<1 | 合理1-1.5 | 偏高1.5-2 | 高估>2

#### 3️⃣ 股息率模型
- 基于分红稳定性和收益率
- 历史分位数分析

</td>
<td width="50%">

### 🎯 AI 分析维度

#### 📋 核心量化指标
ROE、毛利率、PE、PB、PEG、股息率、资产负债率等

#### 📊 多维度估值对比
综合 PE/PEG/股息率 等模型，给出估值结论

#### 📈 利弗莫尔趋势信号
价格位置分析（距52周高/低点的距离）

#### 💵 股息策略分析
分红吸引力、历史分位、稳定性评估

#### ⚠️ 风险提示
至少3条具体风险点，避免盲目乐观

#### ✅ 投资建议
明确的**买入/观望/卖出**操作建议

</td>
</tr>
</table>

---
在运行应用前，可以先验证环境：

```bash
# 1. 查看所有 conda 环境
conda env list

# 2. 激活目标环境
conda activate your_env_name

# 3. 检查已安装的包
pip list | findstr "streamlit akshare openai"

# 4. 验证 Python 版本（建议 3.8+）
python --version
```

⚠️ **重要提醒**：
- 必须在安装了所有依赖（见 `requirements.txt`）的 Python 环境中运行
- 如果提示缺少模块，请返回第 1 步重新安装依赖
- 确保 `.env` 文件已配置 DeepSeek API Key

## 📊 核心功能

### AI 模型选择
- **DeepSeek-Chat (V3)** - 快速响应，适合日常快速分析
- **DeepSeek-Reasoner (R1)** - 深度推理，适合复杂投资决策
- 可在侧边栏自由切换

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
| `requirements.txt` | Python 依赖列表 |
```mermaid
graph LR
    A[启动应用] --> B[输入API Key]
    B --> C[输入公司名称]
    C --> D[点击分析按钮]
    D --> E[获取实时数据]
    E --> F[计算估值模型]
    F --> G[AI深度分析]
    G --> H[生成投资报告]
    H --> I[制定投资决策]
```

### 详细步骤

1. **启动应用**  
   双击 `run.bat`（Windows）或运行 `streamlit run app_v2_enhanced.py`

2. **配置 API Key**  
   在侧边栏输入 DeepSeek API Key（或提前配置 `.env` 文件）

3. **输入公司名称**  
   输入框输入公司名称，如：`贵州茅台`、`宁德时代`、`比亚迪`等  
   ⚠️ **注意**：输入的是公司名称，不是股票代码

4. **选择AI模型**（可选）  
   - DeepSeek-Chat (V3)：快速分析（推荐日常使用）
   - DeepSeek-Reasoner (R1)：深度分析（推荐重大决策）

5. **开始分析**  
   点击"开始深度分析"按钮，应用会自动：
   - 🔍 检索股票代码
   - 📊 抓取财务数据
   - 📈 获取价格和股息数据
   - 🔢 计算多维度估值模型
   - 🤖 调用 AI 生成分析报告

6. **查看结果**  
   - **数据面板**：52周价格、股息率、估值对比
   - **财务摘要**：近10年关键财务指标
   - **AI报告**：综合分析和投资建议

7. **制定决策**  
   基于报告的风险提示和投资建议，结合个人风险偏好做出决策

---

## 🕐️ 最近更新

### v2.3.0 (2026-01-19) - 数据精简优化
- ⚡ **优化数据引用量**
  - 财报数据从 20期 精简至 10期（最近2-3年数据更有参考价值）
  - 智能筛选关键指标：ROE、净利润、营收、毛利率、净利率、资产负债率、EPS、增长率等
  - 界面显示完整数据，AI分析使用精简数据
  - 新增"查看AI分析用数据"折叠面板，透明化数据处理
- 📊 **分析效果提升**
  - 减少无关信息干扰，AI更聚焦核心财务指标
  - Token消耗降低约50%，响应速度更快
  - 分析结论更精准，避免信息过载

### v2.2.0 (2026-01-19) - 估值模型优化
- 🔧 **优化 PE 估值模型**
  - 调整阈值适配 A股市场：低估<15 | 合理15-25 | 偏高25-35 | 高估>35
  - 市场平均 PE 从 15 调整为 25，更符合 A股实际
- 🔧 **优化 PEG 估值模型**
  - 自动从财报提取真实净利润增长率（优先使用）
  - 增长率来源标注（财报数据 vs 预估值）
  - 优化判断标准：低估<1 | 合理1-1.5 | 偏高1.5-2 | 高估>2
- 📊 **改进股息率数据处理**
  - 历史数据范围调整为 10年（与财报数据保持一致）
  - 改进缺失值处理，只记录有效派息数据
  - 显示实际数据年限，数据不足时给出提示
- 💡 **增强 AI 分析提示**
  - 在 AI prompt 中说明估值标准（PE/PEG阈值调整、数据来源说明）
  - 提醒 AI 注意数据年限，避免过度解读有限数据

### v2.1.0 (2026-01-16) - AI 模型选择
- 🤖 **新增模型切换功能**
  - 在侧边栏添加 AI 模型选择器
  - 支持 deepseek-chat (V3) 和 deepseek-reasoner (R1) 两种模型
  - 用户可根据分析需求选择快速响应或深度推理模式

### v2.0.1 (2026-01-16) - Bug 修复
- ✅ 修复近一年价格范围获取失败（中文列名编码问题）
  - 改用位置索引 `iloc[:, 2]`（最高价）和 `iloc[:, 3]`（最低价）
- ✅ 修复 None 值格式化错误
  - 添加安全的条件格式化替代不安全的 `.2f` 格式
  - 缺失数据显示"数据暂无"而不是崩溃
- ✅ 改进股息数据提取
  - 确保提取数字型数据而不是日期对象

---

## 🐛 故障排查

### 问题：获取近一年价格范围失败
**解决方案**：已在 v2.0.1 修复，使用位置索引替代列名

### 问题：显示"数据暂无"
**原因**：数据源（akshare）暂时无法获取该数据
**解决方案**：稍后重试或检查网络连接

---

## 💡 投资建议与免责声明

<div align="center">

### ⚠️ 重要提示

</div>

```
本工具仅供学习和参考使用，不构成任何投资建议。
投资有风险，决策需谨慎。
```

**使用本工具前，请务必注意**：

- 📖 **审阅公司财报**  
  深入阅读年报、季报，了解公司真实经营状况

- 🏭 **了解行业动态**  
  关注行业政策、竞争格局、技术变革

- 📊 **综合多方信息**  
  结合多个分析工具和专业研报，避免单一信息源

**AI分析的局限性**：
- ✓ 可以：提供数据驱动的量化分析
- ✓ 可以：识别历史财务趋势和估值水平
- ✗ 不能：预测未来股价走势
- ✗ 不能：考虑突发事件和政策变化
- ✗ 不能：替代专业投资顾问的经验判断

---

## 📦 快速安装（通过 git clone）

```bash
# 克隆项目
git clone https://github.com/Eleeoeat/StockAgent.git
cd StockAgent  # 进入项目文件夹

# 安装依赖（确保已激活正确的 Python 环境）
pip install -r requirements.txt

# 运行应用
python run.py  # 或双击 run.py / run.bat
```

## 🙏 致谢与参考

受到以下项目和理念的启发：

### 📚 参考项目
- **[ValueCell-ai/valuecell](https://github.com/ValueCell-ai/valuecell)**  
  提供了核心数据获取思路、估值模型框架和AI分析流程

### 💡 投资理念参考
- **Benjamin Graham（本杰明·格雷厄姆）**  
  价值投资之父，安全边际理论
- **Warren Buffett（沃伦·巴菲特）**  
  护城河理论，长期持有优质企业
- **Jesse Livermore（杰西·利弗莫尔）**  
  趋势跟踪，价格位置分析

### 🛠️ 技术栈
- **Streamlit** - Web应用框架
- **akshare** - A股数据源
- **DeepSeek AI** - 智能分析引擎
- **pandas & numpy** - 数据处理

### 🌟 特别感谢
感谢所有开源项目的贡献者，让价值投资工具的开发变得更加容易！

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议

```
MIT License - 你可以自由地使用、修改、分发本项目
但需要保留原作者的版权声明
```

---

## 📞 联系方式

- **GitHub**: [@Eleeoeat](https://github.com/Eleeoeat)
- **项目地址**: [StockAgent](https://github.com/Eleeoeat/StockAgent)
- **问题反馈**: [Issues](https://github.com/Eleeoeat/StockAgent/issues)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，欢迎 Star ⭐**

**最后更新**：2026年1月19日

Made with ❤️ by [Eleeoeat](https://github.com/Eleeoeat)

</div>
