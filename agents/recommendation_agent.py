"""Finding prioritisation and recommendation generation."""


SEVERITY_PRIORITY = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}


def recommend_actions(findings: list[dict], limit: int = 7) -> list[dict]:
    """Return the highest-priority unique recommended actions."""
    ordered = sorted(
        findings,
        key=lambda item: SEVERITY_PRIORITY.get(str(item.get("severity", "Low")).title(), 4),
    )
    recommendations = []
    seen = set()

    for finding in ordered:
        action = str(finding.get("recommended_action", "")).strip()
        if not action or action.casefold() in seen:
            continue
        seen.add(action.casefold())
        recommendations.append({
            "severity": str(finding.get("severity", "Low")).title(),
            "category": finding.get("category", "General"),
            "category_group": finding.get("category_group", "Data Quality"),
            "finding": finding.get("finding", ""),
            "evidence": finding.get("evidence", ""),
            "evidence_key": finding.get("evidence_key", ""),
            "source": finding.get("source", ""),
            "recommended_action": action,
        })
        if len(recommendations) >= limit:
            break

    return recommendations
