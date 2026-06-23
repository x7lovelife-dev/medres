# MCP 工具契约

## search_literature

```json
{
  "name": "search_literature",
  "input": {
    "query": "PD-1 gastric cancer immunotherapy",
    "sources": ["pubmed", "pmc", "europe_pmc", "crossref", "openalex", "semantic_scholar", "biorxiv", "medrxiv"],
    "date_range": { "from": "2018-01-01", "to": "2026-06-23" },
    "max_results": 50
  },
  "output_item": {
    "source": "pubmed",
    "id": "PMID:00000000",
    "doi": "10.xxxx/example",
    "title": "Title",
    "authors": ["Author A"],
    "journal_or_server": "Journal",
    "publication_date": "2025-01-01",
    "abstract": "Abstract text",
    "url": "https://example.org",
    "dedupe_key": "doi-or-normalized-title",
    "evidence_note": "Why this item matters"
  }
}
```

失败处理：某个来源失败时保留其他来源结果，并在 `warnings` 里标出失败来源和原因。

## fetch_publication_detail

```json
{
  "name": "fetch_publication_detail",
  "input": {
    "ids": ["PMID:00000000", "10.xxxx/example"],
    "source": "pubmed"
  },
  "output_item": {
    "id": "PMID:00000000",
    "doi": "10.xxxx/example",
    "title": "Title",
    "abstract": "Abstract text",
    "mesh_terms": ["Neoplasms"],
    "full_text_available": true,
    "full_text_url": "https://pmc.ncbi.nlm.nih.gov/articles/example/",
    "references": []
  }
}
```

## search_clinical_trials

```json
{
  "name": "search_clinical_trials",
  "input": {
    "condition": "gastric cancer",
    "intervention": "nivolumab",
    "phase": ["PHASE2", "PHASE3"],
    "status": ["RECRUITING", "COMPLETED"]
  },
  "output_item": {
    "nct_id": "NCT00000000",
    "title": "Study title",
    "phase": ["PHASE3"],
    "condition": ["Gastric Cancer"],
    "intervention": ["Nivolumab"],
    "sponsor": "Sponsor",
    "enrollment": 500,
    "primary_outcomes": ["Overall survival"],
    "status": "COMPLETED",
    "start_date": "2021-01",
    "completion_date": "2025-01",
    "url": "https://clinicaltrials.gov/study/NCT00000000"
  }
}
```

## search_adverse_events

```json
{
  "name": "search_adverse_events",
  "input": {
    "drug": "nivolumab",
    "reaction": "pneumonitis",
    "date_range": { "from": "2018-01-01", "to": "2026-06-23" }
  },
  "output_item": {
    "drug": "nivolumab",
    "reaction": "PNEUMONITIS",
    "count": 100,
    "serious_count": 50,
    "yearly_counts": { "2024": 20, "2025": 25 },
    "query_url": "https://api.fda.gov/drug/event.json?...",
    "source": "openFDA FAERS"
  }
}
```

## search_drug_labels

```json
{
  "name": "search_drug_labels",
  "input": {
    "drug": "nivolumab"
  },
  "output_item": {
    "drug": "nivolumab",
    "brand_names": ["OPDIVO"],
    "indications_and_usage": ["..."],
    "warnings": ["..."],
    "adverse_reactions": ["..."],
    "dosage_and_administration": ["..."],
    "set_id": "label-set-id",
    "source": "openFDA Drug Label"
  }
}
```

## normalize_entities

```json
{
  "name": "normalize_entities",
  "input": {
    "text": "Keytruda and pembrolizumab in MSI-H gastric cancer",
    "entity_types": ["drug", "target", "condition", "reaction"]
  },
  "output_item": {
    "text": "Keytruda",
    "type": "drug",
    "normalized_name": "pembrolizumab",
    "aliases": ["Keytruda"],
    "confidence": 0.95
  }
}
```

## rank_evidence

```json
{
  "name": "rank_evidence",
  "input": {
    "research_question": "PD-1 competition in gastric cancer",
    "items": []
  },
  "output_item": {
    "source_id": "PMID:00000000",
    "evidence_type": "randomized clinical trial",
    "rank": 1,
    "conclusion_label": "直接证据",
    "reason": "Phase 3 trial directly evaluates the intervention in target indication."
  }
}
```
