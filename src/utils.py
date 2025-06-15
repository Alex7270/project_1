import json
import os
from datetime import datetime
from typing import Any, Hashable

import pandas as pd
import requests
import yfinance as yf
from dotenv import load_dotenv
from pandas import DataFrame

import logger
from src.file_reader import reade_file

logger_ = logger.get_logger(__name__)


def greetings() -> str:
    """
    Приветствует в зависимости от времени суток
    :return: str
    """
    logger_.info("Приветствие")
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


def format_date_columns() -> DataFrame:
    """
    Форматирует колонку с датами
    :return: DataFrame
    """
    data: DataFrame = reade_file()
    data["Дата операции"] = pd.to_datetime(data["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce")
    return data


def filters_by_date(date: str) -> DataFrame:
    """
    Фильтрует транзакции по дате
    :return: DataFrame
    """
    df = format_date_columns()
    end_date = pd.to_datetime(date)
    start_date = end_date.replace(day=1)
    df_filtered = df[df["Дата операции"].between(start_date, end_date, inclusive="both")]
    return df_filtered


def get_cards(data: DataFrame) -> Any:
    """
    Группирует расходы по номерам карт
    :return: DataFrame
    """
    if isinstance(data, DataFrame):
        df = data.loc[(data["Сумма платежа"] < 0) & (data["Номер карты"] != 0) & (data["Статус"] == "OK")]
        df_cards = df.groupby("Номер карты", as_index=False)["Сумма платежа"].sum()
        df_cards = df_cards.assign(cashback=round(-df_cards["Сумма платежа"] / 100, 2))
        df_cards = df_cards.rename(columns={"Номер карты": "last_digits", "Сумма платежа": "total_spent"})
    else:
        return ""

    return df_cards.to_dict(orient="records")


def top_transactions(data: DataFrame) -> str | list[dict[Hashable, Any]]:
    """
    Сортирует транзакции по сумме платежа
    :return: str
    """
    # Преобразование даты в строку для корректной
    data["Дата операции"] = data["Дата операции"].dt.strftime("%d.%m.%Y")

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

    return df.to_dict(orient="records")


def reade_json_file() -> Any:
    """
    Чтение json-файла user_settings
    :return: list[Any] | Any
    """
    logger_.info("Чтение json-файла user_settings")
    try:
        with open("user_settings.json", encoding="utf-8") as f:
            user_dict = json.load(f)
            return user_dict
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        logger_.error(f"{e}")
        return {}


def get_currency_rates() -> list[Any]:
    """
    Получение курса валют
    :return: list|str
    """
    logger_.info("Получение курса валют")
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
            logger_.error(f"Error: {e}")
        else:
            currency_rates.append({"currency": currency, "rate": round(response.json().get("info").get("rate"), 2)})
    return currency_rates


def get_stock_rates() -> Any:
    logger_.info("Получение данных о котировках акций")
    user_stocks = reade_json_file()["user_stocks"]
    stocks = []
    for ticker in user_stocks:
        stocks.append({"stock": ticker, "price": yf.Ticker(ticker).info["currentPrice"]})
    logger_.info("Данные о котировках акций получены")
    return stocks
