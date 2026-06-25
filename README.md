# Delivery Chief of Staff

**Agentic Operations Governance Assistant for Banking Delivery Reviews**

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

## Official Hackathon Use Case Alignment

Delivery Chief of Staff aligns with the official hackathon use case:

* Industry: BFSI
* Sector: Banking
* Vertical: Banking Operations
* Area: Middle & Back Office Operations
* Scenario: Shared services, operations work orchestration
* Theme: Operations modernisation via orchestration and knowledge
* Primary use case: Operations work orchestration with human-in-loop controls

The MVP supports this use case by automating delivery governance review across Jira, RAID and release artefacts. It turns work artefacts into validated inputs, runs control checks, detects exceptions, routes recommended actions to accountable leaders and produces evidence-backed reporting.

| Official value-chain step | Delivery Chief of Staff capability |
|---|---|
| Work intake & classification | CSV ingestion and validation of Jira, RAID and release artefacts |
| Data/document extraction | Structured extraction from delivery artefacts |
| Policy/control checks | Governance Agent checks ownership, mitigations, acceptance criteria and release readiness |
| Task routing & approvals | Recommendation Agent proposes human-in-loop leadership actions |
| Execution across systems | Provides action-ready outputs for execution in existing delivery and governance tools |
| Exception handling | Risk, dependency, blocker and governance gap detection |
| Reporting & evidence | Dashboard, evidence trail and downloadable executive report |
| Continuous improvement | Repeatable findings, score deductions and evidence model support trend analysis in future iterations |

This positions the MVP as an agentic operations governance assistant for banking delivery and shared services reviews.

## Human-in-the-loop Controls

Delivery Chief of Staff is designed to support governance decisions, not automate them.

* Agents identify risks, dependencies, governance gaps and release readiness issues.
* The system recommends actions but does not automatically approve delivery decisions.
* Delivery leaders remain accountable for decisions, escalations and approvals.
* Evidence keys support human review, auditability and governance confidence.
* This is appropriate for banking operations where governance decisions require oversight.

## Operational Guardrails

Delivery Chief of Staff is designed for human-in-loop banking operations governance.

* Deterministic scoring remains the source of truth.
* Findings and recommendations are evidence-backed only.
* OpenAI, if enabled, is narrative-only and does not alter the source-of-truth assessment.
* The app does not perform autonomous release approvals or system execution.
* Recommendations require human review and approval.
* The evidence trail supports auditability and governance confidence.

## Why this matters

Delivery Chief of Staff is designed for enterprise delivery governance, programme assurance and release readiness reviews.

It helps teams move from manual review packs to faster, more consistent, evidence-backed leadership insight.

Estimated impact hypotheses:

* Reduce weekly delivery review preparation effort by 30–50%.
* Reduce time to identify governance gaps from hours to minutes.
* Improve consistency of RAID, dependency and release readiness checks.
* Accelerate leadership decision-making with evidence-backed recommendations.
* Improve auditability through stable evidence keys and traceable findings.

## Before and after

### Before Delivery Chief of Staff

A typical enterprise delivery review may require manual inspection of:

* Jira delivery status
* Blocked or ageing work items
* RAID log risks, issues and dependencies
* Missing owners or mitigations
* Release readiness controls
* Business approvals
* Rollback and communications readiness
* Executive summary preparation

This can take several hours and may still result in inconsistent conclusions.

### After Delivery Chief of Staff

A programme manager or delivery leader can upload Jira, RAID and release artefacts and receive:

* Delivery Health Score
* Executive summary
* Top risks
* Dependency and blocker analysis
* Governance findings
* Recommended leadership actions
* Score deductions
* Evidence and audit trail
* Downloadable executive report

The result is a faster, more consistent and more auditable delivery governance review.

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
* No external API dependency for the core assessment
* Reliable hackathon demo execution

The optional OpenAI enhancement improves executive narrative wording only. The underlying Delivery Health Score, findings and evidence model remain deterministic for governance trust.

## Optional OpenAI Enhancement

The app works without OpenAI. The deterministic governance engine remains the source of truth for the Delivery Health Score, findings, recommendations and evidence keys.

OpenAI can optionally generate a polished executive brief from the existing evidence-backed findings. This is a narrative enhancement only:

* OpenAI does not alter the Delivery Health Score.
* OpenAI does not alter findings or evidence keys.
* OpenAI does not invent risks, evidence or unsupported actions.
* Delivery leaders remain accountable for human-in-loop review and approval.

To enable the optional AI-enhanced executive brief, set `OPENAI_API_KEY` in your environment and use the sidebar checkbox in the app:

```bash
export OPENAI_API_KEY="your-key-here"
streamlit run app.py
```

You can also place `OPENAI_API_KEY` in a local `.env` file. Do not commit `.env` or API keys.

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

## Recommended demo flow

Use the default At Risk Programme scenario for the main demo.

1. Select **At Risk Programme**.
2. Click **Load Selected Sample Scenario**.
3. Review the Delivery Health Score.
4. Review the Agent Workflow Trace.
5. Review the top risks, dependencies, governance findings and recommendations.
6. Open the evidence and audit trail.
7. Download the executive report.

Suggested demo message:

> Delivery Chief of Staff reduces enterprise delivery review preparation from hours to under a minute by using specialised agents to analyse Jira, RAID and release artefacts, generate an evidence-backed Delivery Health Score, prioritise leadership actions and produce a downloadable executive governance report.

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

## Scoring model

The Delivery Health Score starts at 100 and applies deductions for evidence-backed delivery findings.

The scoring model is designed to be explainable and audit-friendly:

* Findings are linked to stable evidence keys.
* Duplicate findings against the same evidence item are deduplicated.
* Category caps prevent one issue type from overwhelming the score.
* Score deductions are displayed in the dashboard and report.
* The score is supported by an evidence and audit trail.

This avoids a black-box assessment and allows delivery leaders to understand why a programme is rated Healthy, Watch, At Risk or Critical.

## Evidence model

Each finding includes a structured evidence contract:

* Severity
* Category
* Category group
* Finding
* Evidence
* Evidence key
* Source
* Recommended action

Example evidence keys:

* `jira:PROG-104`
* `raid:R-002`
* `release:REL-1.2:UAT Sign-off`

This evidence model supports explainability, governance review and leadership trust.

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

## Documentation

Additional documentation is available under `docs/`:

* [Agent Architecture](docs/agents.md)
* [Demo Script](docs/demo_script.md)
* [Judging Pitch](docs/judging_pitch.md)
* [Business Impact](docs/business_impact.md)
* [Submission Alignment](docs/submission_alignment.md)

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
* Required OpenAI API key for the normal demo flow

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

## Submission note

This MVP was intentionally designed for fast, reliable local demonstration within the hackathon timeframe.

It focuses on:

* Enterprise relevance
* Measurable business impact
* Agentic workflow clarity
* Evidence-backed recommendations
* Low technical risk
* High demo reliability
