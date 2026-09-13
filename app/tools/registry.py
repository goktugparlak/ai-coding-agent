from app.tools import file_tools, terminal_tools, test_tools


class ToolRegistry:
    def execute(self, tool_name: str, arguments: dict) -> object:
        if tool_name == "list_files":
            return file_tools.list_files()

        if tool_name == "read_file":
            return file_tools.read_file(arguments["filename"])

        if tool_name == "write_file":
            return file_tools.write_file(
                arguments["filename"],
                arguments["content"],
            )

        if tool_name == "run_python":
            return terminal_tools.run_python(arguments["filename"])

        if tool_name == "run_tests":
            return test_tools.run_tests()

        raise ValueError(f"Unknown tool: {tool_name}")
