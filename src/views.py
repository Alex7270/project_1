import json

from src.utils import filters_by_date, get_cards, get_currency_rates, get_stock_rates, greetings, top_transactions


def main_views(date: str) -> str:
    """
    Основная функция старицы главная
    :param date: str
    :return: str
    """
    data = filters_by_date(date)

    return json.dumps(
        {
            "greeting": greetings(),
            "cards": get_cards(data),
            "top_transactions": top_transactions(data),
            "currency_rates": get_currency_rates(),
            "stock_prices": get_stock_rates(),
        },
        ensure_ascii=False,
        indent=4,
    )
