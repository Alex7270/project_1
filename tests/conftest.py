import pandas as pd
import pytest


@pytest.fixture()
def filepath() -> str:
    return "data/operations.xlsx"


@pytest.fixture()
def filepath_incorrect() -> str:
    return "data/oper[ations.xlsx"


@pytest.fixture()
def expected_df() -> pd.DataFrame:
    return pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
