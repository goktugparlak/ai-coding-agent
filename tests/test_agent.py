from app.agent import CodingAgent
from app.database import HistoryStore
from app.providers.mock_provider import MockProvider
from app.tools import file_tools


def make_agent(tmp_path):

    return CodingAgent(
        provider=MockProvider(),
        history=HistoryStore(
            tmp_path / "history.db"
        ),
    )


def test_agent_lists_files(
    tmp_path,
    monkeypatch,
):

    workspace = tmp_path / "workspace"
    workspace.mkdir()

    monkeypatch.setattr(
        file_tools,
        "WORKSPACE_DIR",
        workspace,
    )

    file_tools.write_file(
        "hello.py",
        'print("Hello")',
    )

    agent = make_agent(tmp_path)

    result = agent.run(
        "list files"
    )

    assert "hello.py" in result


def test_agent_reads_file(
    tmp_path,
    monkeypatch,
):

    workspace = tmp_path / "workspace"
    workspace.mkdir()

    monkeypatch.setattr(
        file_tools,
        "WORKSPACE_DIR",
        workspace,
    )

    file_tools.write_file(
        "hello.py",
        'print("Hello")',
    )

    agent = make_agent(tmp_path)

    result = agent.run(
        "read hello.py"
    )

    assert 'print("Hello")' in result


def test_agent_unknown_command(tmp_path):

    agent = make_agent(tmp_path)

    result = agent.run(
        "do something magical"
    )

    assert "I do not understand" in result


def test_agent_history(tmp_path):

    agent = make_agent(tmp_path)

    agent.run("help")

    result = agent.run(
        "history"
    )

    assert "Recent history:" in result
    assert "help" in result