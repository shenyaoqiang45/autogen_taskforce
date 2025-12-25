import json
import os
from datetime import datetime
from pathlib import Path

def list_logs():
    """列出所有日志文件"""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        print("❌ 日志目录不存在")
        return []
    
    log_files = sorted(logs_dir.glob("run_*.json"), reverse=True)
    return log_files

def view_log(log_file):
    """查看单个日志文件"""
    with open(log_file, 'r', encoding='utf-8') as f:
        log_data = json.load(f)
    
    print("\n" + "="*80)
    print(f"📁 日志文件: {log_file.name}")
    print(f"⏰ 执行时间: {log_data['timestamp']}")
    print("="*80)
    
    print(f"\n🎯 任务目标:")
    print("-"*80)
    print(log_data['mission'])
    
    for i, step in enumerate(log_data['steps'], 1):
        agent_emoji = {
            "Planner": "📋",
            "RedTeam": "🔴",
            "Commander": "👨‍✈️",
            "Executor": "⚙️",
            "Auditor": "📊"
        }
        
        emoji = agent_emoji.get(step['agent'], "🤖")
        print(f"\n{emoji} 步骤 {i}: {step['agent']}")
        print(f"⏰ 时间: {step.get('timestamp', 'N/A')}")
        print("-"*80)
        print(step['output'])
    
    print("\n" + "="*80)

def main():
    log_files = list_logs()
    
    if not log_files:
        print("❌ 没有找到日志文件")
        return
    
    print("\n📚 可用的日志文件:")
    print("="*80)
    for i, log_file in enumerate(log_files, 1):
        # 从文件名提取时间
        filename = log_file.stem
        timestamp_str = filename.replace("run_", "")
        try:
            dt = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            formatted_time = timestamp_str
        
        print(f"{i}. {formatted_time} - {log_file.name}")
    
    print("="*80)
    
    try:
        choice = input("\n请选择要查看的日志编号 (输入 0 退出): ")
        choice = int(choice)
        
        if choice == 0:
            print("👋 再见！")
            return
        
        if 1 <= choice <= len(log_files):
            view_log(log_files[choice - 1])
        else:
            print("❌ 无效的选择")
    except ValueError:
        print("❌ 请输入有效的数字")
    except KeyboardInterrupt:
        print("\n👋 再见！")

if __name__ == "__main__":
    main()
