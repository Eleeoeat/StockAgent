# 📊 AI 价值投资分析助手 (StockAgent)

一个基于 Streamlit 的 A股股票价值投资分析工具，集成 DeepSeek AI、akshare 数据源和多维度估值模型。

## 🖼️ 界面演示（以"贵州茅台"为例）

![Step 1 - 输入与财务摘要](https://github.com/Eleeoeat/StockAgent/raw/main/screenshots/step1.png)
![Step 2 - 核心指标与AI报告开头](https://github.com/Eleeoeat/StockAgent/raw/main/screenshots/step2.png)
![Step 3 - 多维度估值与趋势分析](https://github.com/Eleeoeat/StockAgent/raw/main/screenshots/step3.png)
![Step 4 - 风险与投资建议](https://github.com/Eleeoeat/StockAgent/raw/main/screenshots/step4.png)

> 💡 报告包含：核心量化指标、四大估值模型对比、利弗莫尔趋势信号、股息策略分析、三大风险提示、明确操作建议。

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
# 步骤 1: 激活包含所需依赖的环境
conda activate your_env_name  # 改为你的环境名

# 步骤 2: 进入项目目录（项目文件夹在哪里就 cd 到哪里）
cd StockAgent  # 如果你在项目父目录
# 或者直接在项目文件夹里打开终端，跳过此步骤

# 步骤 3: 启动应用
streamlit run app_v2_enhanced.py
```

**运行成功后**：
- 程序启动后，应用会在浏览器中自动打开（默认地址：http://localhost:8501）
- 如果浏览器未自动打开，保持终端运行，手动在浏览器访问 http://localhost:8501
- ⚠️ **注意**：必须保持程序运行，关闭终端则应用停止

---

#### 如何确认环境配置正确？

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
| `.env.example` | API Key 配置模板 |
| `.env` | 本地环境变量（需自己创建，不上传） |
| `.gitignore` | Git 忽略规则 |
| `README.md` | 本文件 |

## ⚙️ 最近更新

### v2.1.0 (2026-01-16) - 新增功能
- ✨ **新增 AI 模型切换功能**
  - 支持 DeepSeek-Chat (V3) 和 DeepSeek-Reasoner (R1) 切换
  - 可根据分析需求选择快速响应或深度推理模式

### v2.0.1 (2026-01-16) - Bug 修复
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
cd StockAgent  # 进入项目文件夹

# 安装依赖（确保已激活正确的 Python 环境）
pip install -r requirements.txt

# 运行应用
python run.py  # 或双击 run.py / run.bat
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
