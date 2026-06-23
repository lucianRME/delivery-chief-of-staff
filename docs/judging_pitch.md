# Judging Pitch

## One-Line Pitch

Delivery Chief of Staff is an agentic AI workflow that turns delivery artefacts into executive-ready governance insight.

## Problem

Enterprise delivery reviews are manual, inconsistent, and time-consuming. Programme teams reconcile Jira exports, RAID logs, and release plans by hand, often under deadline pressure. Important signals can be buried across artefacts, governance checks vary between reviewers, and leadership receives information after the window for low-cost intervention has narrowed.

The result is avoidable preparation effort, uneven assurance, and decisions made without a clear line from executive conclusion to source evidence.

## Solution

Delivery Chief of Staff is a local Streamlit application that ingests Jira, RAID, and release CSVs and automatically produces:

- A deduplicated, explainable Delivery Health Score.
- Prioritised risk, dependency, governance, and release-readiness findings.
- Evidence-backed recommended actions.
- A concise executive summary and leadership decision prompt.
- A downloadable Markdown report with a complete audit trail.

The MVP uses transparent, deterministic rules. It is reliable in a live demo, easy to inspect, and does not depend on cloud infrastructure or external APIs.

## Why Agentic AI

The workflow separates delivery reasoning into specialised agents with distinct responsibilities:

- **Risk Agent:** detects blocked work, high-priority exposure, material RAID items, and at-risk milestones.
- **Dependency Agent:** identifies dependencies, blockers, missing dependency ownership, and links to priority work.
- **Governance Agent:** reviews ownership, mitigations, acceptance criteria, approvals, and release controls.
- **Recommendation Agent:** deduplicates and prioritises the actions leadership should take next.
- **Executive Summary Agent:** converts the scored evidence into a concise, deterministic leadership narrative.

This separation makes the analysis modular, explainable, and extensible. Each agent contributes a bounded form of reasoning while retaining a common evidence contract.

## Business Value

- Reduced manual review effort across Jira, RAID, and release artefacts.
- Earlier detection of delivery and release-readiness risks.
- Consistent governance assessment across programmes and reviewers.
- Improved leadership decision-making through prioritised, action-oriented insight.
- An auditable evidence trail from every conclusion back to its source record.

## Why This Can Win

- **Enterprise relevance:** delivery assurance and governance are recurring problems across large organisations.
- **Measurable impact:** preparation time, detected gaps, and decision turnaround can all be tracked.
- **Realistic implementation:** the MVP works with the CSV exports teams already use.
- **Local demo reliability:** no network, cloud service, or external API is required.
- **Low technical risk:** the architecture is simple, deterministic, and easy to test.
- **Strong executive storytelling:** the demo moves from fragmented delivery data to a decision-ready report in under a minute.

## MVP Scope

### Included

- CSV ingestion and validation.
- Local Streamlit application.
- Deterministic specialist agents.
- Deduplicated and capped delivery health scoring.
- Prioritised recommendations.
- Executive summary and decision prompt.
- Downloadable Markdown executive report.
- At Risk and Critical demonstration scenarios.

### Intentionally Excluded for the MVP

- Jira API integration.
- Cloud deployment.
- Authentication and access control.
- Database persistence.
- PDF generation.
- Complex multi-agent frameworks.

These exclusions keep the hackathon implementation focused on proving user value and analytical credibility.

## Future Roadmap

- Jira integration for scheduled or on-demand analysis.
- Portfolio-level reporting across multiple programmes.
- PowerPoint and PDF export for governance packs.
- OpenAI-enhanced narrative with deterministic evidence grounding.
- Integration with established governance and approval workflows.
