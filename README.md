# autogen_taskforce

AI 特种部队 - 基于 AutoGen 的多智能体协作系统，遵循《AI 特种部队军规》和《配置最大系统能力.md》，降低高价值复杂决策中的致命错误概率。

## 📖 项目简介

本项目实现了一个人类指挥官与 AI 智能体协作的决策系统，**采用异构模型配置**以最大化系统能力，包含以下角色：

- **Commander (人类指挥官)**: 拥有最终决策权和责任
- **Planner (战术策划官)**: 将目标拆解为 2 个可执行方案 *[Claude 4.5]*
- **Red Team (红队)**: 寻找方案漏洞和风险 *[DeepSeek-R1]*
- **Peer Analyst (同行分析师)**: 提供建设性分析和价值评估 *[GPT-4o]*
- **Executor (执行专家)**: 将决策转化为具体行动 *[GPT-5.2]*
- **Auditor (审计官)**: 评估执行结果 *[DeepSeek-R1]*

## 🎯 核心设计理念

### 最大化系统能力，而非单一模型性能

```
System Capability = 
  问题空间覆盖率 × 失败模式发现概率 
  × 错误阻断概率 × 单位成本下的稳定性
```

**关键机制**：
1. **异构认知**: 不同 Agent 使用不同模型，避免认知盲区
2. **强制冲突**: Red Team 强制介入，暴露潜在问题
3. **严格否决权**: Auditor 独立判定，可阻断流程
4. **人类裁决**: Commander 承担最终责任

详见：[配置最大系统能力.md](配置最大系统能力.md)

## 🚀 快速开始

### 前置要求

- Python 3.10+
- Conda 环境管理器

### 安装步骤

1. **激活 Conda 环境**
```powershell
conda activate autogen
```

2. **安装依赖**
```powershell
pip install autogen-agentchat autogen-ext
```

3. **配置 API 密钥**

编辑 [config/llm_config.py](config/llm_config.py)，配置各个模型的 API Key：

```python
# WhatAI 中转 API 配置（接入 Claude 和 GPT）
WHATAI_API_KEY = "your-whatai-api-key"
WHATAI_BASE_URL = "https://api.whatai.cc/v1"

# DeepSeek 官方 API 配置
DEEPSEEK_API_KEY = "your-deepseek-api-key"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
```

**当前配置状态（已完成异构配置 ✅）**：
- ✅ Planner: Claude 4.5 (`claude-sonnet-4-5-20250929`) - WhatAI 中转
- ✅ Red Team: DeepSeek-R1 (`deepseek-reasoner`) - DeepSeek 官方
- ✅ Executor: GPT-5.2 (`gpt-5.2`) - WhatAI 中转
- ✅ Auditor: DeepSeek-R1 (`deepseek-reasoner`) - DeepSeek 官方

## 🤖 模型配置说明

### 当前异构模型配置

| Agent | 模型 | API 来源 | 温度 | 作用 |
|-------|------|---------|------|------|
| **Planner** | Claude 4.5 | WhatAI 中转 | 0.3 | 最强解空间扩展能力 |
| **Red Team** | DeepSeek-R1 | DeepSeek 官方 | 0.1 | 严格推理和反例构造 |
| **Peer Analyst** | GPT-4o | WhatAI 中转 | 0.4 | 建设性分析和价值评估 |
| **Executor** | GPT-5.2 | WhatAI 中转 | 0.2 | 工程化能力强 |
| **Auditor** | DeepSeek-R1 | DeepSeek 官方 | 0.0 | 零温度严格审计 |

### 为什么使用异构模型？

根据《配置最大系统能力.md》，使用不同模型的核心原因：

1. **防止系统性认知盲区**
   - 单一模型家族在某些问题上可能有共同的弱点
   - 异构模型可以互相补充盲区

2. **提高错误发现率**
   - Red Team (DeepSeek-R1) 的推理方式不同于 Planner (Claude 4.5)
   - 更容易发现方案中的逻辑漏洞

3. **提供平衡决策视角**
   - Peer Analyst (GPT-4o) 提供建设性分析和价值评估
   - 平衡 Red Team 的负面攻击，帮助人类指挥官全面评估方案

4. **降低高置信错误的发布概率**
   - 不是减少错误生成，而是确保错误被发现
   - Auditor 使用独立模型，避免"一致性错觉"

## 📝 使用教程

### 1. 运行主程序

启动交互式任务流程：

```powershell
python run.py
```

**运行流程**：
1. 输入战略目标（例如：开发一个用户管理系统）
2. **Planner (Claude 4.5)** 制定 2 个可执行方案
3. **Red Team (DeepSeek-R1)** 对每个方案进行风险评估
4. **Peer Analyst (GPT-4o)** 提供建设性分析和价值评估
5. **Commander (你)** 选择执行方案
6. **Executor (GPT-5.2)** 生成具体执行计划
7. **Auditor (DeepSeek-R1)** 审计执行质量

