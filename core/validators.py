"""Schema validation for uploaded delivery data."""

import pandas as pd


REQUIRED_COLUMNS = {
    "jira": [
        "issue_key", "issue_type", "summary", "status", "priority", "assignee",
        "team", "sprint", "due_date", "release", "dependency", "blocker",
        "acceptance_criteria", "story_points", "updated_date",
    ],
    "raid": [
        "raid_id", "type", "description", "impact", "probability", "owner",
        "mitigation", "due_date", "status", "linked_issue", "escalation_required",
    ],
    "release": [
        "release_id", "release_name", "release_date", "milestone", "milestone_status",
        "owner", "entry_criteria_met", "exit_criteria_met", "rollback_plan",
        "comms_plan", "test_status", "business_approval", "notes",
    ],
}


def validate_dataframe(dataframe: pd.DataFrame, data_type: str) -> dict:
    """Return a simple validation result for one delivery dataset."""
    if data_type not in REQUIRED_COLUMNS:
        raise ValueError(f"Unknown data type: {data_type}")

    actual = {str(column).strip().lower() for column in dataframe.columns}
    missing = [column for column in REQUIRED_COLUMNS[data_type] if column not in actual]
    errors = []
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
    if dataframe.empty:
        errors.append("The CSV contains no data rows.")

    return {
        "valid": not errors,
        "row_count": len(dataframe),
        "missing_columns": missing,
        "errors": errors,
    }


def validate_all(dataframes: dict[str, pd.DataFrame]) -> dict[str, dict]:
    """Validate the Jira, RAID, and release datasets."""
    return {
        data_type: validate_dataframe(dataframes[data_type], data_type)
        for data_type in REQUIRED_COLUMNS
    }
