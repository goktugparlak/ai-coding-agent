from app.tools import test_tools


def test_run_tests_success(tmp_path, monkeypatch):
    monkeypatch.setattr(
        test_tools,
        "WORKSPACE_DIR",
        tmp_path.resolve(),
    )

    (tmp_path / "test_example.py").write_text(
        "def test_example():\n    assert 2 + 2 == 4\n",
        encoding="utf-8",
    )

    result = test_tools.run_tests()

    assert "Tests passed." in result
    assert "1 passed" in result


def test_run_tests_failure(tmp_path, monkeypatch):
    monkeypatch.setattr(
        test_tools,
        "WORKSPACE_DIR",
        tmp_path.resolve(),
    )

    (tmp_path / "test_example.py").write_text(
        "def test_example():\n    assert 2 + 2 == 10\n",
        encoding="utf-8",
    )

    result = test_tools.run_tests()

    assert "Tests failed." in result
    assert "1 failed" in result
