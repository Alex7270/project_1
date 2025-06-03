from src.utils import clearing_data, greetings


def main() -> None:
    """
    Основная функция программы. Отвечает за логику проекта и связывает функциональности между собой.
    :return: None
    """
    print(clearing_data())
    print(greetings())


if __name__ == "__main__":
    main()
