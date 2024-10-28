import os
import pytest
import datetime
from shell import shell

@pytest.fixture
def temp_dir(tmp_path):
    # Создание временной директории
    temp_dir = tmp_path / "temp"
    temp_dir.mkdir()
    return temp_dir

def test_ls_command(temp_dir, capsys):
    # Создание тестовых файлов в временной директории
    test_file1 = temp_dir / "file1.txt"
    test_file2 = temp_dir / "file2.txt"
    test_file1.touch()
    test_file2.touch()

    # Смена текущего рабочего каталога на временную директорию
    os.chdir(temp_dir)

    # Создание объектов для вывода результатов и обновления текущего каталога
    output_text = []
    current_dir = str(temp_dir)

    # Выполнение команды ls
    shell(["ls"], output_text, current_dir)

    # Проверка вывода команды ls
    assert "file1.txt" in "\n".join(output_text)
    assert "file2.txt" in "\n".join(output_text)


def test_mv_command(temp_dir, capsys):
    # Создание тестового файла в временной директории
    test_file = temp_dir / "file.txt"
    test_file.touch()

    # Смена текущего рабочего каталога на временную директорию
    os.chdir(temp_dir)

    # Создание объектов для вывода результатов и обновления текущего каталога
    output_text = []
    current_dir = str(temp_dir)

    # Выполнение команды mv
    new_file_path = temp_dir / "new_file.txt"
    shell([f"mv {test_file} {new_file_path}"], output_text, current_dir)

    # Проверка перемещения файла
    assert not test_file.exists()
    assert new_file_path.exists()

def test_tail_command(temp_dir, capsys):
    # Создание тестового файла в временной директории
    test_file = temp_dir / "file.txt"
    with open(test_file, "w") as f:
        f.write("line1\nline2\nline3\nline4\nline5\nline6\nline7\nline8\nline9\nline10\nline11")

    # Смена текущего рабочего каталога на временную директорию
    os.chdir(temp_dir)

    # Создание объектов для вывода результатов и обновления текущего каталога
    output_text = []
    current_dir = str(temp_dir)

    # Выполнение команды tail
    shell([f"tail {test_file}"], output_text, current_dir)

    # Проверка вывода команды tail
    assert "line7" in "\n".join(output_text)
    assert "line11" in "\n".join(output_text)

def test_cal_command(capsys):
    # Создание объектов для вывода результатов и обновления текущего каталога
    output_text = []
    current_dir = os.getcwd()

    # Выполнение команды cal
    shell(["cal"], output_text, current_dir)

    # Проверка вывода команды cal
    assert datetime.datetime.now().strftime("%B %Y") in "\n".join(output_text)

def test_exit_command():
    # Создание объектов для вывода результатов и обновления текущего каталога
    output_text = []
    current_dir = os.getcwd()

    # Выполнение команды exit
    with pytest.raises(SystemExit):
        shell(["exit"], output_text, current_dir)
