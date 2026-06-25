"""Tests for delivery health scoring."""

from core.scoring import calculate_health_score


def test_scoring_deduplicates_by_evidence_key_and_caps_floor() -> None:
    findings = [
        {
            "severity": "High",
            "category_group": "Delivery Risk",
            "finding": "Issue PROG-101 is blocked.",
            "evidence_key": "jira:PROG-101",
        },
        {
            "severity": "Medium",
            "category_group": "Governance",
            "finding": "Issue PROG-101 has no assignee.",
            "evidence_key": "jira:PROG-101",
        },
        {
            "severity": "High",
            "category_group": "Governance",
            "finding": "RAID item R-001 has no owner.",
            "evidence_key": "raid:R-001",
        },
    ]

    result = calculate_health_score(findings)

    assert result["score"] == 86
    assert result["status"] == "Healthy"
    assert len(result["deductions"]) == 2
    assert result["category_totals"]["Delivery Risk"] == 7
    assert result["category_totals"]["Governance"] == 7


def test_at_risk_sample_score_is_stable() -> None:
    from pathlib import Path

    from agents.dependency_agent import analyze_dependencies
    from agents.governance_agent import analyze_governance
    from agents.risk_agent import analyze_risks
    from core.data_loader import load_sample_data

    dataframes = load_sample_data(Path("data"), "at_risk")
    findings = (
        analyze_risks(dataframes["jira"], dataframes["raid"], dataframes["release"])
        + analyze_dependencies(dataframes["jira"], dataframes["raid"])
        + analyze_governance(
            dataframes["jira"],
            dataframes["raid"],
            dataframes["release"],
        )
    )

    result = calculate_health_score(findings)

    assert result["score"] == 63
    assert result["status"] == "At Risk"
