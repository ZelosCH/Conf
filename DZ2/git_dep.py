import argparse
import json
import subprocess
from datetime import datetime

def parse_config_file(config_file_path):
    with open(config_file_path, 'r') as f:
        config = json.load(f)
    return config

def analyze_git_repository(repository_path, commit_date_limit):
    cmd = f'git -C {repository_path} log --pretty=format:"%h %P %ct" --date=iso --since={commit_date_limit}'
    output = subprocess.check_output(cmd, shell=True, text=True)
    lines = output.strip().split('\n')
    graph = {}
    for line in lines:
        commit_hash, parents, timestamp = line.split(' ', 2)
        parents = parents.split()
        graph[commit_hash] = parents
    return graph

def convert_graph_to_mermaid(graph):
    mermaid_code = 'graph TD\n'
    for node, edges in graph.items():
        for edge in edges:
            mermaid_code += f'    "{node}" --> "{edge}"\n'
    return mermaid_code

def main():
    parser = argparse.ArgumentParser(description='Visualize git commit dependencies')
    parser.add_argument('config_file', type=str, help='Path to the configuration file')
    args = parser.parse_args()
    config = parse_config_file(args.config_file)
    graph = analyze_git_repository(config['repository_path'], config['commit_date_limit'])
    mermaid_code = convert_graph_to_mermaid(graph)
    print(mermaid_code)
    with open(config['output_file_path'], 'w') as f:
        f.write(mermaid_code)

if __name__ == '__main__':
    main()
