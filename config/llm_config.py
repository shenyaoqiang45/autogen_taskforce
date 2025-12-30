"""
LLM 配置 - 按照《配置最大系统能力.md》的最优主模型配置

异构模型配置原则：
1. Planner (Claude 4.5): 扩展解空间，最强战略思考能力
2. Red Team (DeepSeek-R1): 高强度反例构造，严格推理
3. Executor (GPT-5.2): 工程与工具成功率优先
4. Auditor (DeepSeek-R1): 严苛否决，零温度审计

系统能力 = 问题空间覆盖率 × 失败模式发现概率 × 错误阻断概率 × 稳定性
"""

# WhatAI 中转 API 配置
WHATAI_API_KEY = "sk-cbnYQN5y7lWjyNSgASgf3Gr9lumP1vYN2B2r9vpF6x9M7QRL"
WHATAI_BASE_URL = "https://api.whatai.cc/v1"

# DeepSeek 官方 API 配置
DEEPSEEK_API_KEY = "sk-f71caf6ed44145b683fcd816b5171b4a"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# Planner: Claude 4.5 - 扩展解空间
planner_config = {
    "config_list": [
        {
            "model": "claude-sonnet-4-5-20250929",
            "api_key": WHATAI_API_KEY,
            "base_url": WHATAI_BASE_URL
        }
    ],
    "temperature": 0.3,  # 保持创造性但不失控
    "cache_seed": None
}

# Red Team: DeepSeek-R1 - 高强度反例构造
red_team_config = {
    "config_list": [
        {
            "model": "deepseek-reasoner",  # DeepSeek-R1
            "api_key": DEEPSEEK_API_KEY,
            "base_url": DEEPSEEK_BASE_URL
        }
    ],
    "temperature": 0.1,  # 严格推理，低温度
    "cache_seed": None
}

# Executor: GPT-5.2 - 工程与工具成功率优先
executor_config = {
    "config_list": [
        {
            "model": "gpt-5.2",
            "api_key": WHATAI_API_KEY,
            "base_url": WHATAI_BASE_URL
        }
    ],
    "temperature": 0.2,  # 工程化执行，需要稳定性
    "cache_seed": None
}

# Auditor: DeepSeek-R1 - 严苛否决
auditor_config = {
    "config_list": [
        {
            "model": "deepseek-reasoner",  # DeepSeek-R1
            "api_key": DEEPSEEK_API_KEY,
            "base_url": DEEPSEEK_BASE_URL
        }
    ],
    "temperature": 0.0,  # 最严格的判定，零温度
    "cache_seed": None
}

# Peer Analyst: GPT-4o - 建设性分析
peer_analyst_config = {
    "config_list": [
        {
            "model": "gpt-4o",  # GPT-4o
            "api_key": WHATAI_API_KEY,
            "base_url": WHATAI_BASE_URL
        }
    ],
    "temperature": 0.4,  # 建设性分析，适度创造性
    "cache_seed": None
}

# 配置说明
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
当前配置状态（完整异构配置 ✅）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent      | 模型              | API 来源        | 温度  | 作用
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Planner    | Claude 4.5        | WhatAI 中转     | 0.3  | 扩展解空间
Red Team   | DeepSeek-R1       | DeepSeek 官方   | 0.1  | 构造反例
Peer Analyst | GPT-4o          | WhatAI 中转     | 0.4  | 建设性分析
Executor   | GPT-5.2           | WhatAI 中转     | 0.2  | 工程执行
Auditor    | DeepSeek-R1       | DeepSeek 官方   | 0.0  | 零温度审计
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

异构配置优势：
1. 认知多样性
   - Claude (Planner): 战略思考和创造性方案
   - DeepSeek (Red Team): 严格推理和反例构造
   - GPT (Peer Analyst): 建设性分析和价值评估
   - GPT (Executor): 工程实现和工具调用

2. 相互制约与平衡
   - Planner 创造性方案 → Red Team 严格质疑 → Peer Analyst 建设性分析
   - Red Team 负面攻击与 Peer Analyst 正面分析形成决策平衡
   - Executor 实现方案 → Auditor 零温度审计

3. 降低系统性错误
   - 不同模型不会犯相同错误
   - 高置信错误被多层检验拦截
   - 正反分析结合减少认知偏见

API 配置：
- WhatAI 中转: https://api.whatai.cc/v1
  - 支持 Claude 和 GPT 系列模型
  - API Key: sk-cbnY...7QRL
  
- DeepSeek 官方: https://api.deepseek.com/v1
  - 支持 DeepSeek-R1 推理模型
  - API Key: sk-f71c...1b4a

如遇连接问题，可尝试：
- https://api.whatai.cc
- https://api.whatai.cc/v1/chat/completions
"""
