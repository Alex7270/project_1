import pandas as pd

import logger


def reade_file(filepath: str = "data/operations.xlsx") -> pd.DataFrame | str | None:
    """
    Читает содержимое файла
    :param filepath: str
    :return: pd.DataFrame | str
    """
    try:
        df = pd.read_excel(filepath)
        if df.empty:
            return "Файл пустой"
        return df.fillna(0)

    except Exception as e:
        return f"Error: {e}"
