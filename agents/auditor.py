from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.llm_config import auditor_config

model_client = OpenAIChatCompletionClient(
    model=auditor_config["config_list"][0]["model"],
    api_key=auditor_config["config_list"][0]["api_key"],
    base_url=auditor_config["config_list"][0]["base_url"],
    model_capabilities={
        "vision": False,
        "function_calling": True,
        "json_output": False,
    }
)

auditor = AssistantAgent(
    name="Auditor",
    description="""你必须遵守《AI 特种部队军规》。

你是审计官（Auditor）。

职责：
- 对完整过程进行复盘
- 明确区分：
  - 事实
  - 推测
  - 人类干预点
- 输出可复用的 SOP 或决策模板

严格禁止：
- 参与实时决策
""",
    model_client=model_client,
)
