# Agent Architecture

## Overview

Delivery Chief of Staff uses a lightweight, deterministic agent workflow to convert familiar delivery artefacts into executive governance insight. The workflow analyses three inputs:

- Jira export CSV.
- RAID log CSV.
- Release plan CSV.

It produces:

- A Delivery Health Score.
- Risk findings.
- Dependency findings.
- Governance findings.
- Recommended actions.
- An executive summary.
- An evidence and audit trail.

The agents share a consistent evidence model, allowing an executive conclusion to be traced back to the source delivery record.

## Agent Workflow

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

The Validation Layer confirms that each CSV contains the required schema before analysis begins. Each subsequent agent has a specific delivery-governance responsibility. Findings are combined for scoring, recommendations, executive summarisation, dashboard presentation, and report generation.

## Agent Responsibilities

### Risk Agent

- Detects blocked work.
- Identifies unfinished Critical and High-priority items.
- Flags open high-impact RAID risks and issues.
- Identifies required escalations.
- Detects at-risk release milestones.

### Dependency Agent

- Detects documented blockers and dependencies.
- Identifies missing dependency owners.
- Reviews RAID dependencies.
- Highlights dependencies linked to high-priority work.

### Governance Agent

- Checks for missing Jira assignees.
- Detects missing acceptance criteria.
- Identifies missing RAID owners and mitigations.
- Reviews milestone ownership, rollback plans, approvals, and release entry and exit criteria.

### Recommendation Agent

- Deduplicates repeated recommended actions.
- Prioritises actions by severity.
- Retains source and evidence references.
- Focuses the dashboard on the actions with the greatest delivery impact.

### Executive Summary Agent

- Uses the Delivery Health Score and status.
- Identifies the leading risk themes from scored findings.
- Selects evidence-backed leadership actions.
- Produces a deterministic leadership-level summary and decision prompt.

## Finding Contract

Every analysis agent returns findings using the same eight-field contract:

- `severity`
- `category`
- `category_group`
- `finding`
- `evidence`
- `evidence_key`
- `source`
- `recommended_action`

Example:

```json
{
  "severity": "High",
  "category": "Blocked Issue",
  "category_group": "Delivery Risk",
  "finding": "High-priority issue PROG-104 is blocked.",
  "evidence": "issue_key=PROG-104; blocker=Waiting for security review",
  "evidence_key": "jira:PROG-104",
  "source": "Jira",
  "recommended_action": "Assign a resolution owner and confirm a recovery date."
}
```

## Evidence and Audit Trail

Every finding links to a stable evidence key representing its source record. Examples include:

- `jira:PROG-104`
- `raid:R-002`
- `release:REL-1.2:UAT Sign-off`

The scoring model uses these keys to prevent the same source item from being penalised repeatedly when multiple agents identify related concerns. The complete set of findings remains available in the audit trail even when scoring is deduplicated.

This evidence model supports:

- **Explainability:** users can see why a conclusion was reached.
- **Auditability:** findings can be traced to a specific delivery record.
- **Governance review:** reviewers can validate evidence before agreeing an action.
- **Leadership trust:** executive summaries remain connected to observable programme data.

## Why Deterministic Agents for the MVP

Deterministic agents were an intentional choice for this 10-day hackathon MVP. They provide:

- Reliable live demonstrations.
- Transparent and auditable rules.
- No external API dependency.
- Fully local execution.
- Predictable scoring and recommendations.
- Low technical and operational risk.

This approach proves the core workflow and business value without making governance conclusions dependent on probabilistic model output.

## Future LLM Enhancement

An LLM could later enhance:

- Executive narrative generation.
- Natural-language questions and answers about programme evidence.
- Stakeholder-specific summaries.
- Recommendation wording and communication style.

The underlying evidence contract, source references, validation, and scoring model should remain deterministic. This preserves explainability and governance trust while allowing richer narrative capabilities around the verified evidence.
