import argparse
import re
import json
import sys


class ConfigParser:
    def __init__(self):
        self.constants = {}

    def parse(self, text):
        text = self.remove_comments(text)
        lines = text.splitlines()
        result = {}

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if match := re.match(r'([_a-zA-Z][_a-zA-Z0-9]*):\s*(.+);', line):
                name, value = match.groups()
                result[name] = self.parse_value(value)
                if isinstance(result[name], (int, list)):
                    self.constants[name] = result[name]
            elif match := re.match(r'!\[([_a-zA-Z][_a-zA-Z0-9]*)\]', line):
                name = match.group(1)
                if name in self.constants:
                    result[name] = self.constants[name]
                else:
                    raise ValueError(f"Undefined constant '{name}'")
            else:
                raise SyntaxError(f"Syntax error in line: {line}")

        return result

    def parse_value(self, value):
        value = value.strip()
        if value.isdigit():  # Числа
            return int(value)
        elif value.startswith('array(') and value.endswith(')'):  # Массивы
            items = value[6:-1].split(',')
            return [self.parse_value(item.strip()) for item in items]
        elif value.startswith('"') and value.endswith('"'):  # Строки
            return value[1:-1]  # Убираем кавычки
        elif value.startswith('![') and value.endswith(']'):  # Подстановки
            const_name = value[2:-1]  # Извлекаем имя константы
            if const_name in self.constants:
                return self.constants[const_name]
            else:
                raise ValueError(f"Undefined constant '{const_name}'")
        else:
            raise ValueError(f"Invalid value: {value}")

    def remove_comments(self, text):
        text = re.sub(r'#.*', '', text)
        text = re.sub(r'/\+.*?\+/', '', text, flags=re.DOTALL)
        return text.strip()


def main():
    parser = argparse.ArgumentParser(description="Учебный конфигурационный язык в JSON")
    parser.add_argument("output_file", help="Путь к файлу для вывода JSON")
    args = parser.parse_args()

    input_text = sys.stdin.read()
    config_parser = ConfigParser()

    try:
        result = config_parser.parse(input_text)
        with open(args.output_file, 'w') as f:
            json.dump(result, f, indent=4)
        print("Конфигурация успешно преобразована в JSON.")
    except (SyntaxError, ValueError) as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
