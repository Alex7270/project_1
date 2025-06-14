import json
import re
from typing import Any

import logger

logger = logger.get_logger(__name__)


def filter_transactions(transactions: list[dict[str, Any]], search: str) -> str:
    """
    Фильтрация транзакций по заданному ключевому слову
    :param transactions: list[dict[str, Any]]
    :param search: str
    :return: str
    """
    logger.info("Начало работы функции filter_transactions")

    new_lst = []
    for transaction in transactions:
        for i, value in transaction.items():
            if re.search(search, str(value), re.I):
                new_lst.append(transaction)

    logger.info(f"Транзакции отфильтрованы по запросу: {search}")

    return json.dumps(new_lst, ensure_ascii=False, indent=4)
