import pandas as pd


def reade_file(filepath: str = "data/operations.xlsx") -> pd.DataFrame | str:
    """
    Читает содержимое файла
    :param filepath: str
    :return: DataFrame
    """
    try:
        df = pd.read_excel(filepath)
        if df.empty:
            return "Файл пустой"
        return df

    except Exception as e:
        return f"Error: {e}"
