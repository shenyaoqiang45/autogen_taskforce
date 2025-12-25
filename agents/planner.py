from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.llm_config import planner_config

model_client = OpenAIChatCompletionClient(
    model=planner_config["config_list"][0]["model"],
    api_key=planner_config["config_list"][0]["api_key"],
    base_url=planner_config["config_list"][0]["base_url"],
    model_capabilities={
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "structured_output": False,
    }
)

planner = AssistantAgent(
    name="Planner",
    description="""你必须遵守《AI 特种部队军规》。

你是战术策划官（Planner）。

职责：
- 将指挥官给出的目标拆解为 2–4 个可执行方案
- 每个方案必须明确：
  1. 核心假设
  2. 所需资源
  3. 最可能失败路径

严格禁止：
- 执行任何具体任务
- 给出最终推荐结论
""",
    model_client=model_client,
)
