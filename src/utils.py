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
