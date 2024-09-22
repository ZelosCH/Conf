import os
import sys
import shutil
import csv
import datetime
import zipfile
import configparser

# Чтение конфигурационного файла
config = configparser.ConfigParser()
config.read('config.ini')
computer_name = config['DEFAULT']['computer_name']
vfs_path = config['DEFAULT']['vfs_path']
log_path = config['DEFAULT']['log_path']

# Извлечение виртуальной файловой системы из zip-файла
with zipfile.ZipFile(vfs_path, 'r') as zip_ref:
    zip_ref.extractall('vfs')

# Смена текущего рабочего каталога на виртуальную файловую систему
os.chdir('vfs')

# Функция для записи действий пользователя в лог-файл
def log_action(action):
    with open(log_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.datetime.now(), action])

# Функция для обработки пользовательского ввода и выполнения команд
def shell():
    while True:
        # Вывод приглашения к вводу
        print(f'{computer_name}:{os.getcwd()}$ ', end='')

        # Получение пользовательского ввода
        command = input()

        # Запись действия пользователя в лог-файл
        log_action(command)

        # Разбор команды
        args = command.split()

        # Выполнение команды
        if args[0] == 'ls':
            files = os.listdir()
            print('\n'.join(files))
        elif args[0] == 'cd':
            if len(args) > 1:
                path = os.path.normpath(args[1])
                if os.path.isabs(path):
                    os.chdir(path)
                else:
                    os.chdir(os.path.join(os.getcwd(), path))
            else:
                print('cd: missing argument')
        elif args[0] == 'exit':
            sys.exit()
        elif args[0] == 'mv':
            shutil.move(args[1], args[2])
        elif args[0] == 'tail':
            with open(args[1], 'r') as f:
                lines = f.readlines()
                print(''.join(lines[-10:]))
        elif args[0] == 'cal':
            import calendar
            print(calendar.month(int(args[1]), int(args[2])))
        else:
            print(f'Команда не найдена: {args[0]}')

# Запуск эмулятора оболочки
shell()
