# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `autogen_taskforce` - a human-in-the-loop multi-agent decision system built on AutoGen. The system follows the "AI Special Forces" design principles to reduce fatal error probability in high-value complex decisions through heterogeneous model configuration.

**Core Philosophy**: Maximize system capability through heterogeneous cognition, forced conflict, and human adjudication, rather than optimizing individual model performance.

## Key Commands

### Setup and Installation
```bash
# Activate Conda environment (required)
conda activate autogen

# Install dependencies
pip install autogen-agentchat autogen-ext
```

### Running the System
```bash
# Main execution flow
python run.py

# View logs via CLI
python view_logs.py

# View logs via web UI (port 8080)
python log_viewer.py
```

### Configuration
- API keys must be configured in `config/llm_config.py` (copy from `llm_config.example.py`)
- The file is gitignored for security
- Uses two API providers: WhatAI (for Claude/GPT) and DeepSeek (for DeepSeek-R1)

## Architecture

### Multi-Agent System
The system implements a fixed workflow sequence with strict role boundaries:

1. **Planner** (Claude 4.5, temp 0.3): Creates 2 executable plans from strategic goals
2. **Red Team** (DeepSeek-R1, temp 0.1): Attacks plans to find vulnerabilities and risks
3. **Peer Analyst** (GPT-4o, temp 0.4): Provides constructive analysis and value assessment
4. **Human Commander**: Makes final decision via `commander.py`
5. **Executor** (GPT-5.2, temp 0.2): Executes selected plan with retry mechanism (max 3 retries)
6. **Auditor** (DeepSeek-R1, temp 0.0): Zero-temperature strict audit of execution results

### Key Design Principles
- **Human has ultimate decision authority**: AI agents are "combat units" not decision-makers
- **Heterogeneous model configuration**: Different models for different roles to prevent systemic cognitive blind spots
- **Fixed workflow sequence**: Cannot skip steps or allow free dialogue between agents
- **Strict role boundaries**: Agents cannot exceed their designated responsibilities
- **Forced conflict**: Red Team must attack plans to expose potential problems
- **Zero-tolerance audit**: Auditor uses temperature 0.0 for strict quality control

### System Capability Formula
```
System Capability =
  Problem Space Coverage × Failure Mode Discovery Probability
  × Error Blocking Probability × Stability per Unit Cost
```

### Agent Implementation Pattern
All agents in `agents/` directory follow the same pattern:
1. Import `AssistantAgent` from `autogen_agentchat.agents`
2. Import `OpenAIChatCompletionClient` from `autogen_ext.models.openai`
3. Load specific configuration from `config.llm_config`
4. Create `model_client` with model-specific settings
5. Define `AssistantAgent` with name, description, and model_client

### Logging System
- JSON logs saved in `logs/` directory with timestamped filenames (`run_YYYYMMDD_HHMMSS.json`)
- Each log contains: mission, model configurations, agent outputs with timestamps
- Logs track which model was used for each step
- Two viewing options: CLI (`view_logs.py`) and web UI (`log_viewer.py` on port 8080)

## Important Files

### Core Execution
- `run.py`: Main orchestrator that sequences agent interactions
- `commander.py`: Human-in-the-loop interface for decision making

### Agent Implementations (`agents/` directory)
- `planner.py`: Tactical planning agent (must create 2 executable plans)
- `red_team.py`: Risk assessment agent (must attack plans, not propose alternatives)
- `peer_analyst.py`: Constructive analysis agent (must provide value assessment)
- `executor.py`: Execution agent with retry mechanism (max 3 retries)
- `auditor.py`: Strict audit agent (temperature 0.0)

### Configuration
- `config/llm_config.py`: Live LLM configuration with API keys (gitignored)
- `config/llm_config.example.py`: Template for configuration

### Documentation
- `README.md`: Comprehensive user guide and technical documentation
- `AI 特种部队军规.md`: Design principles and operational rules ("AI Special Forces Rules")
- `配置最大系统能力.md`: Theoretical framework for maximizing system capability

## Development Notes

### Model Selection Rationale
- **Claude 4.5** for Planner: Best for strategic thinking and creative solutions
- **DeepSeek-R1** for Red Team/Auditor: Best for strict reasoning and counterexample construction
- **GPT-4o** for Peer Analyst: Best for constructive analysis and value assessment
- **GPT-5.2** for Executor: Best for engineering execution and tool success rate

### Error Handling
- Executor has retry mechanism with up to 3 attempts
- When Executor fails with `[EXECUTOR_ERROR:` marker, Commander provides clarification
- Auditor provides final quality check with zero-temperature strictness

### Security Considerations
- API keys are in `.gitignore`-protected configuration file
- No hardcoded secrets in version control
- Human maintains control over all critical decisions

### Testing and Experimentation
- Use `log_viewer.py` to analyze model performance across different roles
- Modify `config/llm_config.py` to test different model combinations
- Compare heterogeneous vs homogeneous model configurations
- Analyze Red Team and Auditor veto rates for error discovery effectiveness

## When Modifying Code

1. **Maintain role boundaries**: Agents should not exceed their designated responsibilities
2. **Preserve heterogeneous configuration**: Changing models should follow the design principles in `配置最大系统能力.md`
3. **Keep human in the loop**: Never automate the Commander's decision-making role
4. **Maintain logging**: All agent outputs should be logged with model information
5. **Follow agent patterns**: New agents should follow the same implementation pattern as existing ones