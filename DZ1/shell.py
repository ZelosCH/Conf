import os
import sys
import shutil
import csv
import datetime
import zipfile
import configparser
import tkinter as tk
from tkinter import filedialog
import tempfile
import atexit
import ttkthemes

# Чтение конфигурационного файла
config = configparser.ConfigParser()
config.read('config.ini')
computer_name = config['DEFAULT']['computer_name']
vfs_path = config['DEFAULT']['vfs_path']
log_path = config['DEFAULT']['log_path']

# Создание временной директории
temp_dir = tempfile.mkdtemp()

# Извлечение виртуальной файловой системы из zip-файла
with zipfile.ZipFile(vfs_path, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

# Смена текущего рабочего каталога на временную директорию
os.chdir(temp_dir)

# Регистрация функции для очистки временной директории
atexit.register(lambda: shutil.rmtree(temp_dir))

# Функция для записи действий пользователя в лог-файл
def log_action(action):
    with open(log_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.datetime.now(), action])


# Функция для обработки пользовательского ввода и выполнения команд
def shell(commands=None):
    if commands is not None:
        for command in commands:
            # Очистка поля ввода команды
            command_entry.delete(0, tk.END)

            # Запись действия пользователя в лог-файл
            log_action(command)

            # Разбор команды
            args = command.split()

            # Выполнение команды
            try:
                if args[0] == 'ls':
                    files = os.listdir()
                    output_text.insert(tk.END, '\n'.join(files) + '\n')
                elif args[0] == 'cd':
                    if len(args) > 1:
                        path = os.path.normpath(args[1])
                        if os.path.isabs(path):
                            os.chdir(path)
                        else:
                            os.chdir(os.path.join(os.getcwd(), path))
                    else:
                        os.chdir(temp_dir)
                    current_dir_label.config(text=f'Current directory: {os.getcwd()}')
                elif args[0] == 'exit':
                    sys.exit()
                elif args[0] == 'mv':
                    shutil.move(args[1], args[2])
                elif args[0] == 'tail':
                    with open(args[1], 'r') as f:
                        lines = f.readlines()
                        output_text.insert(tk.END, ''.join(lines[-10:]) + '\n')
                elif args[0] == 'cal':
                    if len(args) == 1:
                        import calendar
                        output_text.insert(tk.END, calendar.month(datetime.datetime.now().year, datetime.datetime.now().month) + '\n')
                    elif len(args) == 3:
                        import calendar
                        output_text.insert(tk.END, calendar.month(int(args[1]), int(args[2])) + '\n')
                    else:
                        output_text.insert(tk.END, 'cal: invalid number of arguments\n')
                elif args[0] == 'pwd':
                    output_text.insert(tk.END, os.getcwd() + '\n')
                else:
                    output_text.insert(tk.END, f'Команда не найдена: {args[0]}\n')
            except Exception as e:
                output_text.insert(tk.END, f'Ошибка: {str(e)}\n')

            # Обновление заголовка окна
            root.title(f'Shell Emulator - {os.getlogin()}@{os.getcwd()}')
    else:
        # Получение пользовательского ввода
        command = command_entry.get()

        # Очистка поля ввода команды
        command_entry.delete(0, tk.END)

        # Запись действия пользователя в лог-файл
        log_action(command)

        # Разбор команды
        args = command.split()

        # Выполнение команды
        try:
            if args[0] == 'ls':
                files = os.listdir()
                output_text.insert(tk.END, '\n'.join(files) + '\n')
            elif args[0] == 'cd':
                if len(args) > 1:
                    path = os.path.normpath(args[1])
                    if os.path.isabs(path):
                        os.chdir(path)
                    else:
                        os.chdir(os.path.join(os.getcwd(), path))
                else:
                    os.chdir(temp_dir)
                current_dir_label.config(text=f'Current directory: {os.getcwd()}')
            elif args[0] == 'exit':
                sys.exit()
            elif args[0] == 'mv':
                shutil.move(args[1], args[2])
            elif args[0] == 'tail':
                with open(args[1], 'r') as f:
                    lines = f.readlines()
                    output_text.insert(tk.END, ''.join(lines[-10:]) + '\n')
            elif args[0] == 'cal':
                if len(args) == 1:
                    import calendar
                    output_text.insert(tk.END, calendar.month(datetime.datetime.now().year, datetime.datetime.now().month) + '\n')
                elif len(args) == 3:
                    import calendar
                    output_text.insert(tk.END, calendar.month(int(args[1]), int(args[2])) + '\n')
                else:
                    output_text.insert(tk.END, 'cal: invalid number of arguments\n')
            elif args[0] == 'pwd':
                output_text.insert(tk.END, os.getcwd() + '\n')
            else:
                output_text.insert(tk.END, f'Команда не найдена: {args[0]}\n')
        except Exception as e:
            output_text.insert(tk.END, f'Ошибка: {str(e)}\n')

        # Обновление заголовка окна
        root.title(f'Shell Emulator - {os.getlogin()}@{os.getcwd()}')

# Создание графического интерфейса
root = ttkthemes.ThemedTk()
root.set_theme('ubuntu')
root.title('Shell Emulator')

# Создание приветственного сообщения
welcome_message = f'Добро пожаловать, {os.getlogin()}!'
welcome_label = tk.Label(root, text=welcome_message)
welcome_label.pack()

# Создание поля ввода команды
command_entry = tk.Entry(root, width=50)
command_entry.pack()

# Создание кнопки для выполнения команды
command_button = tk.Button(root, text='Execute', command=shell)
command_button.pack()

# Создание текстового поля для вывода результатов
output_text = tk.Text(root, height=20, width=80)
output_text.pack()

# Создание метки для отображения текущего каталога
current_dir_label = tk.Label(root, text=f'Current directory: {os.getcwd()}')
current_dir_label.pack()

# Создание кнопки для выбора файла
file_button = tk.Button(root, text='Select File', command=lambda: os.chdir(filedialog.askdirectory()))
file_button.pack()
# Чтение команд из файла
with open('instructions.txt', 'r') as f:
    commands = f.readlines()

# Выполнение команд из файла
shell(commands)

# Запуск графического интерфейса
root.mainloop()
