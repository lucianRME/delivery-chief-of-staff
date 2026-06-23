"""Deduplicated and capped delivery health scoring."""


SEVERITY_DEDUCTIONS = {
    "Critical": 10,
    "High": 7,
    "Medium": 4,
    "Low": 2,
}

CATEGORY_CAPS = {
    "Delivery Risk": 20,
    "Dependency": 15,
    "Governance": 20,
    "Release Readiness": 20,
    "Data Quality": 10,
}

STATUS_SUMMARIES = {
    "Healthy": "Delivery is broadly on track with manageable risks.",
    "Watch": "Delivery is mostly stable but requires targeted management attention.",
    "At Risk": "Delivery risk is material and requires leadership action.",
    "Critical": "Delivery is unlikely to meet current commitments without intervention.",
}


def _status_for_score(score: int) -> str:
    if score >= 85:
        return "Healthy"
    if score >= 70:
        return "Watch"
    if score >= 50:
        return "At Risk"
    return "Critical"


def _deduplicate_findings(findings: list[dict]) -> list[dict]:
    """Keep the highest-severity finding for each stable evidence key."""
    selected = {}
    selected_weights = {}
    for index, finding in enumerate(findings):
        evidence_key = str(finding.get("evidence_key", "")).strip() or f"finding:{index}"
        severity = str(finding.get("severity", "Low")).title()
        weight = SEVERITY_DEDUCTIONS.get(severity, 0)
        if evidence_key not in selected or weight > selected_weights[evidence_key]:
            selected[evidence_key] = {**finding, "evidence_key": evidence_key, "severity": severity}
            selected_weights[evidence_key] = weight
    return list(selected.values())


def calculate_health_score(findings: list[dict]) -> dict:
    """Calculate an explainable score from unique evidence units."""
    deduplicated = _deduplicate_findings(findings)
    critical_count = sum(item["severity"] == "Critical" for item in deduplicated)
    ordered = sorted(
        enumerate(deduplicated),
        key=lambda item: (-SEVERITY_DEDUCTIONS.get(item[1]["severity"], 0), item[0]),
    )

    raw_category_totals = {group: 0 for group in CATEGORY_CAPS}
    candidates = []
    for _, finding in ordered:
        severity = finding["severity"]
        points = SEVERITY_DEDUCTIONS.get(severity, 0)
        if not points:
            continue
        category_group = finding.get("category_group")
        if category_group not in CATEGORY_CAPS:
            category_group = "Data Quality"
        raw_category_totals[category_group] += points
        candidates.append({
            "evidence_key": finding["evidence_key"],
            "severity": severity,
            "category_group": category_group,
            "points": points,
            "reason": finding.get("finding", "Unspecified finding"),
        })

    category_totals = {group: 0 for group in CATEGORY_CAPS}
    capped_categories = [
        group for group, total in raw_category_totals.items() if total > CATEGORY_CAPS[group]
    ]
    category_capped = []
    for deduction in candidates:
        group = deduction["category_group"]
        available = CATEGORY_CAPS[group] - category_totals[group]
        applied_points = min(deduction["points"], max(available, 0))
        if applied_points:
            category_capped.append({**deduction, "points": applied_points})
            category_totals[group] += applied_points

    maximum_total_deduction = 100 if critical_count >= 3 else 65
    deductions = []
    final_category_totals = {group: 0 for group in CATEGORY_CAPS}
    applied_total = 0
    for deduction in category_capped:
        remaining = maximum_total_deduction - applied_total
        applied_points = min(deduction["points"], max(remaining, 0))
        if not applied_points:
            break
        deductions.append({**deduction, "points": applied_points})
        final_category_totals[deduction["category_group"]] += applied_points
        applied_total += applied_points

    score = max(0, 100 - applied_total)
    status = _status_for_score(score)
    return {
        "score": score,
        "status": status,
        "status_summary": STATUS_SUMMARIES[status],
        "deductions": deductions,
        "category_totals": final_category_totals,
        "capped_categories": capped_categories,
    }
