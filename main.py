from src.views import main_views


def main() -> None:
    """
    Основная функция программы. Отвечает за логику проекта и связывает функциональности между собой.
    :return: None
    """
    print(main_views("2021-02-10 23:15:00"))


if __name__ == "__main__":
    main()
