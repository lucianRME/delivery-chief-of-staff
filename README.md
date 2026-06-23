# Delivery Chief of Staff

**Delivery Chief of Staff** is a local Streamlit MVP that acts as an executive delivery advisor for enterprise programmes.

It reviews Jira exports, RAID logs and release plans, then converts them into an evidence-backed delivery health assessment, governance findings, prioritised leadership actions and a downloadable executive report.

## One-line pitch

Delivery Chief of Staff turns delivery artefacts into executive-ready governance insight in under a minute.

## Problem

Enterprise delivery reviews are often manual, time-consuming and inconsistent.

Programme managers, delivery managers and PMO teams spend significant time reviewing Jira boards, RAID logs, release plans and governance artefacts to identify risks, dependencies, ownership gaps, mitigation gaps and release readiness concerns.

This creates several problems:

* Delivery risks may be identified late.
* Governance checks vary by programme or reviewer.
* Leadership updates can lack consistent evidence.
* Executive review preparation can take hours.
* RAID, dependency and release readiness gaps can be missed.

## Solution

Delivery Chief of Staff uses a lightweight agentic workflow to analyse delivery artefacts and produce an executive delivery health view.

The MVP supports:

* Jira export CSV analysis
* RAID log CSV analysis
* Release plan CSV analysis
* Delivery Health Score
* Risk findings
* Dependency and blocker findings
* Governance findings
* Prioritised recommended actions
* Deterministic executive summary
* Evidence and audit trail
* Downloadable Markdown executive report

All processing runs locally in memory. The application has no database, backend service, cloud deployment or Jira API dependency.

## Why this matters

Delivery Chief of Staff is designed for enterprise delivery governance, programme assurance and release readiness reviews.

It helps teams move from manual review packs to faster, more consistent, evidence-backed leadership insight.

Estimated impact hypotheses:

* Reduce weekly delivery review preparation effort by 30–50%.
* Reduce time to identify governance gaps from hours to minutes.
* Improve consistency of RAID, dependency and release readiness checks.
* Accelerate leadership decision-making with evidence-backed recommendations.
* Improve auditability through stable evidence keys and traceable findings.

## Agent Architecture

Delivery Chief of Staff uses a deterministic agent workflow. Each agent performs a focused delivery governance task and passes structured findings into the next stage.

Workflow:

```text
CSV Inputs
→ Validation Layer
→ Risk Agent
→ Dependency Agent
→ Governance Agent
→ Recommendation Agent
→ Executive Summary Agent
→ Dashboard and Executive Report
```

Agents:

* **Risk Agent** detects blocked work, high-priority unfinished items, high-impact RAID risks, escalations and at-risk release milestones.
* **Dependency Agent** detects blockers, dependencies, missing dependency owners and dependencies linked to high-priority work.
* **Governance Agent** checks missing assignees, missing acceptance criteria, missing RAID owners, missing mitigations and release readiness controls.
* **Recommendation Agent** deduplicates and prioritises actions based on severity, evidence and delivery impact.
* **Executive Summary Agent** generates a leadership-level summary using the health score, findings and recommended actions.

See [docs/agents.md](docs/agents.md) for the full agent workflow, responsibilities and evidence model.

## Why deterministic agents?

The MVP intentionally uses deterministic agents for the core assessment.

This supports:

* Explainability
* Repeatability
* Auditability
* Local execution
* No external API dependency
* Reliable hackathon demo execution

A future OpenAI enhancement could improve executive narrative generation or natural-language Q&A, but the underlying Delivery Health Score, findings and evidence model should remain deterministic for governance trust.

## Demo scenarios

The app includes two one-click sample scenarios.

### At Risk Programme

The default demo scenario.

* Score: **63/100**
* Status: **At Risk**
* Narrative: A recoverable enterprise delivery scenario with targeted blockers, dependencies and readiness gaps alongside completed work.
* Recommended demo path: use this scenario first.