**控制台输出示例**：
```
请输入战略目标：开发一个博客系统
================================================================================
🎯 MISSION: 开发一个博客系统
================================================================================

📋 Planner 正在制定计划... [模型: claude-sonnet-4-5-20250929]
--------------------------------------------------------------------------------
...

🔴 Red Team 正在评估风险... [模型: deepseek-reasoner]
--------------------------------------------------------------------------------
...

🔍 Peer Analyst 正在进行分析... [模型: gpt-4o]
--------------------------------------------------------------------------------
...

⚙️ Executor 正在执行任务... [模型: gpt-5.2]
--------------------------------------------------------------------------------
...

📊 Auditor 正在审计... [模型: deepseek-reasoner]
--------------------------------------------------------------------------------
```

每个步骤都会显示使用的模型，方便观察异构模型的协作效果。

### 2. 查看执行日志

#### 方法 1: 命令行查看（快速查看）

```powershell
python view_logs.py
```

**功能**：
- 列出所有历史执行日志
- 选择日志文件查看详细内容
- 按时间倒序排列，最新的在最前
- 显示每个步骤使用的模型

**示例**：
```
📋 可用日志文件:
1. run_20251225_135340.json (2025-12-25 13:53:40)
2. run_20251225_120521.json (2025-12-25 12:05:21)

请选择要查看的日志编号 (1-2, 或 0 退出): 1
```

#### 方法 2: Web UI 查看（可视化）

启动 Web 日志查看器：

```powershell
python log_viewer.py
```

然后在浏览器打开：`http://localhost:8080`

**功能**：
- 🌐 可视化界面查看所有日志
- 🔍 按步骤展开/折叠查看详情
- 📊 彩色标记不同智能体输出
- 🤖 显示每个步骤使用的模型
- 💾 支持导出和分享

**界面说明**：
- 左侧：日志文件列表（按时间倒序）
- 右侧：选中日志的详细内容
- 每个智能体输出带有不同的图标、颜色和模型标识
- 可以对比不同模型的决策风格和输出质量

### 3. AutoGen Studio（可选）

AutoGen Studio 是官方提供的可视化配置和调试工具。

#### 启动 AutoGen Studio

```powershell
autogenstudio ui --port 8081
```

访问地址：`http://localhost:8081`

#### 主要功能

1. **Skills 管理**
   - 创建和管理智能体技能
   - 测试函数调用

2. **Agents 配置**
   - 可视化配置智能体
   - 设置系统提示词
   - **选择不同模型和参数**（测试异构配置）

3. **Workflows 设计**
   - 拖拽式设计多智能体流程
   - 设置智能体交互规则

4. **Playground 测试**
   - 实时测试智能体对话
   - 查看执行日志
   - 调试和优化

#### 使用 Studio 测试异构模型

在 AutoGen Studio 中，你可以：
1. 为每个 Agent 配置不同的模型
2. 对比相同任务下不同模型组合的表现
3. 快速验证《配置最大系统能力.md》中的理论

#### 注意事项

⚠️ AutoGen Studio 主要用于开发和调试，本项目的核心流程已在 `run.py` 中实现。Studio 可用于：
- 快速原型设计新的智能体
- 调试智能体行为
- 测试不同的提示词和参数
- **验证异构模型配置的效果**

## 📂 项目结构

```
autogen_taskforce/
├── agents/                      # 智能体模块
│   ├── planner.py              # 战术策划官 (Claude 4.5)
│   ├── red_team.py             # 红队 (DeepSeek-R1)
│   ├── peer_analyst.py         # 同行分析师 (GPT-4o)
│   ├── executor.py             # 执行专家 (GPT-5.2)
│   └── auditor.py              # 审计官 (DeepSeek-R1)
├── config/                      # 配置文件
│   └── llm_config.py           # 异构模型配置（API Key等）
├── logs/                        # 执行日志目录
│   └── run_YYYYMMDD_HHMMSS.json  # 包含模型信息的执行日志
├── run.py                       # 主程序入口
├── commander.py                 # 人类指挥官接口
├── view_logs.py                 # 命令行日志查看器
├── log_viewer.py                # Web 日志查看器
├── AI 特种部队军规.md           # 系统设计原则
├── 配置最大系统能力.md          # 模型配置理论
└── README.md                    # 本文件
```

## 🔧 进阶配置

### 调整模型温度

根据任务类型，你可以调整温度参数：

```python
# 需要更多创造性（战略规划）
planner_config["temperature"] = 0.5

# 需要更严格的执行（审计）
auditor_config["temperature"] = 0.0  # 已是零温度
```

### 切换模型供应商

如果需要更换 API 提供商，可以修改配置：

