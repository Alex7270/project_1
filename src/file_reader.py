import pandas as pd

import logger

logger_ = logger.get_logger(__name__)


def reade_file(filepath: str = "data/operations.xlsx") -> pd.DataFrame | str | None:
    """
    Читает содержимое файла
    :param filepath: str
    :return: pd.DataFrame | str
    """
    logger_.info("Чтение xlsx-файла")
    try:
        df = pd.read_excel(filepath)
        if df.empty:
            return "Файл пустой"
        return df.fillna(0)

    except Exception as e:
        logger_.error(f"Error: {e}")
        return f"Error: {e}"
