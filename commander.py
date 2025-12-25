class Commander:
    def __init__(self):
        pass

    def decide(self, planner_output, red_team_output):
        print("\n====== PLANNER ======")
        print(planner_output)

        print("\n====== RED TEAM ======")
        print(red_team_output)

        decision = input("\n请输入你的命令（例如：执行方案 B）：")
        return decision