```python
# 使用官方 Anthropic API
planner_config = {
    "config_list": [{
        "model": "claude-sonnet-4-20250514",
        "api_key": "your-claude-key",
        "base_url": "https://api.anthropic.com/v1",
        "api_type": "anthropic"
    }],
    "temperature": 0.3
}

# 使用官方 OpenAI API
executor_config = {
    "config_list": [{
        "model": "gpt-4o",
        "api_key": "your-openai-key",
        "base_url": "https://api.openai.com/v1"
    }],
    "temperature": 0.2
}
```

### 成本优化

如果需要降低成本，可以考虑：

1. **关键节点使用强模型**：仅在 Planner 和 Auditor 使用顶级模型
2. **Executor 使用轻量模型**：如 GPT-3.5-turbo（工程任务）
3. **Red Team 使用本地模型**：如果有算力资源

**注意**：降低模型能力会影响系统整体的错误发现率，需要权衡。

### 日志配置

日志自动保存在 `logs/` 目录，格式：`run_YYYYMMDD_HHMMSS.json`

**日志包含**：
- 任务目标
- 模型配置信息（每个 Agent 使用的模型）
- 每个智能体的输出
- 每个步骤使用的具体模型
- 时间戳
- 完整的决策链

**日志示例结构**：
```json
{
  "timestamp": "2025-12-25T15:30:00",
  "model_config": {
    "Planner": "claude-sonnet-4-5-20250929",
    "RedTeam": "deepseek-reasoner",
    "Executor": "gpt-5.2",
    "Auditor": "deepseek-reasoner"
  },
  "mission": "开发一个博客系统",
  "steps": [
    {
      "agent": "Planner",
      "model": "claude-sonnet-4-5-20250929",
      "timestamp": "2025-12-25T15:30:15",
      "output": "..."
    }
  ]
}
```

## 📋 常见使用场景

### 场景 1: 技术方案决策

```powershell
python run.py
# 输入：开发一个高并发的实时通知系统
```

- **Planner (Claude 4.5)** 提供多个技术方案（WebSocket vs SSE vs Long Polling）
- **Red Team (DeepSeek-R1)** 用严格推理分析各方案风险
- **Executor (GPT-5.2)** 生成工程实现方案
- **Auditor (DeepSeek-R1)** 零温度审计执行质量

**异构优势**：Claude 的创造性 vs DeepSeek 的逻辑严密性 vs GPT 的工程能力

### 场景 2: 业务流程设计

```powershell
python run.py
# 输入：设计一个电商平台的退款流程
```

系统会考虑用户体验、风控、财务等多个维度，不同模型从不同角度评估。

### 场景 3: 风险评估

```powershell
python run.py
# 输入：评估将服务迁移到云端的方案
```

- **Red Team (DeepSeek-R1)** 会重点分析安全、成本、技术债务
- **Auditor (DeepSeek-R1)** 零温度审计，不放过任何疑点

## 🛡️ 设计原则

本项目严格遵循《AI 特种部队军规》和《配置最大系统能力.md》：

### 系统能力公式

```
System Capability = 
  问题空间覆盖率（Planner 用 Claude 扩展）
  × 失败模式发现概率（Red Team 用 DeepSeek 攻击）
  × 错误阻断概率（Auditor 独立审计）
  × 单位成本下的稳定性
```

### 关键原则

1. **人类最终决策权**: AI 只提供分析，不做决策
2. **角色边界清晰**: 每个智能体只负责自己的职责
3. **异构认知**: 不同角色使用不同模型，防止系统性盲区
4. **可追溯**: 所有决策过程完整记录
5. **风险前置**: Red Team 强制介入，暴露潜在问题
6. **零容忍审计**: Auditor 使用零温度，严格把关

详见：
- [AI 特种部队军规.md](AI 特种部队军规.md)
- [配置最大系统能力.md](配置最大系统能力.md)

## 🔬 实验与验证

### 对比实验

你可以通过修改配置文件进行对比实验：

**实验 1: 同构 vs 异构**
```python
# 所有 Agent 都用 DeepSeek
vs
# 当前配置（Claude + DeepSeek + GPT）
```

**实验 2: 温度影响**
```python
# Auditor 温度 0.7（较宽松）
vs
# Auditor 温度 0.0（严格，当前配置）
```

**实验 3: 模型组合**
```python
# 测试不同的模型组合
# 例如：全部用 GPT vs 全部用 Claude vs 异构配置
```

### 日志分析

通过 `log_viewer.py` 或 `view_logs.py`，你可以：
- **对比模型输出**：查看不同模型对同一问题的处理方式
- **统计否决率**：分析 Red Team 和 Auditor 的拦截效果
- **错误分析**：研究哪些类型的错误被成功发现和阻断
- **模型性能**：评估不同模型在各个角色中的表现

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

特别欢迎：
- 新的模型配置实验结果
- 触发式升级机制的实现
- 更多的使用场景和案例

## 📄 许可证

MIT License

---

> **核心理念**: 最大系统能力 = 异构认知 × 强制冲突 × 条件化最强模型 × 人类裁决
