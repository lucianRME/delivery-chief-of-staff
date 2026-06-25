"""Optional OpenAI-powered executive brief generation.

The deterministic governance engine remains the source of truth. This module
only converts already-produced evidence-backed findings into a sharper
executive narrative when explicitly enabled by the user.
"""

from __future__ import annotations

import json
import os
from typing import Any

from agents.recommendation_agent import SEVERITY_PRIORITY


OPENAI_MODEL = "gpt-4o-mini"
CONFIDENCE_NOTE = (
    "This brief is generated from deterministic evidence-backed findings and "
    "does not alter the underlying score."
)
PLACEHOLDER_API_KEYS = {
    "your-key-here",
    "your-openai-api-key-here",
    "sk-your-real-key-here",
}

AI_BRIEF_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "headline": {"type": "string"},
        "executive_briefing": {"type": "string"},
        "leadership_actions": {
            "type": "array",
            "items": {"type": "string"},
        },
        "decision_required": {"type": "string"},
        "confidence_note": {"type": "string"},
    },
    "required": [
        "headline",
        "executive_briefing",
        "leadership_actions",
        "decision_required",
        "confidence_note",
    ],
}


def _safe_text(value: Any, default: str = "") -> str:
    """Return compact text safe for prompts and UI display."""
    if value is None:
        return default
    cleaned = " ".join(str(value).split())
    return cleaned or default


def _safe_error_message(error: Exception) -> str:
    """Return an error message without exposing the configured API key."""
    message = _safe_text(error, error.__class__.__name__)
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        message = message.replace(api_key, "[redacted]")
    return message[:300]


def _configured_api_key() -> str | None:
    """Return a real configured API key, ignoring local template placeholders."""
    api_key = _safe_text(os.getenv("OPENAI_API_KEY"))
    if not api_key or api_key in PLACEHOLDER_API_KEYS:
        return None
    return api_key


def _ordered(items: list[dict] | None) -> list[dict]:
    """Return dictionaries in stable severity order."""
    valid = [item for item in (items or []) if isinstance(item, dict)]
    return [
        item
        for _, item in sorted(
            enumerate(valid),
            key=lambda pair: (
                SEVERITY_PRIORITY.get(_safe_text(pair[1].get("severity"), "Low").title(), 4),
                pair[0],
            ),
        )
    ]


def _summarise_finding(finding: dict) -> dict:
    """Keep the LLM payload small and evidence-key focused."""
    return {
        "severity": _safe_text(finding.get("severity"), "Low").title(),
        "category": _safe_text(finding.get("category")),
        "category_group": _safe_text(finding.get("category_group")),
        "finding": _safe_text(finding.get("finding")),
        "evidence_key": _safe_text(finding.get("evidence_key")),
        "source": _safe_text(finding.get("source")),
        "recommended_action": _safe_text(finding.get("recommended_action")),
    }


def _build_payload(
    scoring_result: dict,
    all_findings: list,
    recommendations: list,
) -> dict:
    """Build the minimal evidence-backed payload sent to OpenAI."""
    scoring_result = scoring_result if isinstance(scoring_result, dict) else {}
    top_findings = [_summarise_finding(item) for item in _ordered(all_findings)[:10]]
    top_recommendations = [_summarise_finding(item) for item in _ordered(recommendations)[:7]]
    evidence_keys = sorted(
        {
            item["evidence_key"]
            for item in top_findings + top_recommendations
            if item.get("evidence_key")
        }
    )

    return {
        "score": scoring_result.get("score"),
        "status": scoring_result.get("status"),
        "status_summary": scoring_result.get("status_summary"),
        "category_totals": scoring_result.get("category_totals", {}),
        "top_findings": top_findings,
        "top_recommendations": top_recommendations,
        "evidence_keys": evidence_keys,
    }


def _extract_output_text(response: Any) -> str:
    """Extract text from a Responses API result across SDK versions."""
    output_text = getattr(response, "output_text", None)
    if output_text:
        return str(output_text)

    output = getattr(response, "output", None) or []
    for item in output:
        content = getattr(item, "content", None) or []
        for content_item in content:
            text = getattr(content_item, "text", None)
            if text:
                return str(text)
            if isinstance(content_item, dict) and content_item.get("text"):
                return str(content_item["text"])
    return ""


