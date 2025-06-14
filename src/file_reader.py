import pandas as pd

import logger

logger = logger.get_logger(__name__)


def reade_file(filepath: str = "data/operations.xlsx") -> pd.DataFrame | str | None:
    """
    Читает содержимое файла
    :param filepath: str
    :return: pd.DataFrame | str
    """
    logger.info("Чтение excel-файла")
    try:
        df = pd.read_excel(filepath)
        if df.empty:
            return "Файл пустой"
        logger.info("excel-файл прочитан")
        return df.fillna(0)

    except Exception as e:
        logger.error(f"Error: {e}")
        return None
