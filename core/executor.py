class Executor:
    def __init__(self, tool_registry: dict):
        self.tools = tool_registry

    def run(self, tool_name: str, args: dict) -> str:
        if tool_name not in self.tools:
            return f"Unknown tool: {tool_name}"
        tool = self.tools[tool_name]
        func = tool["func"]
        schema = tool.get("schema", {})
        required = schema.get("required", [])
        for req in required:
            if req not in args:
                return f"Missing argument: {req}"
        try:
            return func(**args)
        except Exception as e:
            return f"Tool error: {e}"