def _normalise_brief(candidate: Any) -> dict:
    """Validate and normalise an AI brief so UI/report code can trust it."""
    if not isinstance(candidate, dict):
        raise ValueError("OpenAI response was not a JSON object")

    leadership_actions = candidate.get("leadership_actions")
    if not isinstance(leadership_actions, list):
        leadership_actions = []

    brief = {
        "headline": _safe_text(candidate.get("headline")),
        "executive_briefing": _safe_text(candidate.get("executive_briefing")),
        "leadership_actions": [
            _safe_text(action)
            for action in leadership_actions
            if _safe_text(action)
        ][:5],
        "decision_required": _safe_text(candidate.get("decision_required")),
        "confidence_note": _safe_text(candidate.get("confidence_note"), CONFIDENCE_NOTE),
    }

    missing = [
        key
        for key in ("headline", "executive_briefing", "decision_required")
        if not brief[key]
    ]
    if missing:
        raise ValueError(f"OpenAI response missing required fields: {', '.join(missing)}")
    if not brief["leadership_actions"]:
        raise ValueError("OpenAI response missing leadership actions")

    brief["confidence_note"] = CONFIDENCE_NOTE
    return brief


def generate_ai_executive_brief(
    scoring_result: dict,
    executive_summary: dict,
    all_findings: list,
    recommendations: list,
    enabled: bool = False,
) -> dict:
    """Return an optional AI-enhanced executive brief.

    OpenAI is only used when explicitly enabled and configured. Failures return
    a safe non-blocking result so the deterministic dashboard continues to run.
    """
    if not enabled:
        return {"enabled": False, "brief": None, "error": None}

    try:
        from dotenv import load_dotenv

        load_dotenv()
    except Exception:
        pass

    if not _configured_api_key():
        return {"enabled": False, "brief": None, "error": "OPENAI_API_KEY not configured"}

    try:
        from openai import OpenAI
    except Exception as error:
        return {"enabled": False, "brief": None, "error": _safe_error_message(error)}

    payload = _build_payload(scoring_result, all_findings, recommendations)
    deterministic_summary = executive_summary if isinstance(executive_summary, dict) else {}
    payload["deterministic_executive_summary"] = {
        "headline": deterministic_summary.get("headline"),
        "summary": deterministic_summary.get("summary"),
        "decision_required": deterministic_summary.get("decision_required"),
    }

    system_prompt = (
        "You are an optional narrative agent for Delivery Chief of Staff. "
        "You are generating an executive narrative only. "
        "The core governance assessment is deterministic and auditable. "
        "OpenAI is used only as an optional narrative enhancement over "
        "deterministic evidence-backed findings. Return JSON only."
    )
    user_prompt = (
        "Create an AI-enhanced executive brief for banking operations governance "
        "and shared services delivery review.\n\n"
        "Constraints:\n"
        "- Use only the supplied score, status, status summary, findings, "
        "recommendations and evidence keys.\n"
        "- Do not invent risks.\n"
        "- Do not invent evidence.\n"
        "- Do not invent evidence keys.\n"
        "- Do not change the Delivery Health Score.\n"
        "- Do not change the status.\n"
        "- Do not change score deductions.\n"
        "- Do not create unsupported recommendations.\n"
        "- Do not claim an action is approved or completed.\n"
        "- Preserve human-in-loop governance.\n"
        "- Recommendations require delivery leader review and approval.\n"
        "- Mention only the top themes.\n"
        "- Keep the tone executive, concise and action-oriented.\n"
        "- Frame the brief for Banking Operations / Middle & Back Office "
        "Operations shared services delivery review.\n"
        "- Return structured JSON matching the expected fields.\n\n"
        f"Evidence-backed payload:\n{json.dumps(payload, indent=2, default=str)}"
    )

    try:
        client = OpenAI()
        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions=system_prompt,
            input=user_prompt,
            max_output_tokens=700,
            store=False,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "ai_executive_brief",
                    "schema": AI_BRIEF_SCHEMA,
                    "strict": True,
                }
            },
        )
        output_text = _extract_output_text(response)
        if not output_text:
            raise ValueError("OpenAI response did not include output text")
        brief = _normalise_brief(json.loads(output_text))
        return {"enabled": True, "brief": brief, "error": None}
    except Exception as error:
        return {"enabled": False, "brief": None, "error": _safe_error_message(error)}
