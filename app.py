"""Streamlit entry point for Delivery Chief of Staff."""

from pathlib import Path

import pandas as pd
import streamlit as st

from agents.dependency_agent import analyze_dependencies
from agents.executive_summary_agent import generate_executive_summary
from agents.governance_agent import analyze_governance
from agents.llm_summary_agent import generate_ai_executive_brief
from agents.recommendation_agent import recommend_actions
from agents.risk_agent import analyze_risks
from core.data_loader import load_csv, load_sample_data
from core.report_builder import build_markdown_report
from core.scoring import calculate_health_score
from core.validators import validate_all


BASE_DIR = Path(__file__).resolve().parent
SAMPLE_SCENARIOS = {
    "At Risk Programme": "at_risk",
    "Critical Programme": "critical",
}
SCENARIO_NOTES = {
    "at_risk": "Scenario: Recoverable delivery risk requiring targeted leadership intervention.",
    "critical": "Scenario: Severe delivery risk requiring immediate executive intervention.",
}
DISPLAY_COLUMNS = [
    "severity", "category", "category_group", "finding", "evidence",
    "evidence_key", "source", "recommended_action",
]
SEVERITY_PRIORITY = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}


st.set_page_config(page_title="Delivery Chief of Staff", page_icon="📋", layout="wide")
st.title("Delivery Chief of Staff")
st.write("Executive delivery advisor for Jira, RAID and release governance.")

with st.sidebar.expander("Architecture / About This MVP"):
    st.write(
        "Delivery Chief of Staff analyses Jira, RAID and release artefacts using "
        "specialised delivery agents."
    )
    st.markdown(
        "- Runs locally\n"
        "- Uses CSV uploads\n"
        "- Uses deterministic scoring\n"
        "- Requires no Jira API\n"
        "- Requires no cloud deployment\n"
        "- Requires no OpenAI API for the deterministic core flow"
    )
    st.markdown("**Agent sequence**")
    st.write(
        "Risk Agent → Dependency Agent → Governance Agent → Recommendation Agent → "
        "Executive Summary Agent"
    )
    st.caption(
        "Guardrail: recommendations are advisory and require human review. "
        "The deterministic score and evidence trail remain the source of truth."
    )

with st.sidebar.expander("Official Use Case Alignment"):
    st.write("BFSI / Banking / Banking Operations")
    st.write("Middle & Back Office Operations")
    st.write("Shared services operations work orchestration")
    st.markdown(
        "- Human-in-loop controls\n"
        "- Reporting and evidence"
    )

enable_ai_brief = st.sidebar.checkbox("Enable AI-enhanced executive brief", value=False)

st.subheader("Delivery data")
upload_columns = st.columns(3)
with upload_columns[0]:
    jira_file = st.file_uploader("Jira CSV", type=["csv"])
with upload_columns[1]:
    raid_file = st.file_uploader("RAID CSV", type=["csv"])
with upload_columns[2]:
    release_file = st.file_uploader("Release CSV", type=["csv"])

selected_scenario_label = st.selectbox("Sample scenario", list(SAMPLE_SCENARIOS))
use_samples = st.button("Load Selected Sample Scenario", type="primary")
dataframes = None

try:
    if use_samples:
        scenario_key = SAMPLE_SCENARIOS[selected_scenario_label]
        st.session_state["sample_data"] = load_sample_data(BASE_DIR / "data", scenario_key)
        st.session_state["sample_scenario"] = scenario_key
        dataframes = st.session_state["sample_data"]
    elif all([jira_file, raid_file, release_file]):
        st.session_state.pop("sample_data", None)
        st.session_state.pop("sample_scenario", None)
        dataframes = {
            "jira": load_csv(jira_file),
            "raid": load_csv(raid_file),
            "release": load_csv(release_file),
        }
    elif "sample_data" in st.session_state:
        dataframes = st.session_state["sample_data"]
    elif any([jira_file, raid_file, release_file]):
        st.warning("Upload all three CSV files to run the analysis.")
