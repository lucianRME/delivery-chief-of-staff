"""Dependency detection rules."""

import pandas as pd


def _text(value) -> str:
    return "" if pd.isna(value) else str(value).strip()


def _is(value, *expected: str) -> bool:
    return _text(value).lower() in {item.lower() for item in expected}


def _finding(severity, category, finding, evidence, evidence_key, source, action) -> dict:
    return {
        "severity": severity,
        "category": category,
        "category_group": "Dependency",
        "finding": finding,
        "evidence": evidence,
        "evidence_key": evidence_key,
        "source": source,
        "recommended_action": action,
    }


def analyze_dependencies(jira: pd.DataFrame, raid: pd.DataFrame) -> list[dict]:
    """Return dependency findings from Jira and RAID data."""
    findings = []

    for _, row in jira.iterrows():
        issue_key = _text(row.get("issue_key"))
        issue = issue_key or "Unknown Jira issue"
        evidence_key = f"jira:{issue_key or 'missing'}"
        dependency = _text(row.get("dependency"))
        blocker = _text(row.get("blocker"))
        priority = _text(row.get("priority"))
        if dependency:
            severity = "High" if _is(priority, "Critical", "Highest", "High") else "Medium"
            finding_text = f"{issue} has an active dependency"
            finding_text += (
                " on a high-priority delivery path."
                if severity == "High"
                else "."
            )
            findings.append(
                _finding(
                    severity,
                    "Active Dependency",
                    finding_text,
                    (
                        f"issue_key={issue}; dependency={dependency}; "
                        f"priority={priority or 'missing'}"
                    ),
                    evidence_key,
                    "Jira",
                    (
                        f"Confirm the owner and delivery date for dependency "
                        f"'{dependency}' affecting {issue}."
                    ),
                )
            )
        if blocker:
            findings.append(
                _finding(
                    "High",
                    "Documented Blocker",
                    f"{issue} has a documented blocker.",
                    f"issue_key={issue}; blocker={blocker}",
                    evidence_key,
                    "Jira",
                    f"Track blocker '{blocker}' to closure with an accountable owner.",
                )
            )

    for _, row in raid.iterrows():
        if not _is(row.get("type"), "Dependency"):
            continue
        raid_key = _text(row.get("raid_id"))
        raid_id = raid_key or "Unknown RAID dependency"
        evidence_key = f"raid:{raid_key or 'missing'}"
        owner = _text(row.get("owner"))
        linked_issue = _text(row.get("linked_issue"))
        findings.append(
            _finding(
                "Medium" if owner else "High",
                "RAID Dependency",
                f"RAID dependency {raid_id}"
                + (" has no owner." if not owner else " requires tracking."),
                (
                    f"raid_id={raid_id}; owner={owner or 'missing'}; "
                    f"linked_issue={linked_issue or 'none'}"
                ),
                evidence_key,
                "RAID",
                (
                    f"{'Assign an owner to' if not owner else 'Confirm the delivery date for'} "
                    f"dependency {raid_id}."
                ),
            )
        )

        if linked_issue:
            matches = jira[
                jira["issue_key"].fillna("").astype(str).str.strip().str.lower()
                == linked_issue.lower()
            ]
            if not matches.empty and _is(
                matches.iloc[0].get("priority"),
                "Critical",
                "Highest",
                "High",
            ):
                findings.append(
                    _finding(
                        "High",
                        "High-priority Dependency",
                        (
                            f"Dependency {raid_id} is linked to high-priority "
                            f"issue {linked_issue}."
                        ),
                        (
                            f"raid_id={raid_id}; linked_issue={linked_issue}; "
                            f"jira_priority={_text(matches.iloc[0].get('priority'))}"
                        ),
                        evidence_key,
                        "RAID",
                        (
                            f"Review {raid_id} and {linked_issue} together in "
                            "the next delivery checkpoint."
                        ),
                    )
                )

    return findings
