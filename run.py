import asyncio
from agents.planner import planner
from agents.red_team import red_team
from agents.executor import executor
from agents.auditor import auditor
from commander import Commander
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

async def main():
    commander = Commander()

    mission = input("请输入战略目标：")

    # Planner
    planner_response = await planner.on_messages(
        [TextMessage(content=mission, source="user")],
        CancellationToken()
    )
    planner_result = planner_response.chat_message.content

    # Red Team
    red_team_response = await red_team.on_messages(
        [TextMessage(content=planner_result, source="user")],
        CancellationToken()
    )
    red_team_result = red_team_response.chat_message.content

    # Commander Decision
    decision = commander.decide(planner_result, red_team_result)

    # Executor
    executor_response = await executor.on_messages(
        [TextMessage(content=decision, source="user")],
        CancellationToken()
    )
    executor_result = executor_response.chat_message.content

    print("\n====== EXECUTION RESULT ======")
    print(executor_result)

    # Auditor
    audit_message = f"""
任务目标：
{mission}

Planner 输出：
{planner_result}

Red Team 输出：
{red_team_result}

人类决策：
{decision}

执行结果：
{executor_result}
"""
    auditor_response = await auditor.on_messages(
        [TextMessage(content=audit_message, source="user")],
        CancellationToken()
    )
    audit_result = auditor_response.chat_message.content

    print("\n====== AUDIT REPORT ======")
    print(audit_result)

if __name__ == "__main__":
    asyncio.run(main())
