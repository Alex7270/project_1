import json
from typing import Any

import logger

logger_ = logger.get_logger(__name__)


print(hasattr(logger, "info"))
print(hasattr(logger, "error"))
#
# Преобразование в список словарей
# df = reade_file().to_dict(orient="records")


def filter_transactions(transactions: list[dict[str, Any]], search: str) -> str:
    """
    Фильтрация транзакций по заданному ключевому слову
    :param transactions: list[dict[str, Any]]
    :param search: str
    :return: str
    """
    logger_.info("Начало работы функции фильтрации")

    new_list = []
    for transaction in transactions:
        if search in [transaction.get("Категория", ""), transaction.get("Описание", "")]:
            new_list.append(transaction)

    logger_.info(f'Транзакции отфильтрованы по ключевому слову: "{search}"')

    return json.dumps(new_list, indent=4, ensure_ascii=False)
