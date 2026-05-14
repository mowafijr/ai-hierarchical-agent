import json
from pathlib import Path
from llm.client import LLMClient
from core.planner import Planner
from core.executor import Executor
from core.replanner import Replanner
from core.agent import Agent
from tools.registry import TOOLS, get_tool_schemas
from memory.memory_store import load_memory

CONFIG_PATH = Path("config/settings.json")

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def main():
    config = load_config()
    memory = load_memory()
    llm = LLMClient(config)
    tool_schemas = get_tool_schemas()
    planner = Planner(llm, tool_schemas)
    executor = Executor(TOOLS)
    replanner = Replanner(llm, tool_schemas)
    agent = Agent(llm, planner, executor, memory, replanner=replanner, max_subgoal_retries=2)

    print("\n🤖 Hierarchical Agent with Surgical Replanning")
    print("Type /exit to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "/exit":
            break
        response = agent.run(user_input)
        print(f"AI: {response}\n")

if __name__ == "__main__":
    main()