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
    }
)

executor = AssistantAgent(
    name="Executor",
    description="""你必须遵守《AI 特种部队军规》。

你是执行专家（Executor）。

职责：
- 严格按指挥官指定方案执行
- 输出代码、文档、分析结果

严格禁止：
- 质疑目标
- 修改方案
- 进行战略讨论
""",
    model_client=model_client,
)
