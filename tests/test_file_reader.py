from typing import Any
from unittest.mock import patch

from pandas import DataFrame
from pandas._testing import assert_frame_equal

from src.file_reader import reade_file


@patch("pandas.read_excel")
def test_reade_file(mock_excel: DataFrame, expected_df: DataFrame) -> None:
    """
    Тестирование функции чтения xlsx-файла
    :param mock_excel: Any
    :param expected_df: pd.DataFrame
    :return: None
    """
    mock_excel.return_value = expected_df
    assert_frame_equal(reade_file(), expected_df)


@patch("pandas.read_excel")
def test_reade_file_empty(mock_excel: Any) -> None:
    """
    Тестирование функции чтения пустого xlsx-файла
    :param mock_excel: Any
    :return: None
    """
    mock_excel.return_value.empty.return_value = True
    assert reade_file() == "Файл пустой"
    mock_excel.assert_called_once()


def test_reade_file_incorrect(filepath_incorrect: str) -> None:
    """
    Тестирование функции чтения xlsx-файла c некорректным путем к файлу
    :return: None
    """
    assert reade_file(filepath_incorrect) == f"Error: [Errno 2] No such file or directory: '{filepath_incorrect}'"
