"""Governance and data-quality detection rules."""

import pandas as pd


def _text(value) -> str:
    return "" if pd.isna(value) else str(value).strip()


def _is(value, *expected: str) -> bool:
    return _text(value).lower() in {item.lower() for item in expected}


def _finding(
    severity,
    category,
    category_group,
    finding,
    evidence,
    evidence_key,
    source,
    action,
) -> dict:
    return {
        "severity": severity,
        "category": category,
        "category_group": category_group,
        "finding": finding,
        "evidence": evidence,
        "evidence_key": evidence_key,
        "source": source,
        "recommended_action": action,
    }


def analyze_governance(jira: pd.DataFrame, raid: pd.DataFrame, release: pd.DataFrame) -> list[dict]:
    """Return governance findings across all three datasets."""
    findings = []

    for _, row in jira.iterrows():
        issue_key = _text(row.get("issue_key"))
        issue = issue_key or "Unknown Jira issue"
        evidence_key = f"jira:{issue_key or 'missing'}"
        if not _text(row.get("assignee")):
            findings.append(
                _finding(
                    "Medium",
                    "Missing Assignee",
                    "Data Quality",
                    f"Jira issue {issue} has no assignee.",
                    f"issue_key={issue}; assignee=missing",
                    evidence_key,
                    "Jira",
                    f"Assign an accountable owner to {issue}.",
                )
            )
        if _is(row.get("issue_type"), "Story") and not _text(
            row.get("acceptance_criteria")
        ):
            findings.append(
                _finding(
                    "Medium",
                    "Missing Acceptance Criteria",
                    "Data Quality",
                    f"Jira story {issue} has no acceptance criteria.",
                    f"issue_key={issue}; acceptance_criteria=missing",
                    evidence_key,
                    "Jira",
                    (
                        f"Add testable acceptance criteria to {issue} before "
                        "implementation continues."
                    ),
                )
            )

    for _, row in raid.iterrows():
        raid_key = _text(row.get("raid_id"))
        raid_id = raid_key or "Unknown RAID item"
        evidence_key = f"raid:{raid_key or 'missing'}"
        if not _text(row.get("owner")):
            findings.append(
                _finding(
                    "High",
                    "Missing Owner",
                    "Governance",
                    f"RAID item {raid_id} has no owner.",
                    f"raid_id={raid_id}; owner=missing",
                    evidence_key,
                    "RAID",
                    f"Assign an accountable owner to {raid_id}.",
                )
            )
        if not _text(row.get("mitigation")):
            findings.append(
                _finding(
                    "High",
                    "Missing Mitigation",
                    "Governance",
                    f"RAID item {raid_id} has no mitigation.",
                    f"raid_id={raid_id}; mitigation=missing",
                    evidence_key,
                    "RAID",
                    f"Document a specific mitigation and due date for {raid_id}.",
                )
            )

    for _, row in release.iterrows():
        release_key = _text(row.get("release_id"))
        milestone_key = _text(row.get("milestone"))
        release_id = release_key or "Unknown release"
        milestone = milestone_key or "Unnamed milestone"
        evidence_key = f"release:{release_key or 'missing'}:{milestone_key or 'missing'}"
        if not _text(row.get("owner")):
            findings.append(
                _finding(
                    "High",
                    "Missing Milestone Owner",
                    "Governance",
                    f"Release milestone '{milestone}' has no owner.",
                    f"release_id={release_id}; milestone={milestone}; owner=missing",
                    evidence_key,
                    "Release",
                    f"Assign an accountable owner to release milestone '{milestone}'.",
                )
            )
        if _is(row.get("rollback_plan"), "No", "N", "False"):
            findings.append(
                _finding(
                    "High",
                    "Missing Rollback Plan",
                    "Release Readiness",
                    f"{release_id} has no rollback plan.",
                    (
                        f"release_id={release_id}; milestone={milestone}; "
                        f"rollback_plan={_text(row.get('rollback_plan'))}"
                    ),
                    evidence_key,
                    "Release",
                    (
                        "Create and validate a rollback plan before approving "
                        f"{release_id} for release."
                    ),
                )
            )
        if _is(row.get("business_approval"), "No", "N", "False"):
            findings.append(
                _finding(
                    "High",
                    "Missing Business Approval",
                    "Release Readiness",
                    f"{release_id} is missing business approval.",
                    (
                        f"release_id={release_id}; milestone={milestone}; "
                        f"business_approval={_text(row.get('business_approval'))}"
                    ),
                    evidence_key,
                    "Release",
                    f"Obtain recorded business approval for {release_id} before go-live.",
                )
            )
        if _is(row.get("entry_criteria_met"), "No", "N", "False"):
            findings.append(
                _finding(
                    "High",
                    "Entry Criteria Gap",
                    "Release Readiness",
                    f"Entry criteria are not met for '{milestone}'.",
                    (
                        f"release_id={release_id}; milestone={milestone}; "
                        f"entry_criteria_met={_text(row.get('entry_criteria_met'))}"
                    ),
                    evidence_key,
                    "Release",
                    f"Close or formally waive entry criteria gaps for '{milestone}'.",
                )
            )
        if _is(row.get("exit_criteria_met"), "No", "N", "False"):
            findings.append(
                _finding(
                    "High",
                    "Exit Criteria Gap",
                    "Release Readiness",
                    f"Exit criteria are not met for '{milestone}'.",
                    (
                        f"release_id={release_id}; milestone={milestone}; "
                        f"exit_criteria_met={_text(row.get('exit_criteria_met'))}"
                    ),
                    evidence_key,
                    "Release",
                    f"Close or formally waive exit criteria gaps for '{milestone}'.",
                )
            )

    return findings
