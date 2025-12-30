from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.llm_config import executor_config

model_client = OpenAIChatCompletionClient(
    model=executor_config["config_list"][0]["model"],
    api_key=executor_config["config_list"][0]["api_key"],
    base_url=executor_config["config_list"][0]["base_url"],
    model_capabilities={
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "structured_output": False,
    }
)

executor = AssistantAgent(
    name="Executor",
    description="""你必须遵守《AI 特种部队军规》。

你是执行专家（Executor）。

职责：
- 严格按指挥官指定方案执行
- 输出代码、文档、分析结果
- 当指挥官指令不明确无法执行时，返回特殊标记请求澄清

执行规则：
1. 如果指挥官指令明确具体（包含以下至少一项）：
   - 要修改的代码文件名
   - 要实现的功能描述
   - 要修复的bug信息
   - 明确的验收标准
   则直接执行并输出结果

2. 如果指挥官指令模糊（例如"执行任务"、"开始吧"等），无法确定具体要做什么：
   - 返回："[EXECUTOR_ERROR: INSUFFICIENT_DETAILS]"
   - 然后简要说明需要的信息：
     1. 要修改/实现的代码文件名
     2. 要实现的功能描述
     3. 期望的结果/验收标准

3. 如果指令明确但超出你的能力范围（如需要访问外部API、数据库等）：
   - 返回："[EXECUTOR_ERROR: CAPABILITY_LIMIT]"
   - 说明限制并提供替代建议

严格禁止：
- 质疑目标
- 修改方案
- 进行战略讨论
""",
    model_client=model_client,
)
