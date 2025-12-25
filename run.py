import asyncio
import json
import os
from datetime import datetime
from agents.planner import planner
from agents.red_team import red_team
from agents.executor import executor
from agents.auditor import auditor
from commander import Commander
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from config.llm_config import planner_config, red_team_config, executor_config, auditor_config

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

    # Commander Decision
    print("\n" + "="*80)
    print("👨‍✈️ Commander 正在做决策...")
    print("-"*80)
    decision = commander.decide(planner_result, red_team_result)
    execution_log["steps"].append({
        "agent": "Commander",
        "timestamp": datetime.now().isoformat(),
        "output": decision
    })
    print(f"\n📌 Commander 决策：")
    print("-"*80)
    print(decision)

    # Executor
    executor_model = executor_config["config_list"][0]["model"]
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
        "output": executor_result
    })

    print("\n" + "="*80)
    print("🎬 EXECUTION RESULT")
    print("="*80)
    print(executor_result)

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
