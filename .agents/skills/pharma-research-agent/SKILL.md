---
name: pharma-research-agent
description: Use when researching biomedical, pharmaceutical, clinical, drug safety, target landscape, drug comparison, FAERS, PubMed, ClinicalTrials, openFDA, or multi-source literature topics and producing evidence-backed Markdown reports in Codex.
---

# Pharma Research Agent

## Overview

Use this skill to run an internal Codex-native pharmaceutical research workflow. It coordinates a multi-role analysis team, selects the right data sources, and produces a Markdown report with source IDs, evidence tables, and clearly separated findings.

## Workflow

1. Clarify the research topic only when the task lacks the target, drug, indication, comparator, or analysis type.
2. Classify the task as one or more research modes:
   - `target-landscape`: target mechanism, indication map, pipeline and company landscape.
   - `drug-clinical-comparison`: trial design, endpoints, efficacy, safety, label evidence.
   - `adverse-event-analysis`: FAERS signal, label reactions, literature safety evidence.
3. Read only the needed reference files:
   - Always read `references/role-cards.md`.
   - Read `references/report-templates.md` before drafting the final report.
   - Read `references/data-source-map.md` before searching or planning data retrieval.
   - Read `references/evidence-quality-rules.md` before ranking or qualifying conclusions.
4. Create a short research plan with roles, data sources, search terms, and expected sections.
5. Retrieve or request data through available tools. If no MCP tools are installed, use safe web/API access or document that the MCP call is planned but unavailable.
6. Deduplicate entities and sources by stable IDs where possible: PMID, PMCID, DOI, NCT ID, openFDA endpoint URL, registry ID, or uploaded file path.
7. Draft the report using the matching template. Save to `reports/YYYY-MM-DD-topic-research.md` when asked to create files.
8. End with an evidence appendix listing all used sources, retrieval date, ID, title/name, and how each source contributed.

## Output Rules

- Prefer concise tables for evidence, trial comparisons, and adverse-event summaries.
- Separate `直接证据`, `综合判断`, and `待补充证据`.
- Do not invent unavailable values. Use `未检索到` or `待补充`.
- Preserve source identifiers in every key table.
- For internal use, do not add public-facing medical disclaimer text unless the user asks.

## Common Mistakes

- Do not load every reference file for a simple task; use progressive disclosure.
- Do not treat FAERS report counts as causality.
- Do not merge literature sources without DOI/PMID/title-level deduplication.
- Do not produce a polished conclusion without showing the evidence table that supports it.
