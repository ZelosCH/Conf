import os
import tempfile
import unittest
from unittest.mock import patch
import shutil
import csv
import datetime


# Вспомогательные функции из оболочки
def list_files():
    """Список файлов и директорий в текущей директории."""
    return os.listdir()


def change_directory(path, temp_dir):
    """Смена директории."""
    if not path:
        os.chdir(temp_dir)
    elif os.path.isabs(path):
        os.chdir(path)
    else:
        os.chdir(os.path.join(os.getcwd(), path))
    return os.getcwd()


def move_file(src, dest):
    """Перемещение файла."""
    shutil.move(src, dest)


def tail_file(file_path, lines=10):
    """Чтение последних строк файла."""
    with open(file_path, 'r') as f:
        return ''.join(f.readlines()[-lines:])


def log_action(log_path, action):
    """Логирование действий."""
    with open(log_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.datetime.now(), action])


def get_calendar(year=None, month=None):
    """Получение календаря на месяц."""
    import calendar
    if year and month:
        return calendar.month(int(year), int(month))
    now = datetime.datetime.now()
    return calendar.month(now.year, now.month)


class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        """Настройка окружения для тестов."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test.txt')
        self.log_file = os.path.join(self.temp_dir, 'log.csv')

        with open(self.test_file, 'w') as f:
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")

        self.start_dir = os.getcwd()
        os.chdir(self.temp_dir)

    def tearDown(self):
        """Очистка после тестов."""
        os.chdir(self.start_dir)
        shutil.rmtree(self.temp_dir)

    def test_list_files(self):
        """Тестирование вывода списка файлов."""
        files = list_files()
        self.assertIn('test.txt', files)

    def test_change_directory(self):
        """Тестирование смены директории."""
        subdir = os.path.join(self.temp_dir, 'subdir')
        os.makedirs(subdir)
        new_dir = change_directory('subdir', self.temp_dir)
        self.assertEqual(new_dir, subdir)

    def test_move_file(self):
        """Тестирование перемещения файла."""
        dest_file = os.path.join(self.temp_dir, 'moved_test.txt')
        move_file('test.txt', dest_file)
        self.assertTrue(os.path.exists(dest_file))
        self.assertFalse(os.path.exists(self.test_file))

    def test_tail_file(self):
        """Тестирование чтения последних строк файла."""
        content = tail_file(self.test_file, lines=3)
        self.assertEqual(content, "Line 3\nLine 4\nLine 5\n")

    def test_log_action(self):
        """Тестирование логирования действий."""
        log_action(self.log_file, 'test_action')
        with open(self.log_file, 'r') as f:
            logs = list(csv.reader(f))
        self.assertEqual(len(logs), 1)
        self.assertIn('test_action', logs[0])

    def test_get_calendar(self):
        """Тестирование получения календаря."""
        cal = get_calendar(2023, 11)
        self.assertIn('November 2023', cal)


if __name__ == '__main__':
    unittest.main()
