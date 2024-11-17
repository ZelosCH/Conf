import pytest
import json
from Pars import ConfigParser

# Фикстура для создания экземпляра парсера
@pytest.fixture
def parser():
    return ConfigParser()

# Тест: обработка чисел и массивов
def test_numbers_and_arrays(parser):
    config = """
    max_limit: 100;
    min_limit: 0;
    numbers: array(1, 2, 3, 4, 5);
    """
    result = parser.parse(config)
    assert result == {
        "max_limit": 100,
        "min_limit": 0,
        "numbers": [1, 2, 3, 4, 5]
    }

# Тест: обработка строк
def test_strings(parser):
    config = """
    server_name: "localhost";
    """
    result = parser.parse(config)
    assert result == {
        "server_name": "localhost"
    }

# Тест: обработка подстановок
def test_constants_substitution(parser):
    config = """
    max_speed: 120;
    optimal_speed: ![max_speed];
    """
    result = parser.parse(config)
    assert result == {
        "max_speed": 120,
        "optimal_speed": 120
    }


# Тест: синтаксическая ошибка
def test_syntax_error(parser):
    config = """
    invalid_line
    """
    with pytest.raises(SyntaxError, match="Syntax error in line: invalid_line"):
        parser.parse(config)

# Тест: неопределённая константа
def test_undefined_constant(parser):
    config = """
    optimal_speed: ![max_speed];
    """
    with pytest.raises(ValueError, match="Undefined constant 'max_speed'"):
        parser.parse(config)

# Тест: удаление комментариев
def test_remove_comments(parser):
    config = """
    # Это комментарий
    value: 42; # Комментарий в строке
    /+ 
    Многострочный комментарий
    +/
    another_value: array(1, 2, 3);
    """
    result = parser.parse(config)
    assert result == {
        "value": 42,
        "another_value": [1, 2, 3]
    }

# Тест: сложная конфигурация
def test_complex_config(parser):
    config = """
    max_limit: 100;
    min_limit: 0;
    server_name: "localhost";
    allowed_ips: array("192.168.1.1", "192.168.1.2");
    optimal_speed: ![max_limit];
    """
    result = parser.parse(config)
    assert result == {
        "max_limit": 100,
        "min_limit": 0,
        "server_name": "localhost",
        "allowed_ips": ["192.168.1.1", "192.168.1.2"],
        "optimal_speed": 100
    }
