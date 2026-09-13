from app.tools import file_tools


def test_write_and_read_file(tmp_path, monkeypatch):
    monkeypatch.setattr(
        file_tools,
        "WORKSPACE_DIR",
        tmp_path.resolve(),
    )

    result = file_tools.write_file(
        "hello.py",
        'print("Hello")',
    )
    content = file_tools.read_file("hello.py")

    assert result == "Successfully wrote to 'hello.py'."
    assert content == 'print("Hello")'


def test_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(
        file_tools,
        "WORKSPACE_DIR",
        tmp_path.resolve(),
    )

    assert (
        file_tools.read_file("missing.py")
        == "Error: 'missing.py' was not found."
    )


def test_path_traversal_is_blocked(tmp_path, monkeypatch):
    monkeypatch.setattr(
        file_tools,
        "WORKSPACE_DIR",
        tmp_path.resolve(),
    )

    result = file_tools.write_file(
        "../dangerous.py",
        "dangerous",
    )

    assert result == "Error: Path is outside the workspace."


def test_list_files(tmp_path, monkeypatch):
    monkeypatch.setattr(
        file_tools,
        "WORKSPACE_DIR",
        tmp_path.resolve(),
    )

    file_tools.write_file("one.py", "hello")
    file_tools.write_file("folder/two.py", "hello")

    assert file_tools.list_files() == [
        "folder/two.py",
        "one.py",
    ]
