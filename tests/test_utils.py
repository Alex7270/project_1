from freezegun import freeze_time

from src.utils import greetings


@freeze_time("2025-06-01 07:00:00")
def test_greetings_morning() -> None:
    """
    Тестирование функции приветствия
    :return: None
    """
    assert greetings() == '"Доброе утро"'


@freeze_time("2025-06-01 15:59:00")
def test_greetings_day() -> None:
    """
    Тестирование функции приветствия
    :return: None
    """
    assert greetings() == '"Добрый день"'


@freeze_time("2025-06-01 22:55:00")
def test_greetings_evening() -> None:
    """
    Тестирование функции приветствия
    :return: None
    """
    assert greetings() == '"Добрый вечер"'


@freeze_time("2025-05-01 03:00:00")
def test_greetings_night() -> None:
    """
    Тестирование функции приветствия
    :return: None
    """
    assert greetings() == '"Доброй ночи"'
