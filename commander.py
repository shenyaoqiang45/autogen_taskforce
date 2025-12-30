class Commander:
    def __init__(self):
        pass

    def decide(self, planner_output, red_team_output, peer_analyst_output):
        print("\n====== PLANNER ======")
        print(planner_output)

        print("\n====== RED TEAM ======")
        print(red_team_output)

        print("\n====== PEER ANALYST ======")
        print(peer_analyst_output)

        decision = input("\n请输入你的命令（例如：执行方案 B）：")
        return decision

    def redecide(self, planner_output, red_team_output, peer_analyst_output, executor_error):
        """当Executor无法执行时重新决策"""
        print("\n" + "!"*80)
        print("⚠️  EXECUTOR 无法执行命令，需要更具体的指令")
        print("!"*80)

        print("\n====== EXECUTOR 反馈 ======")
        print(executor_error)

        print("\n====== 方案回顾 ======")
        print("Planner 方案摘要：")
        # 显示方案的前几行作为摘要
        planner_lines = planner_output.split('\n')
        for i, line in enumerate(planner_lines[:10]):
            if line.strip():
                print(f"  {line}")
        if len(planner_lines) > 10:
            print(f"  ...（共 {len(planner_lines)} 行）")

        print("\n请提供更具体的执行指令，例如：")
        print("1. '实现真正的LLM集成，替换硬编码的任务分解逻辑'")
        print("2. '测试运行 examples/basic_demo.py 并报告结果'")
        print("3. '添加Web界面用于监控智能体状态'")
        print("4. '修复 agent_os/main.py 中的XX行bug'")
        print("\n指令应包含：要修改的文件、要实现的功能、期望的结果")

        decision = input("\n请输入具体的执行指令：")
        return decision
