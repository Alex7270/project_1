import json
from datetime import datetime

from pandas import DataFrame

from src.file_reader import reade_file


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


# def format_date_columns() -> DataFrame:
#     """
#     Форматирует колонки с датами в DataFrame
#     :return: DataFrame
#     """
#     data = reade_file()
#     data["Дата операции"] = pd.to_datetime(
#         data["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
#     )
#     data["Дата платежа"] = pd.to_datetime(data["Дата платежа"], format="%d.%m.%Y", errors="coerce")
#     return data


def get_cards() -> str:
    """
    Группирует расходы по номерам карт
    :return: DataFrame
    """
    data = reade_file()
    if isinstance(data, DataFrame):
        df = data.loc[(data["Сумма платежа"] < "0") & (data["Номер карты"] != 0) & (data["Статус"] == "OK")]
        df_cards = df.groupby("Номер карты", as_index=False)["Сумма платежа"].sum()
        df_cards = df_cards.assign(cashback=round(-df_cards["Сумма платежа"] / 100, 2))
        df_cards = df_cards.rename(columns={"Номер карты": "last_digits", "Сумма платежа": "total_spent"})
    else:
        return ""
    return json.dumps(df_cards.to_dict(orient="records"), ensure_ascii=False, indent=4)


def top_transactions() -> str:
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
    return json.dumps(df.to_dict(orient="records"), ensure_ascii=False, indent=4)
