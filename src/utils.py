import json
import os
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame

import logger
from src import file_reader
from src.file_reader import reade_file

logger = logger.get_logger(__name__)


def clearing_data() -> DataFrame | str:
    """
    Очищает некорректные данные в столбцах 'Номер карты', 'Категория', 'MCC', заменяет отсутствующие данные на 0
    :return: DataFrame
    """
    df: DataFrame | str = file_reader.reade_file()
    if isinstance(df, DataFrame):
        data = df.dropna(subset=["Номер карты", "Категория", "MCC"])
        return data.fillna(0)
    return "Неверный формат данных"


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

    return json.dumps(greeting, ensure_ascii=False)
    # return greeting


def get_cards() -> str:
    """
    Группирует расходы по номерам карт
    :return: DataFrame
    """
    data = reade_file()
    if isinstance(data, DataFrame):
        df = data.loc[(data["Сумма платежа"] < 0) & (data["Номер карты"] != 0) & (data["Статус"] == "OK")]
        df_cards = df.groupby("Номер карты", as_index=False)["Сумма платежа"].sum()
        df_cards = df_cards.assign(cashback=round(-df_cards["Сумма платежа"] / 100, 2))
        df_cards = df_cards.rename(columns={"Номер карты": "last_digits", "Сумма платежа": "total_spent"})
    else:
        return ""
    # return json.dumps(df_cards.to_dict(orient="records"), ensure_ascii=False, indent=4)
    return df_cards.to_dict(orient="records")


def top_transactions() -> str | DataFrame:
    """
    Сортирует транзакции по сумме платежа
    :return: str
    """
    data = reade_file()
    if isinstance(data, DataFrame):
        df = (
            data.loc[data["Статус"] == "OK"]
            .sort_values(["Сумма платежа"], key=lambda x: abs(x), ascending=False)
            .head(5)
        )
        df = df[["Дата операции", "Сумма платежа", "Категория", "Описание"]]
        df = df.rename(
            columns={
                "Дата операции": "date",
                "Сумма платежа": "amount",
                "Категория": "category",
                "Описание": "description",
            }
        )
    else:
        return ""
    # return json.dumps(df.to_dict(orient="records"), ensure_ascii=False, indent=4)
    return df


def format_date_columns(data: DataFrame) -> Any:
    """
    Форматирует колонку с датами
    :return: DataFrame
    """
    data["Дата операции"] = pd.to_datetime(data["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce").dt.date
    # data["Дата операции"] = pd.to_datetime(data["Дата операции"], infer_datetime_format=True, errors="coerce").dt.date
    return data


def reade_json_file() -> list[Any] | Any:
    """
    Чтение json-файла user_settings
    :return: list[Any] | Any
    """
    logger.info("Чтение json-файла user_settings")
    try:
        with open("user_settings.json", encoding="utf-8") as f:
            user_list = json.load(f)
            return user_list
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        logger.error(f"{e}")
        return []


def get_currency_rates() -> str | list[Any]:
    """
    Получение курсов валют
    :return: list|str
    """
    logger.info("Начало работы функции по получению курсов валют")
    # Загрузка переменных из .env-файла
    load_dotenv()

    # Получение значения переменной API_KEY из .env-файла
    api_key = os.getenv("API_KEY")

    url = "https://api.apilayer.com/exchangerates_data/convert"

    user_settings = reade_json_file()["user_currencies"]
    currency_rates = []
    for currency in user_settings:
        params = {"amount": 1, "to": "RUB", "from": currency}
        headers = {"apikey": api_key}
        try:
            response = requests.request("GET", url, headers=headers, params=params, timeout=50)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"
        else:
            currency_rates.append({"currency": currency, "rate": round(response.json().get("info").get("rate"), 2)})
    return currency_rates


print(get_currency_rates())

# def get_stock_rates() -> list:
#     # logger.info("Начало работы функции по получению данных о котировках акций")
#     with open(settings, "r", encoding="utf-8") as file:
#         ticker_list = json.load(file)["user_stocks"]
#     stock = []
#     for ticker in ticker_list:
#         temp = {"stock": ticker, "price": yf.Ticker(ticker).info["currentPrice"]}
#         stock.append(temp)
#         # logger.info("Успешное получение данных о котировках акций и формирование корректного JSON-ответа")
#     return stock
