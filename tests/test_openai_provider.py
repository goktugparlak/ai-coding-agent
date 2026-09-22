from types import SimpleNamespace

from app.providers.openai_provider import OpenAIProvider


class FakeResponses:
    def __init__(self):
        self.calls = 0

    def create(self, **kwargs):

        self.calls += 1

        if self.calls == 1:

            tool_call = SimpleNamespace(
                type="function_call",
                name="list_files",
                arguments="{}",
                call_id="call_123",
            )

            return SimpleNamespace(
                output=[tool_call],
                output_text="",
            )

        return SimpleNamespace(
            output=[],
            output_text=(
                "I inspected the workspace files."
            ),
        )


class FakeClient:
    def __init__(self):
        self.responses = FakeResponses()


def test_openai_provider_executes_tool():

    executed = []

    def execute_tool(
        tool_name,
        arguments,
    ):

        executed.append(
            (
                tool_name,
                arguments,
            )
        )

        return [
            "calculator.py",
            "tests/test_calculator.py",
        ]

    provider = OpenAIProvider(
        client=FakeClient(),
        model="test-model",
    )

    result = provider.run(
        "List the project files.",
        execute_tool,
    )

    assert executed == [
        (
            "list_files",
            {},
        )
    ]

    assert (
        "I inspected the workspace files."
        in result
    )

    assert (
        "Tools used: list_files"
        in result
    )