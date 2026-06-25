"""Risk detection rules for Jira, RAID, and release data."""

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


def analyze_risks(jira: pd.DataFrame, raid: pd.DataFrame, release: pd.DataFrame) -> list[dict]:
    """Return risk findings across all three datasets."""
    findings = []

    for _, row in jira.iterrows():
        issue_key = _text(row.get("issue_key"))
        issue = issue_key or "Unknown Jira issue"
        evidence_key = f"jira:{issue_key or 'missing'}"
        priority = _text(row.get("priority"))
        status = _text(row.get("status"))
        if _is(status, "Blocked"):
            severity = "Critical" if _is(priority, "Critical", "Highest") else "High"
            findings.append(
                _finding(
                    severity,
                    "Blocked Issue",
                    "Delivery Risk",
                    f"{priority or 'Unprioritised'} issue {issue} is blocked.",
                    (
                        f"issue_key={issue}; status={status}; "
                        f"blocker={_text(row.get('blocker')) or 'not specified'}"
                    ),
                    evidence_key,
                    "Jira",
                    (
                        f"Assign an owner to remove the blocker for {issue} "
                        "and confirm a recovery date."
                    ),
                )
            )
        if _is(priority, "Critical", "Highest", "High") and not _is(
            status,
            "Done",
            "Closed",
            "Resolved",
        ):
            severity = "Critical" if _is(priority, "Critical", "Highest") else "High"
            findings.append(
                _finding(
                    severity,
                    "Priority Exposure",
                    "Delivery Risk",
                    f"{priority} priority issue {issue} is not complete.",
                    (
                        f"issue_key={issue}; priority={priority}; "
                        f"status={status or 'missing'}"
                    ),
                    evidence_key,
                    "Jira",
                    f"Review the delivery path and completion forecast for {issue}.",
                )
            )

    for _, row in raid.iterrows():
        raid_key = _text(row.get("raid_id"))
        raid_id = raid_key or "Unknown RAID item"
        evidence_key = f"raid:{raid_key or 'missing'}"
        item_type = _text(row.get("type"))
        status = _text(row.get("status"))
        impact = _text(row.get("impact"))
        if (
            _is(item_type, "Risk", "Issue")
            and _is(impact, "High", "Critical")
            and not _is(status, "Closed", "Resolved")
        ):
            findings.append(
                _finding(
                    "Critical" if _is(impact, "Critical") else "High",
                    "High-impact RAID Item",
                    "Delivery Risk",
                    f"High-impact {item_type.lower()} {raid_id} remains open.",
                    (
                        f"raid_id={raid_id}; impact={impact}; "
                        f"status={status or 'missing'}"
                    ),
                    evidence_key,
                    "RAID",
                    (
                        "Confirm mitigation, accountable owner, and target "
                        f"resolution for {raid_id}."
                    ),
                )
            )
        if _is(row.get("escalation_required"), "Yes", "Y", "True"):
            findings.append(
                _finding(
                    "High",
                    "Escalation Required",
                    "Governance",
                    f"RAID item {raid_id} requires escalation.",
                    (
                        f"raid_id={raid_id}; "
                        f"escalation_required={_text(row.get('escalation_required'))}"
                    ),
                    evidence_key,
                    "RAID",
                    (
                        f"Escalate {raid_id} to the appropriate governance forum "
                        "with a clear decision request."
                    ),
                )
            )

    for _, row in release.iterrows():
        release_key = _text(row.get("release_id"))
        milestone_key = _text(row.get("milestone"))
        release_id = release_key or "Unknown release"
        milestone = milestone_key or "Unnamed milestone"
        evidence_key = f"release:{release_key or 'missing'}:{milestone_key or 'missing'}"
        if _is(row.get("milestone_status"), "At Risk"):
            findings.append(
                _finding(
                    "High",
                    "Milestone At Risk",
                    "Release Readiness",
                    f"Release milestone '{milestone}' is at risk.",
                    (
                        f"release_id={release_id}; milestone={milestone}; "
                        f"milestone_status={_text(row.get('milestone_status'))}"
                    ),
                    evidence_key,
                    "Release",
                    (
                        f"Create a recovery plan for '{milestone}' and assess "
                        "impact on the release date."
                    ),
                )
            )

    return findings
