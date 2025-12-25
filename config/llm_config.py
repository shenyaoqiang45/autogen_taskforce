# 基础配置
base_config = {
    "temperature": 0.2
}

# 模型配置
llm_config = {
    "config_list": [
        {
            "model": "deepseek-chat",
            "api_key": "sk-f71caf6ed44145b683fcd816b5171b4a",
            "base_url": "https://api.deepseek.com/v1"
        }
    ],
    **base_config
}

# Planner: DeepSeek
planner_config = {
    "config_list": [
        {
            "model": "deepseek-chat",
            "api_key": "sk-f71caf6ed44145b683fcd816b5171b4a",
            "base_url": "https://api.deepseek.com/v1"
        }
    ],
    **base_config
}

# Executor: DeepSeek
executor_config = {
    "config_list": [
        {
            "model": "deepseek-chat",
            "api_key": "sk-f71caf6ed44145b683fcd816b5171b4a",
            "base_url": "https://api.deepseek.com/v1"
        }
    ],
    **base_config
}

red_team_config = {
    "config_list": [
        {
            "model": "deepseek-chat",
            "api_key": "sk-f71caf6ed44145b683fcd816b5171b4a",
            "base_url": "https://api.deepseek.com/v1"
        }
    ],
    **base_config
}

auditor_config = {
    "config_list": [
        {
            "model": "deepseek-chat",
            "api_key": "sk-f71caf6ed44145b683fcd816b5171b4a",
            "base_url": "https://api.deepseek.com/v1"
        }
    ],
    **base_config
}
