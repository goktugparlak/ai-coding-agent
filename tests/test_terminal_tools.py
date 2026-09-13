from app.tools import file_tools, terminal_tools


def test_run_python(tmp_path, monkeypatch):
    monkeypatch.setattr(
        file_tools,
        "WORKSPACE_DIR",
        tmp_path.resolve(),
    )
    monkeypatch.setattr(
        terminal_tools,
        "WORKSPACE_DIR",
        tmp_path.resolve(),
    )

    script = tmp_path / "hello.py"
    script.write_text(
        'print("Hello from test")',
        encoding="utf-8",
    )

    result = terminal_tools.run_python("hello.py")

    assert result == "Hello from test"


def test_run_python_error(tmp_path, monkeypatch):
    monkeypatch.setattr(
        file_tools,
        "WORKSPACE_DIR",
        tmp_path.resolve(),
    )
    monkeypatch.setattr(
        terminal_tools,
        "WORKSPACE_DIR",
        tmp_path.resolve(),
    )

    script = tmp_path / "broken.py"
    script.write_text(
        "print(undefined_variable)",
        encoding="utf-8",
    )

    result = terminal_tools.run_python("broken.py")

    assert "NameError" in result
