---
name: pharma-research-agent
description: Use when researching biomedical, pharmaceutical, clinical, drug safety, target landscape, early drug assets, nonclinical evidence, target validation, PubMed, ClinicalTrials, openFDA, or multi-source literature topics and producing evidence-backed Markdown reports in Codex.
---

# Pharma Research Agent

## Overview

Use this skill to run an internal Codex-native pharmaceutical research workflow. It routes each question to the smallest relevant role team, selects the right data sources, and produces a Markdown report with source IDs, evidence tables, explicit uncertainty, and clearly separated findings.

## Workflow

1. Run the scope gate before searching. Clarify the research topic when the task lacks the target, drug, indication, comparator, analysis type, treatment line, population, regimen, route, geography, or endpoint priority. If the user asks the team to decide, state the chosen scope explicitly and keep excluded scenarios as background only.
2. Classify the task as one or more research modes:
   - `target-landscape`: target mechanism, indication map, pipeline and company landscape.
   - `drug-clinical-comparison`: trial design, endpoints, efficacy, safety, label evidence.
   - `adverse-event-analysis`: FAERS signal, label reactions, literature safety evidence.
   - `target-validation`: disease biology, human evidence, expression, pathway, genetic and translational support for a target.
   - `modality-feasibility`: whether the proposed modality fits the target, biology, tissue access, delivery route, and safety constraints.
   - `nonclinical-evidence-review`: in vitro, in vivo, PK/PD, biomarker, toxicology, and model translatability review.
   - `early-asset-diligence`: third-party feasibility assessment for an early drug project, including defects, failure paths, and required de-risking experiments.
3. Read only the needed reference files:
   - Always read `references/role-cards.md` for shared coordination rules.
   - For `target-landscape`, `drug-clinical-comparison`, or `adverse-event-analysis`, read `references/data-source-map.md`, `references/evidence-quality-rules.md`, and `references/report-templates.md` as needed.
   - For `target-validation`, `modality-feasibility`, `nonclinical-evidence-review`, or `early-asset-diligence`, read only the early-project references needed for the task: `references/early-asset-role-cards.md`, `references/early-asset-data-source-map.md`, `references/early-asset-evidence-rules.md`, and `references/early-asset-report-template.md`.
   - Read `references/scope-clarification-rules.md` before clinical comparisons or any broad/ambiguous oncology question.
4. Create a short research plan with selected roles, data sources, search terms, expected sections, and explicit exclusion boundaries.
5. For drug comparisons, first identify direct head-to-head trials for the exact scope. If no mature direct result exists, define the indirect evidence set and label it as cross-trial comparison.
6. For early assets, first decompose the project hypothesis into target validity, modality fit, nonclinical pharmacology, PK/PD, toxicology, competitive/precedent evidence, IP/differentiation, and failure paths. Search for both supporting and opposing evidence.
7. Retrieve or request data through available tools. If no MCP tools are installed, use safe web/API access or document that the MCP call is planned but unavailable.
8. Deduplicate entities and sources by stable IDs where possible: PMID, PMCID, DOI, NCT ID, openFDA endpoint URL, registry ID, accession ID, database ID, patent number, URL, or uploaded file path.
9. Draft the report using the matching template. Save to `reports/YYYY-MM-DD-topic-research.md` when asked to create files.
10. End with an evidence appendix listing all used sources, retrieval date, ID, title/name, and how each source contributed.

## Output Rules

- Prefer concise tables for evidence, trial comparisons, and adverse-event summaries.
- Separate `直接证据`, `综合判断`, and `待补充证据`.
- Do not invent unavailable values. Use `未检索到` or `待补充`.
- Preserve source identifiers in every key table.
- Preserve the final scope statement near the top of every clinical comparison report, including population, line of therapy, regimen, route, comparator, geography, and endpoint priority when available.
- For early-asset reports, include both `支持证据` and `反对证据`; include `关键缺陷与失败路径`, `建议补充实验`, and a `第三方结论`.
- For internal use, do not add public-facing medical disclaimer text unless the user asks.

## Common Mistakes

- Do not load every reference file for a simple task; use progressive disclosure.
- Do not treat FAERS report counts as causality.
- Do not merge literature sources without DOI/PMID/title-level deduplication.
- Do not mix populations, lines of therapy, monotherapy vs combination therapy, routes, or post-progression settings into the main comparison unless the report explicitly labels them as background or indirect evidence.
- Do not produce a polished conclusion without showing the evidence table that supports it.
- Do not treat early nonclinical activity as clinical proof. Identify model limits, exposure limits, species differences, and missing de-risking experiments.
- Do not let a positive company narrative stand alone. Search for failed precedents, weak translation assumptions, tissue-expression risk, and modality mismatch.
