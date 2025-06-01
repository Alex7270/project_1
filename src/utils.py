from datetime import datetime
from typing import Any

from file_reader import reade_file


def clearing_data() -> Any:
    """
    Очищает некорректные данные в столбцах 'Номер карты', 'Категория', 'MCC', заменяет отсутствующие данные на 0
    :param: df pd.DataFrame
    :return: pd.DataFrame
    """
    df = reade_file()
    data = df.dropna(subset=["Номер карты", "Категория", "MCC"])
    return data.fillna(0)


def greetings() -> str:
    """
    Приветствует в зависимости от времени суток
    :return: str
    """
    hour_now = datetime.now().hour
    if 23 <= hour_now < 6:
        greeting = "Доброй ночи"
    elif 17 <= hour_now < 24:
        greeting = "Добрый вечер"
    elif 12 <= hour_now < 18:
        greeting = "Добрый день"
    else:
        greeting = "Доброе утро"

    return greeting
