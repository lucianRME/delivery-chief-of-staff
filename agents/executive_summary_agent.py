"""Deterministic executive summary generation."""

from agents.recommendation_agent import SEVERITY_PRIORITY


THEME_DESCRIPTIONS = {
    "Delivery Risk": "delivery blockers and high-impact risks",
    "Dependency": "unresolved dependencies",
    "Governance": "ownership and governance controls",
    "Release Readiness": "release readiness controls",
    "Data Quality": "delivery data quality",
}


def generate_executive_summary(score_result: dict, findings: list[dict]) -> dict:
    """Build a concise, action-oriented summary from existing findings."""
    score = score_result["score"]
    status = score_result["status"]
    category_totals = score_result.get("category_totals", {})
    top_groups = [
        group
        for group, points in sorted(category_totals.items(), key=lambda item: (-item[1], item[0]))
        if points > 0
    ][:3]

    if top_groups:
        themes = [THEME_DESCRIPTIONS[group] for group in top_groups]
        if len(themes) == 1:
            theme_text = themes[0]
        else:
            theme_text = f"{', '.join(themes[:-1])} and {themes[-1]}"
        summary = f"The principal concerns are {theme_text}."
    else:
        summary = "No material delivery concerns were identified in the supplied evidence."

    ordered_findings = sorted(
        enumerate(findings),
        key=lambda item: (
            SEVERITY_PRIORITY.get(str(item[1].get("severity", "Low")).title(), 4),
            item[0],
        ),
    )
    leadership_attention = []
    used_groups = set()
    used_actions = set()
    for _, finding in ordered_findings:
        group = finding.get("category_group")
        action = str(finding.get("recommended_action", "")).strip()
        if group not in top_groups or group in used_groups or not action:
            continue
        action_key = action.casefold()
        if action_key in used_actions:
            continue
        leadership_attention.append(action)
        used_groups.add(group)
        used_actions.add(action_key)
        if len(leadership_attention) == 3:
            break

    if status == "Healthy":
        decision_required = "Leadership should maintain current commitments and monitor the identified watch items."
    else:
        decision_required = (
            "Leadership should confirm ownership for the top blockers and agree whether release scope or date needs adjustment."
        )

    return {
        "headline": f"Delivery is {status} with a health score of {score}/100.",
        "summary": summary,
        "leadership_attention": leadership_attention,
        "decision_required": decision_required,
    }
