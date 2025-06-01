from datetime import datetime
from typing import Any, Union

from pandas import DataFrame

from src import file_reader


def clearing_data() -> Union[Any]:
    """
    Очищает некорректные данные в столбцах 'Номер карты', 'Категория', 'MCC', заменяет отсутствующие данные на 0
    :param: df pd.DataFrame
    :return: pd.DataFrame
    """
    df: DataFrame | Union[Any] = file_reader.reade_file()
    data = df.dropna(subset=["Номер карты", "Категория", "MCC"])
    return data.fillna(0)


def greetings() -> str:
    """
    Приветствует в зависимости от времени суток
    :return: str
    """
    hour_now = datetime.now().hour
    if 23 <= hour_now < 24 or 0 <= hour_now <= 5:
        greeting = "Доброй ночи"
    elif 17 <= hour_now < 23:
        greeting = "Добрый вечер"
    elif 12 <= hour_now < 18:
        greeting = "Добрый день"
    else:
        greeting = "Доброе утро"

    return greeting
