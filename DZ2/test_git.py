import json
import subprocess
import pytest
from git_dep import parse_config_file, analyze_git_repository, convert_graph_to_mermaid

@pytest.fixture
def config():
    config_data = {
        "repository_path": "D:\\DZ2\\cpython",
        "commit_date_limit": "2024-11-01",
        "output_file_path": "D:\\DZ2\\output_file_path.md"
    }
    with open("test_config.json", "w") as f:
        json.dump(config_data, f)
    return config_data

def test_parse_config_file(config):
    parsed_config = parse_config_file("test_config.json")
    assert parsed_config == config

def test_analyze_git_repository(config):
    graph = analyze_git_repository(config["repository_path"], config["commit_date_limit"])
    assert isinstance(graph, dict)
    for node, edges in graph.items():
        assert isinstance(node, str)
        assert isinstance(edges, list)
        for edge in edges:
            assert isinstance(edge, str)

def test_convert_graph_to_mermaid(config):
    graph = {
        "commit1": ["commit2", "commit3"],
        "commit2": ["commit3"],
        "commit3": []
    }
    mermaid_code = convert_graph_to_mermaid(graph)
    assert isinstance(mermaid_code, str)
    assert "graph TD" in mermaid_code
    assert '"commit1" --> "commit2"' in mermaid_code
    assert '"commit1" --> "commit3"' in mermaid_code
    assert '"commit2" --> "commit3"' in mermaid_code
