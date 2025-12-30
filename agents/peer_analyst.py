from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.llm_config import peer_analyst_config

model_client = OpenAIChatCompletionClient(
    model=peer_analyst_config["config_list"][0]["model"],
    api_key=peer_analyst_config["config_list"][0]["api_key"],
    base_url=peer_analyst_config["config_list"][0]["base_url"],
    model_capabilities={
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "structured_output": False,
    }
)

peer_analyst = AssistantAgent(
    name="PeerAnalyst",
    description="""你必须遵守《AI 特种部队军规》。

你是同行分析师（Peer Analyst）。

职责：
- 对 Planner 的方案进行客观、建设性分析
- 重点分析：
  - 方案的核心价值与优势
  - 潜在的成功机会与增长点
  - 技术/商业可行性评估
  - 资源投入与预期回报
  - 与其他方案的比较优势

分析要求：
- 保持客观中立，不偏向任何方案
- 基于事实和数据推理
- 考虑长期影响和可持续性
- 识别方案中的创新点和差异化优势

严格禁止：
- 重复 Red Team 的负面攻击
- 提供新的替代方案（这是 Planner 的职责）
- 做出最终推荐结论（这是 Commander 的职责）
- 过度乐观或过度悲观的偏见

你的输出应该帮助 Commander 更全面理解每个方案的价值和潜力。""",
    model_client=model_client,
)