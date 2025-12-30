import asyncio
import json
import os
from datetime import datetime
from agents.planner import planner
from agents.red_team import red_team
from agents.peer_analyst import peer_analyst
from agents.executor import executor
from agents.auditor import auditor
from commander import Commander
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from config.llm_config import planner_config, red_team_config, peer_analyst_config, executor_config, auditor_config

async def main():
    commander = Commander()
    
    # 创建日志目录
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    execution_log = {
        "timestamp": datetime.now().isoformat(),
        "model_config": {
            "Planner": planner_config["config_list"][0]["model"],
            "RedTeam": red_team_config["config_list"][0]["model"],
            "PeerAnalyst": peer_analyst_config["config_list"][0]["model"],
            "Executor": executor_config["config_list"][0]["model"],
            "Auditor": auditor_config["config_list"][0]["model"]
        },
        "steps": []
    }

    mission = input("请输入战略目标：")
    execution_log["mission"] = mission

    print("\n" + "="*80)
    print(f"🎯 MISSION: {mission}")
    print("="*80)

    # Planner
    planner_model = planner_config["config_list"][0]["model"]
    print(f"\n📋 Planner 正在制定计划... [模型: {planner_model}]")
    print("-"*80)
    planner_response = await planner.on_messages(
        [TextMessage(content=mission, source="user")],
        CancellationToken()
    )
    planner_result = planner_response.chat_message.content
    execution_log["steps"].append({
        "agent": "Planner",
        "model": planner_model,
        "timestamp": datetime.now().isoformat(),
        "output": planner_result
    })
    print(f"\n✅ Planner 输出：")
    print("-"*80)
    print(planner_result)

    # Red Team
    red_team_model = red_team_config["config_list"][0]["model"]
    print("\n" + "="*80)
    print(f"🔴 Red Team 正在评估风险... [模型: {red_team_model}]")
    print("-"*80)
    red_team_response = await red_team.on_messages(
        [TextMessage(content=planner_result, source="user")],
        CancellationToken()
    )
    red_team_result = red_team_response.chat_message.content
    execution_log["steps"].append({
        "agent": "RedTeam",
        "model": red_team_model,
        "timestamp": datetime.now().isoformat(),
        "output": red_team_result
    })
    print(f"\n⚠️ Red Team 输出：")
    print("-"*80)
    print(red_team_result)

    # Peer Analyst
    peer_analyst_model = peer_analyst_config["config_list"][0]["model"]
    print("\n" + "="*80)
    print(f"🔍 Peer Analyst 正在进行分析... [模型: {peer_analyst_model}]")
    print("-"*80)
    analysis_message = f"""
任务目标：
{mission}

Planner 的方案：
{planner_result}

Red Team 的风险评估：
{red_team_result}

请对方案进行建设性分析，重点关注：
1. 方案的核心价值与优势
2. 潜在的成功机会
3. 技术/商业可行性
4. 资源投入与预期回报
"""
    peer_analyst_response = await peer_analyst.on_messages(
        [TextMessage(content=analysis_message, source="user")],
        CancellationToken()
    )
    peer_analyst_result = peer_analyst_response.chat_message.content
    execution_log["steps"].append({
        "agent": "PeerAnalyst",
        "model": peer_analyst_model,
        "timestamp": datetime.now().isoformat(),
        "output": peer_analyst_result
    })
    print(f"\n💡 Peer Analyst 分析：")
    print("-"*80)
    print(peer_analyst_result)

    # Commander Decision
    print("\n" + "="*80)
    print("👨‍✈️ Commander 正在做决策...")
    print("-"*80)
    decision = commander.decide(planner_result, red_team_result, peer_analyst_result)
    execution_log["steps"].append({
        "agent": "Commander",
        "timestamp": datetime.now().isoformat(),
        "output": decision
    })
    print(f"\n📌 Commander 决策：")
    print("-"*80)
    print(decision)

    # Executor with retry mechanism
    executor_model = executor_config["config_list"][0]["model"]
    max_retries = 3
    retry_count = 0
    executor_completed = False
    executor_result = ""

    while not executor_completed and retry_count < max_retries:
        if retry_count > 0:
            print(f"\n🔄 Executor 重试 ({retry_count}/{max_retries-1})...")

        print("\n" + "="*80)
        print(f"⚙️ Executor 正在执行任务... [模型: {executor_model}]")
        print("-"*80)

        executor_response = await executor.on_messages(
            [TextMessage(content=decision, source="user")],
            CancellationToken()
        )
        executor_result = executor_response.chat_message.content

        execution_log["steps"].append({
            "agent": "Executor",
            "model": executor_model,
            "timestamp": datetime.now().isoformat(),
            "output": executor_result,
            "retry_count": retry_count
        })

        print("\n" + "="*80)
        print("🎬 EXECUTION RESULT")
        print("="*80)
        print(executor_result)

        # Check if Executor needs clarification
        if "[EXECUTOR_ERROR:" in executor_result:
            print("\n⚠️  Executor 无法执行，需要更具体的指令")
            retry_count += 1

            if retry_count < max_retries:
                # Get clarification from Commander
                print("\n" + "="*80)
                print("🔄 重新请求指挥官决策...")
                print("="*80)

                decision = commander.redecide(
                    planner_result,
                    red_team_result,
                    peer_analyst_result,
                    executor_result
                )

                # Log the redecision
                execution_log["steps"].append({
                    "agent": "Commander",
                    "timestamp": datetime.now().isoformat(),
                    "output": f"[REDECISION {retry_count}] {decision}"
                })

                print(f"\n📌 重新决策 ({retry_count}):")
                print("-"*80)
                print(decision)
            else:
                print(f"\n❌ 达到最大重试次数 ({max_retries})，继续审计流程")
                executor_completed = True
        else:
            executor_completed = True

    if not executor_completed:
        print(f"\n⚠️  Executor 未完成执行，达到最大重试次数")

    # Auditor
    auditor_model = auditor_config["config_list"][0]["model"]
    print("\n" + "="*80)
    print(f"📊 Auditor 正在审计... [模型: {auditor_model}]")
    print("-"*80)
    audit_message = f"""
任务目标：
{mission}

Planner 输出：
{planner_result}

Red Team 输出：
{red_team_result}

Peer Analyst 分析：
{peer_analyst_result}

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
    execution_log["steps"].append({
        "agent": "Auditor",
        "model": auditor_model,
        "timestamp": datetime.now().isoformat(),
        "output": audit_result
    })

    print("\n" + "="*80)
    print("📈 AUDIT REPORT")
    print("="*80)
    print(audit_result)

    # 保存日志
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(execution_log, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print(f"💾 执行日志已保存到: {log_file}")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())
