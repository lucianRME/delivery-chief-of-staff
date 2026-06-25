"""Tests for recommendation prioritisation."""

from agents.recommendation_agent import recommend_actions


def test_recommend_actions_deduplicates_and_prioritises_by_severity() -> None:
    findings = [
        {
            "severity": "Medium",
            "category": "Data Quality",
            "category_group": "Data Quality",
            "finding": "Story has no acceptance criteria.",
            "evidence": "issue_key=PROG-201",
            "evidence_key": "jira:PROG-201",
            "source": "Jira",
            "recommended_action": "Add acceptance criteria.",
        },
        {
            "severity": "High",
            "category": "Blocked Issue",
            "category_group": "Delivery Risk",
            "finding": "Issue is blocked.",
            "evidence": "issue_key=PROG-101",
            "evidence_key": "jira:PROG-101",
            "source": "Jira",
            "recommended_action": "Escalate blocker.",
        },
        {
            "severity": "Critical",
            "category": "Blocked Issue",
            "category_group": "Delivery Risk",
            "finding": "Another issue is blocked.",
            "evidence": "issue_key=PROG-102",
            "evidence_key": "jira:PROG-102",
            "source": "Jira",
            "recommended_action": "Escalate blocker.",
        },
    ]

    recommendations = recommend_actions(findings)

    assert len(recommendations) == 2
    assert recommendations[0]["severity"] == "Critical"
    assert recommendations[0]["recommended_action"] == "Escalate blocker."
    assert recommendations[1]["recommended_action"] == "Add acceptance criteria."
