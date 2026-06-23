---
name: pharma-research-agent
description: Use when researching biomedical, pharmaceutical, clinical, drug safety, target landscape, drug comparison, FAERS, PubMed, ClinicalTrials, openFDA, or multi-source literature topics and producing evidence-backed Markdown reports in Codex.
---

# Pharma Research Agent

## Overview

Use this skill to run an internal Codex-native pharmaceutical research workflow. It coordinates a multi-role analysis team, selects the right data sources, and produces a Markdown report with source IDs, evidence tables, and clearly separated findings.

## Workflow

1. Run the scope gate before searching. Clarify the research topic when the task lacks the target, drug, indication, comparator, analysis type, treatment line, population, regimen, route, geography, or endpoint priority. If the user asks the team to decide, state the chosen scope explicitly and keep excluded scenarios as background only.
2. Classify the task as one or more research modes:
   - `target-landscape`: target mechanism, indication map, pipeline and company landscape.
   - `drug-clinical-comparison`: trial design, endpoints, efficacy, safety, label evidence.
   - `adverse-event-analysis`: FAERS signal, label reactions, literature safety evidence.
3. Read only the needed reference files:
   - Always read `references/role-cards.md`.
   - Read `references/report-templates.md` before drafting the final report.
   - Read `references/data-source-map.md` before searching or planning data retrieval.
   - Read `references/evidence-quality-rules.md` before ranking or qualifying conclusions.
   - Read `references/scope-clarification-rules.md` before clinical comparisons or any broad/ambiguous oncology question.
4. Create a short research plan with roles, data sources, search terms, and expected sections.
5. For drug comparisons, first identify direct head-to-head trials for the exact scope. If no mature direct result exists, define the indirect evidence set and label it as cross-trial comparison.
6. Retrieve or request data through available tools. If no MCP tools are installed, use safe web/API access or document that the MCP call is planned but unavailable.
7. Deduplicate entities and sources by stable IDs where possible: PMID, PMCID, DOI, NCT ID, openFDA endpoint URL, registry ID, or uploaded file path.
8. Draft the report using the matching template. Save to `reports/YYYY-MM-DD-topic-research.md` when asked to create files.
9. End with an evidence appendix listing all used sources, retrieval date, ID, title/name, and how each source contributed.

## Output Rules

- Prefer concise tables for evidence, trial comparisons, and adverse-event summaries.
- Separate `直接证据`, `综合判断`, and `待补充证据`.
- Do not invent unavailable values. Use `未检索到` or `待补充`.
- Preserve source identifiers in every key table.
- Preserve the final scope statement near the top of every clinical comparison report, including population, line of therapy, regimen, route, comparator, geography, and endpoint priority when available.
- For internal use, do not add public-facing medical disclaimer text unless the user asks.

## Common Mistakes

- Do not load every reference file for a simple task; use progressive disclosure.
- Do not treat FAERS report counts as causality.
- Do not merge literature sources without DOI/PMID/title-level deduplication.
- Do not mix populations, lines of therapy, monotherapy vs combination therapy, routes, or post-progression settings into the main comparison unless the report explicitly labels them as background or indirect evidence.
- Do not produce a polished conclusion without showing the evidence table that supports it.
