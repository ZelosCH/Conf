import pytest
import os
import json
from git_dep import (
    load_config,
    get_commits_from_cache,
    get_all_dependencies,
    generate_mermaid_tree,
    sanitize_string,
    save_to_file,
)


# Мок-данные для тестов
MOCK_COMMITS = [
    {"hash": "a1b2c3", "parents": ["d4e5f6"], "message": "Initial commit"},
    {"hash": "d4e5f6", "parents": [], "message": "Base commit"},
    {"hash": "g7h8i9", "parents": ["a1b2c3"], "message": "Feature added"},
]


@pytest.fixture
def mock_config(tmp_path):
    config_path = tmp_path / "config.json"
    config_data = {
        "commit_date": "2024-01-01",
        "output_file_path": str(tmp_path / "output.md"),
        "repository_path": "/mock/repo/path",
    }
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f)
    return config_path, config_data


def test_load_config(mock_config):
    config_path, expected_config = mock_config
    config = load_config(config_path)
    assert config == expected_config


def test_sanitize_string():
    raw_string = "Test-string, with special:chars!"
    sanitized = sanitize_string(raw_string)
    assert sanitized == "Test_string, with special:chars"


def test_get_commits_from_cache(mocker):
    mock_subprocess = mocker.patch("subprocess.run")
    mock_subprocess.return_value.stdout = "a1b2c3;d4e5f6;Initial commit\nd4e5f6;;Base commit\n"
    repo_path = "/mock/repo/path"
    commit_date = "2024-01-01"

    commits = get_commits_from_cache(repo_path, commit_date)
    expected = [
        {"hash": "a1b2c3", "parents": ["d4e5f6"], "message": "Initial commit"},
        {"hash": "d4e5f6", "parents": [], "message": "Base commit"},
    ]
    assert commits == expected
    mock_subprocess.assert_called_once_with(
        [
            "git",
            "-C",
            repo_path,
            "log",
            "--since=2024-01-01",
            "--pretty=format:%H;%P;%s",
        ],
        capture_output=True,
        text=True,
        check=True,
    )


def test_get_all_dependencies():
    commits_map = {commit["hash"]: commit for commit in MOCK_COMMITS}
    dependencies = get_all_dependencies(MOCK_COMMITS[0], commits_map)
    assert dependencies == {"d4e5f6"}


def test_generate_mermaid_tree():
    mermaid_code = generate_mermaid_tree(MOCK_COMMITS)
    expected_lines = [
        "graph TD",
        '    a1b2c3["Initial commit"];',
        '    d4e5f6["Base commit"];',
        '    g7h8i9["Feature added"];',
        "    a1b2c3 --> d4e5f6;",
        "    g7h8i9 --> a1b2c3;",
    ]
    for line in expected_lines:
        assert line in mermaid_code


def test_save_to_file(tmp_path):
    mermaid_code = "graph TD\n    a1b2c3 --> d4e5f6;"
    output_file_path = tmp_path / "output.md"
    save_to_file(mermaid_code, output_file_path)
    assert output_file_path.exists()
    with open(output_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == mermaid_code