except (OSError, UnicodeDecodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as error:
    st.error(f"Could not load CSV data: {error}")

active_scenario = st.session_state.get("sample_scenario")
if dataframes is not None and active_scenario in SCENARIO_NOTES:
    st.caption(SCENARIO_NOTES[active_scenario])

if dataframes is None:
    st.info("Upload all three CSV files or load the sample data to begin.")
    st.stop()

validation_results = validate_all(dataframes)
st.subheader("Validation")
validation_columns = st.columns(3)
data_labels = {"jira": "Jira", "raid": "RAID", "release": "Release"}
for column, data_type in zip(validation_columns, ("jira", "raid", "release")):
    result = validation_results[data_type]
    with column:
        st.metric(f"{data_labels[data_type]} rows", result["row_count"])
        if result["valid"]:
            st.success("Validation passed")
        else:
            st.error("Validation failed")
            for error in result["errors"]:
                st.write(error)

if not all(result["valid"] for result in validation_results.values()):
    st.error("Fix the validation errors before analysis can run.")
    st.stop()

risk_findings = analyze_risks(dataframes["jira"], dataframes["raid"], dataframes["release"])
dependency_findings = analyze_dependencies(dataframes["jira"], dataframes["raid"])
governance_findings = analyze_governance(dataframes["jira"], dataframes["raid"], dataframes["release"])
all_findings = risk_findings + dependency_findings + governance_findings
score_result = calculate_health_score(all_findings)
recommendations = recommend_actions(all_findings)
executive_summary = generate_executive_summary(score_result, all_findings)
ai_brief_result = {"enabled": False, "brief": None, "error": None}
ai_executive_brief = None
if enable_ai_brief:
    with st.spinner("Generating AI-enhanced executive brief..."):
        ai_brief_result = generate_ai_executive_brief(
            score_result,
            executive_summary,
            all_findings,
            recommendations,
            enabled=True,
        )
    if ai_brief_result.get("enabled"):
        ai_executive_brief = ai_brief_result.get("brief")

markdown_report = build_markdown_report(
    score_result,
    executive_summary,
    risk_findings,
    dependency_findings,
    governance_findings,
    recommendations,
    ai_executive_brief=ai_executive_brief,
)

st.subheader("Executive summary")
score_column, status_column, finding_column, action_column = st.columns(4)
score_column.metric("Delivery Health Score", f"{score_result['score']}/100")
status_column.metric("Health Status", score_result["status"])
finding_column.metric("Total Findings", len(all_findings))
action_column.metric("Priority Actions", len(recommendations))
st.caption(
    "The score uses the highest-severity finding for each evidence item, then applies category caps."
)

if score_result["status"] == "Critical":
    st.error(score_result["status_summary"])
elif score_result["status"] in {"At Risk", "Watch"}:
    st.warning(score_result["status_summary"])
else:
    st.success(score_result["status_summary"])

st.markdown(f"**{executive_summary['headline']}**")
st.write(executive_summary["summary"])
if executive_summary["leadership_attention"]:
    st.write("Leadership attention:")
    for action in executive_summary["leadership_attention"]:
        st.markdown(f"- {action}")
st.info(f"Decision required: {executive_summary['decision_required']}")

if enable_ai_brief:
    if ai_executive_brief:
        st.subheader("AI-Enhanced Executive Brief")
        st.caption(
            "AI enhancement uses deterministic evidence-backed findings and does not alter "
            "the score, findings or evidence keys."
        )
        st.markdown(f"**{ai_executive_brief.get('headline', '')}**")
        st.write(ai_executive_brief.get("executive_briefing", ""))
        leadership_actions = ai_executive_brief.get("leadership_actions", [])
        if leadership_actions:
            st.write("Leadership actions:")
            for action in leadership_actions:
                st.markdown(f"- {action}")
        st.info(f"Decision required: {ai_executive_brief.get('decision_required', '')}")
        st.caption(ai_executive_brief.get("confidence_note", ""))
    elif ai_brief_result.get("error") == "OPENAI_API_KEY not configured":
        st.warning("AI-enhanced brief unavailable: OPENAI_API_KEY not configured.")
    else:
        st.warning(f"AI-enhanced brief unavailable: {ai_brief_result.get('error')}")

st.write("Download an evidence-backed executive report for governance review or leadership discussion.")
st.download_button(
    label="Download Executive Report",
    data=markdown_report,
    file_name="delivery_chief_of_staff_report.md",
    mime="text/markdown",
)

st.subheader("Score breakdown")
deduction_column, category_column = st.columns(2)
with deduction_column:
    st.write("Evidence-based deductions")
    st.dataframe(pd.DataFrame(score_result["deductions"]), width="stretch", hide_index=True)
with category_column:
    st.write("Category deduction totals")
    category_rows = [
        {"category_group": group, "points": points}
        for group, points in score_result["category_totals"].items()
    ]
    st.dataframe(pd.DataFrame(category_rows), width="stretch", hide_index=True)
if score_result["capped_categories"]:
    st.caption(f"Capped categories: {', '.join(score_result['capped_categories'])}")


def highest_priority_concern(outputs: list[dict], field: str = "finding") -> str:
    """Return the highest-severity output text while preserving stable order."""
    if not outputs:
        return "No material concern identified"
    ordered = sorted(
        enumerate(outputs),
        key=lambda item: (
            SEVERITY_PRIORITY.get(str(item[1].get("severity", "Low")).title(), 4),
            item[0],
        ),
    )
    return str(ordered[0][1].get(field) or "No material concern identified")


st.subheader("Agent Workflow Trace")
st.caption("Deterministic trace of the specialist analysis completed for this review.")
agent_trace = [
    {
        "Agent": "Risk Agent",
        "Purpose": "Detect material delivery and release risks",
        "Inputs analysed": "Jira, RAID, Release",
        "Outputs generated": f"{len(risk_findings)} findings",
        "Highest-priority concern": highest_priority_concern(risk_findings),
    },
    {
        "Agent": "Dependency Agent",
        "Purpose": "Identify dependencies, blockers, and ownership gaps",
        "Inputs analysed": "Jira, RAID",
        "Outputs generated": f"{len(dependency_findings)} findings",
        "Highest-priority concern": highest_priority_concern(dependency_findings),
    },
    {
        "Agent": "Governance Agent",
        "Purpose": "Review ownership, mitigations, criteria, and release controls",
        "Inputs analysed": "Jira, RAID, Release",
        "Outputs generated": f"{len(governance_findings)} findings",
        "Highest-priority concern": highest_priority_concern(governance_findings),
    },
    {
        "Agent": "Recommendation Agent",
        "Purpose": "Prioritise distinct, evidence-backed actions",
        "Inputs analysed": "All agent findings",
        "Outputs generated": f"{len(recommendations)} recommendations",
        "Highest-priority concern": highest_priority_concern(recommendations, "recommended_action"),
    },
    {
        "Agent": "Executive Summary Agent",
        "Purpose": "Convert scored evidence into a leadership narrative",
        "Inputs analysed": "Health score, findings, category totals",
        "Outputs generated": "1 executive summary",
        "Highest-priority concern": executive_summary.get("headline", "No material concern identified"),
    },
]
st.dataframe(pd.DataFrame(agent_trace), width="stretch", hide_index=True)

st.subheader("Business Impact Estimate")
st.caption("Impact hypothesis for a typical programme governance review; validate through a pilot.")
with st.container(border=True):
    impact_left, impact_right = st.columns(2)
    with impact_left:
        st.markdown("**Manual review effort avoided**")
        st.write("Estimated at 3–5 hours per programme review.")
        st.markdown("**Governance checks automated**")
        st.write(
            "Ownership, mitigation, acceptance criteria, dependency ownership, and release readiness."
        )
    with impact_right:
        st.markdown("**Decision acceleration**")
        st.write("Executive report generated in under 1 minute.")
        st.markdown("**Primary value**")
        st.write("Earlier intervention on delivery risk with evidence-backed recommendations.")


def display_findings(title: str, findings: list[dict]) -> None:
    st.subheader(title)
    if findings:
        st.dataframe(pd.DataFrame(findings)[DISPLAY_COLUMNS], width="stretch", hide_index=True)
    else:
        st.success(f"No {title.lower()} identified.")


display_findings("Top Risks", risk_findings)
display_findings("Dependency Findings", dependency_findings)
display_findings("Governance Findings", governance_findings)
display_findings("Recommended Actions", recommendations)

with st.expander("Evidence Trail"):
    st.write("All findings retained for traceability, including findings deduplicated from scoring.")
    if all_findings:
        st.dataframe(pd.DataFrame(all_findings)[DISPLAY_COLUMNS], width="stretch", hide_index=True)
    else:
        st.success("No findings were generated from the supplied evidence.")
