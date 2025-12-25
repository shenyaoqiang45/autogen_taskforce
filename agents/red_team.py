from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.llm_config import red_team_config

model_client = OpenAIChatCompletionClient(
    model=red_team_config["config_list"][0]["model"],
    api_key=red_team_config["config_list"][0]["api_key"],
    base_url=red_team_config["config_list"][0]["base_url"],
    model_capabilities={
        "vision": False,
        "function_calling": True,
        "json_output": False,
    }
)

red_team = AssistantAgent(
    name="RedTeam",
    description="""你必须遵守《AI 特种部队军规》。

你是红队（Red Team）。

职责：
- 对当前方案进行无情攻击
- 重点关注：
  - 隐性假设
  - 现实不可行性
  - 过度乐观判断
  - 逻辑跳跃

严格禁止：
- 提出替代方案
- 给出建设性建议
""",
    model_client=model_client,
)
