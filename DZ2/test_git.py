import pytest
import json
from unittest.mock import MagicMock, mock_open, patch
from git_dep import (
    load_config,
    get_commits_from_local_repo,
    generate_mermaid_code,
    save_to_file,
    generate_graph_image,
)

# Тест для load_config
def test_load_config():
    config_data = {
        "commit_date": "2024-11-01",
        "output_file_path": "output.md",
        "repository_path": "test_repo",
        "visualization_program_path": "graphviz_path",
    }
    config_json = json.dumps(config_data)

    with patch("builtins.open", mock_open(read_data=config_json)):
        config = load_config("config.json")
        assert config["commit_date"] == "2024-11-01"
        assert config["output_file_path"] == "output.md"
        assert config["repository_path"] == "test_repo"
        assert config["visualization_program_path"] == "graphviz_path"

# Тест для get_commits_from_local_repo
def test_get_commits_from_local_repo():
    mock_repo = MagicMock()
    mock_commit = MagicMock()
    mock_commit.hexsha = "abc123"
    mock_commit.message = "Initial commit"
    mock_commit.parents = []

    mock_repo.iter_commits.return_value = [mock_commit]

    with patch("git.Repo", return_value=mock_repo):
        commits = get_commits_from_local_repo("test_repo", "2024-11-01")
        assert len(commits) == 1
        assert commits[0].hexsha == "abc123"
        assert commits[0].message == "Initial commit"

# Тест для generate_mermaid_code
def test_generate_mermaid_code():
    mock_commit_1 = MagicMock(hexsha="abc123", message="Initial commit", parents=[])
    mock_commit_2 = MagicMock(hexsha="def456", message="Second commit", parents=[mock_commit_1])

    commits = [mock_commit_1, mock_commit_2]
    mermaid_code = generate_mermaid_code(commits)

    expected_code = (
        "graph TD\n"
        '    "abc123 (Initial commit)" [shape=ellipse];\n'
        '    "def456 (Second commit)" --> "abc123";\n'
    )
    assert mermaid_code == expected_code

# Тест для save_to_file
def test_save_to_file():
    mermaid_code = "graph TD\n    A --> B\n"
    with patch("builtins.open", mock_open()) as mock_file:
        save_to_file(mermaid_code, "output.md")
        mock_file.assert_called_once_with("output.md", "w", encoding="utf-8")
        mock_file().write.assert_called_once_with(mermaid_code)

# Тест для generate_graph_image
def test_generate_graph_image():
    mermaid_code = "graph TD\n    A --> B\n"
    output_image_path = "output.png"

    with patch("graphviz.Digraph.render") as mock_render:
        generate_graph_image(mermaid_code, output_image_path)
        mock_render.assert_called_once_with(output_image_path, cleanup=True)
