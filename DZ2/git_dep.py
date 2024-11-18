import os
import subprocess
import json


# Чтение конфигурационного файла
def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Получение коммитов с локального репозитория через git log
def get_commits_from_cache(repo_path, commit_date):
    try:
        log_format = "--pretty=format:%H;%P;%s"  # Шаблон: hash;parents;message
        git_command = [
            "git",
            "-C",
            repo_path,
            "log",
            f"--since={commit_date}",
            log_format,
        ]
        result = subprocess.run(
            git_command, capture_output=True, text=True, check=True
        )

        commits = []
        for line in result.stdout.strip().split("\n"):
            parts = line.split(";")
            commit = {
                "hash": parts[0],
                "parents": parts[1].split() if len(parts) > 1 and parts[1] else [],
                "message": parts[2] if len(parts) > 2 else "",
            }
            commits.append(commit)
        return commits

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды git: {e.stderr}")
        return []


# Рекурсивное получение всех зависимостей для коммита
def get_all_dependencies(commit, commits_map):
    dependencies = set(commit["parents"])  # Начинаем с родительских коммитов

    for parent_hash in commit["parents"]:
        parent_commit = commits_map.get(parent_hash)
        if parent_commit:
            dependencies.update(
                get_all_dependencies(parent_commit, commits_map))  # Рекурсивно добавляем все зависимости

    return dependencies


# Генерация кода для визуализации зависимостей в формате Mermaid
def generate_mermaid_tree(commits):
    mermaid_code = "graph TD\n"  # Начинаем с директивы для графа Mermaid
    commits_map = {commit["hash"]: commit for commit in commits}  # Создаем словарь для быстрого доступа к коммитам

    for commit in commits:
        sanitized_message = sanitize_string(commit["message"].replace("\n", " ").replace('"', "'"))
        dependencies = get_all_dependencies(commit, commits_map)

        for parent in dependencies:
            if parent != commit["hash"]:  # Чтобы не создавать циклические зависимости с самим собой
                mermaid_code += f'    {commit["hash"]} --> {parent};\n'

        # Для корневых коммитов используем другой стиль
        mermaid_code += f'    {commit["hash"]}["{sanitized_message}"];\n'

    return mermaid_code


# Очистка строки от недопустимых символов для использования в именах коммитов
def sanitize_string(text):
    text = text.replace("-", "_")
    return "".join(
        e for e in text if e.isalnum() or e.isspace() or e in ("_", ".", ":", ",", "'")
    )


# Сохранение зависимостей в файл (в формате Markdown для Mermaid)
def save_to_file(mermaid_code, output_file_path):
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(mermaid_code)


def main():
    # Путь к конфигурационному файлу
    config_path = "config.json"

    # Загружаем конфигурацию
    config = load_config(config_path)

    commit_date = config["commit_date"]
    output_file_path = config["output_file_path"]
    repository_path = config["repository_path"]

    # Получаем коммиты из локального репозитория
    commits = get_commits_from_cache(repository_path, commit_date)

    # Генерация Mermaid-кода
    mermaid_code = generate_mermaid_tree(commits)

    # Вывод Mermaid-кода в консоль
    print("\nСгенерированный Mermaid-код:")
    print(mermaid_code)

    # Сохраняем код в файл .md
    save_to_file(mermaid_code, output_file_path)
    print(f"\nГраф зависимостей сохранен в файл: {output_file_path}")


if __name__ == "__main__":
    main()
