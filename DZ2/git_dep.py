import os
import subprocess
import json
import git
from graphviz import Digraph


# Чтение конфигурационного файла
def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Получение коммитов с локального репозитория
def get_commits_from_local_repo(repo_path, commit_date):
    # Открытие локального репозитория
    repo = git.Repo(repo_path)

    # Получаем основную ветку
    main_branch = repo.active_branch.name

    # Получаем коммиты до указанной даты
    commits = list(repo.iter_commits(main_branch, since=commit_date))

    return commits




# Генерация кода для визуализации зависимостей (Mermaid)
def generate_mermaid_code(commits):
    mermaid_code = "graph TD\n"
    for commit in commits:
        if not commit.hexsha:  # Проверяем, что у коммита есть hexsha
            continue
        message = commit.message.replace("\n", " ").replace('"', "'")  # Убираем кавычки и переносы строк
        sanitized_message = sanitize_string(message)
        if commit.parents:
            for parent in commit.parents:
                if parent.hexsha:  # Проверяем, что у родителя есть hexsha
                    mermaid_code += f'    "{commit.hexsha} ({sanitized_message})" --> "{parent.hexsha}";\n'
        else:
            mermaid_code += f'    "{commit.hexsha} ({sanitized_message})" [shape=ellipse];\n'  # Корневой коммит

    return mermaid_code




# Очистка строки от недопустимых символов
def sanitize_string(text):
    # Заменяем небезопасные символы на безопасные
    text = text.replace('-', '_')  # Заменяем дефисы на подчеркивания
    return ''.join(e for e in text if e.isalnum() or e.isspace() or e in ('_', '.', ':', ',', "'"))


# Сохранение зависимостей в файл
def save_to_file(mermaid_code, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(mermaid_code)


# Генерация изображения графа с помощью Graphviz
# Генерация изображения графа с помощью Graphviz
def generate_graph_image(mermaid_code, output_image_path):
    # Конвертируем Mermaid в Graphviz
    dot_code = mermaid_to_dot(mermaid_code)

    # Создаем объект графа и добавляем DOT-код
    graph = Digraph(format='png')
    graph.attr(dpi='300')  # Можно настроить параметры, например, разрешение
    graph.node_attr['shape'] = 'box'  # Пример настройки внешнего вида
    graph.attr(nodesep='0.5')  # Сжимаем узлы, чтобы избежать пустых пробелов

    # Добавляем связи из DOT-кода
    for line in dot_code.splitlines():
        if '->' in line:
            parts = line.replace(';', '').split('->')
            if len(parts) == 2:
                graph.edge(parts[0].strip().strip('"'), parts[1].strip().strip('"'))

    # Генерируем изображение
    try:
        graph.render(output_image_path, cleanup=True)
        print(f"Изображение графа сохранено в файл: {output_image_path}")
    except Exception as e:
        print(f"Ошибка при генерации изображения: {e}")


# Конвертация Mermaid-кода в формат dot (для Graphviz)
def mermaid_to_dot(mermaid_code):
    # Простой перевод из Mermaid в dot (по сути, это преобразование для графа направленных зависимостей)
    dot_code = "digraph G {\n"
    for line in mermaid_code.split("\n")[1:]:
        if line.strip():
            parts = line.strip().split(" --> ")
            if len(parts) == 2:
                # Обрабатываем строки и убираем лишние символы
                dot_code += f'    "{sanitize_string(parts[0].strip())}" -> "{sanitize_string(parts[1].strip())}";\n'
    dot_code += "}"

    return dot_code


def main():
    # Путь к конфигурационному файлу
    config_path = 'config.json'

    # Загружаем конфигурацию
    config = load_config(config_path)

    commit_date = config["commit_date"]
    output_file_path = config["output_file_path"]
    repository_path = config["repository_path"]
    visualization_program_path = config["visualization_program_path"]

    # Получаем коммиты из локального репозитория
    commits = get_commits_from_local_repo(repository_path, commit_date)

    # Генерация Mermaid-кода
    mermaid_code = generate_mermaid_code(commits)

    # Вывод Mermaid-кода в консоль
    print("\nСгенерированный Mermaid-код:")
    print(mermaid_code)

    # Сохраняем код в файл
    save_to_file(mermaid_code, output_file_path)
    print(f"\nГраф зависимостей сохранен в файл: {output_file_path}")

    # Генерация изображения графа
    output_image_path = output_file_path.replace(".md", ".png")
    generate_graph_image(mermaid_code, output_image_path)



if __name__ == "__main__":
    main()
