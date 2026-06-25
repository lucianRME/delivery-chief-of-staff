"""Tests for CSV schema validation."""

import pandas as pd

from core.validators import REQUIRED_COLUMNS, validate_all, validate_dataframe


def test_validate_dataframe_accepts_required_columns() -> None:
    dataframe = pd.DataFrame([{column: "value" for column in REQUIRED_COLUMNS["jira"]}])

    result = validate_dataframe(dataframe, "jira")

    assert result["valid"] is True
    assert result["row_count"] == 1
    assert result["missing_columns"] == []


def test_validate_dataframe_reports_missing_columns() -> None:
    dataframe = pd.DataFrame([{"issue_key": "PROG-101"}])

    result = validate_dataframe(dataframe, "jira")

    assert result["valid"] is False
    assert "issue_type" in result["missing_columns"]
    assert result["errors"]


def test_validate_all_returns_each_dataset_result() -> None:
    dataframes = {
        data_type: pd.DataFrame(
            [{column: "value" for column in required_columns}]
        )
        for data_type, required_columns in REQUIRED_COLUMNS.items()
    }

    result = validate_all(dataframes)

    assert set(result) == {"jira", "raid", "release"}
    assert all(item["valid"] for item in result.values())
