"""CSV loading helpers."""

from pathlib import Path
from typing import IO, Union

import pandas as pd


CsvSource = Union[str, Path, IO[bytes]]


def load_csv(source: CsvSource) -> pd.DataFrame:
    """Load a CSV source and normalise its column names."""
    dataframe = pd.read_csv(source)
    dataframe.columns = [str(column).strip().lower() for column in dataframe.columns]
    return dataframe


SAMPLE_SCENARIO_SUFFIXES = {
    "at_risk": "_at_risk",
    "critical": "_critical",
}


def load_sample_data(
    data_dir: Union[str, Path] = "data",
    scenario: str = "at_risk",
) -> dict[str, pd.DataFrame]:
    """Load a bundled sample scenario. At Risk is the default demo."""
    if scenario not in SAMPLE_SCENARIO_SUFFIXES:
        raise ValueError(f"Unknown sample scenario: {scenario}")
    directory = Path(data_dir)
    suffix = SAMPLE_SCENARIO_SUFFIXES[scenario]
    return {
        "jira": load_csv(directory / f"jira_sample{suffix}.csv"),
        "raid": load_csv(directory / f"raid_sample{suffix}.csv"),
        "release": load_csv(directory / f"release_sample{suffix}.csv"),
    }
