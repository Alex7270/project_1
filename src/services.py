import json
from typing import Any

import logger
from src.file_reader import reade_file

logger = logger.get_logger(__name__)

# Преобразование в список словарей
data = reade_file().to_dict(orient="records")


def filter_transactions(transactions: list[dict[str, Any]], search: str) -> str:
    """
    Фильтрация транзакций по заданному ключевому слову
    :param transactions: list[dict[str, Any]]
    :param search: str
    :return: str
    """
    logger.info("Начало работы функции фильтрации")

    new_list = []
    for transaction in transactions:
        if transaction.get('Категория', "") == search:
            new_list.append(transaction)
        elif transaction.get('Описание', "") == search:
            new_list.append(transaction)

    logger.info(f'Транзакции отфильтрованы по ключевому слову: "{search}"')
    return json.dumps(new_list, indent=4, ensure_ascii=False)

print(filter_transactions(data, "Иван Ф."))