### Critical Programme

A severe delivery pressure scenario.

* Score: **40/100**
* Status: **Critical**
* Narrative: Multiple blocked items, unresolved risks and missing release controls require immediate executive intervention.

The original `jira_sample.csv`, `raid_sample.csv` and `release_sample.csv` filenames remain available and contain the default At Risk scenario for backward compatibility.

## Run locally

Python 3.10 or newer is recommended. Python 3.11 or 3.12 is preferred for demo reliability.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the URL printed by Streamlit.

Recommended demo flow:

1. Select **At Risk Programme**.
2. Click **Load Selected Sample Scenario**.
3. Review the Delivery Health Score.
4. Review the Agent Workflow Trace.
5. Review the top risks, dependencies, governance findings and recommendations.
6. Open the evidence and audit trail.
7. Download the executive report.

## Uploading custom CSVs

Users can also upload their own delivery artefacts:

1. Jira export CSV
2. RAID log CSV
3. Release plan CSV

The app validates required columns before analysis. Analysis only runs when a complete valid set of files is available.

## Expected CSV columns

The required schemas are represented by the headers in:

* `data/jira_sample.csv`
* `data/raid_sample.csv`
* `data/release_sample.csv`

Column names are trimmed and compared case-insensitively during loading. Values such as `Yes`, `No`, `High` and `At Risk` are handled case-insensitively by the analysis agents.

## Outputs

The dashboard provides:

* Delivery Health Score
* Health status
* Executive summary
* Agent Workflow Trace
* Business Impact Estimate
* Top risks
* Dependency and blocker findings
* Governance findings
* Recommended actions
* Score deductions
* Category deduction totals
* Evidence and audit trail
* Downloadable Markdown executive report

## Project structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── agents/
│   ├── risk_agent.py
│   ├── dependency_agent.py
│   ├── governance_agent.py
│   ├── recommendation_agent.py
│   └── executive_summary_agent.py
├── core/
│   ├── data_loader.py
│   ├── validators.py
│   ├── scoring.py
│   └── report_builder.py
├── data/
│   ├── jira_sample.csv
│   ├── raid_sample.csv
│   ├── release_sample.csv
│   ├── jira_sample_at_risk.csv
│   ├── raid_sample_at_risk.csv
│   ├── release_sample_at_risk.csv
│   ├── jira_sample_critical.csv
│   ├── raid_sample_critical.csv
│   └── release_sample_critical.csv
├── docs/
│   ├── agents.md
│   ├── demo_script.md
│   ├── judging_pitch.md
│   └── business_impact.md
├── reports/
└── tests/
```

## MVP scope

Included in the MVP:

* Local Streamlit app
* CSV upload
* Sample scenario loading
* Deterministic agent workflow
* Evidence-backed findings
* Deduplicated Delivery Health Score
* Executive summary
* Recommended actions
* Markdown report download
* Demo and judging documentation

Intentionally excluded from the MVP:

* Jira API integration
* Cloud deployment
* Authentication
* Database
* PDF generation
* PowerPoint generation
* Complex multi-agent frameworks
* Required OpenAI dependency

These exclusions are deliberate. The MVP prioritises demo reliability, enterprise relevance, low technical risk and completion within the hackathon timeframe.

## Future roadmap

Potential future enhancements include:

* Jira API integration
* Portfolio-level delivery reporting
* PDF or PowerPoint governance pack export
* OpenAI-enhanced executive narrative generation
* Natural-language Q&A over delivery findings
* Integration with enterprise governance workflows
* Historical trend analysis across delivery review cycles

## Hackathon positioning

Delivery Chief of Staff is not a generic dashboard.

It is an agentic delivery governance workflow that converts operational delivery artefacts into executive-ready recommendations with an evidence and audit trail.

The MVP demonstrates how agentic AI can improve enterprise delivery governance by reducing manual review effort, improving consistency and accelerating leadership decision-making.
