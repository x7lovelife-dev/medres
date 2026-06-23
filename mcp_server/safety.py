from __future__ import annotations

from datetime import date
from typing import Any, Mapping
from urllib.parse import urlencode

import requests


def search_drug_labels(
    drug: str,
    max_results: int = 5,
    base_url: str = "https://api.fda.gov/drug/label.json",
    timeout: int = 20,
) -> dict[str, Any]:
    """Search openFDA drug labels by generic or brand name."""
    search = f'openfda.generic_name:"{drug}" OR openfda.brand_name:"{drug}"'
    params = {"search": search, "limit": max(1, min(max_results, 100))}
    query_url = f"{base_url}?{urlencode(params)}"
    try:
        response = requests.get(base_url, params=params, timeout=timeout)
        response.raise_for_status()
        records = response.json().get("results", [])
    except Exception as exc:
        return _base_result("openFDA Drug Label", {"drug": drug, "max_results": max_results}, [], [f"openFDA label failed: {exc}"])

    items = [_flatten_label(record, drug, query_url) for record in records]
    return _base_result("openFDA Drug Label", {"drug": drug, "max_results": max_results}, items, [])


def search_adverse_events(
    drug: str,
    reaction: str | None = None,
    date_range: Mapping[str, str] | None = None,
    max_results: int = 10,
    base_url: str = "https://api.fda.gov/drug/event.json",
    timeout: int = 20,
) -> dict[str, Any]:
    """Search openFDA FAERS counts for a drug and optional reaction."""
    search_parts = [f'patient.drug.openfda.generic_name:"{drug}" OR patient.drug.openfda.brand_name:"{drug}"']
    if reaction:
        search_parts.append(f'patient.reaction.reactionmeddrapt:"{reaction}"')
    if date_range and (date_range.get("from") or date_range.get("to")):
        start = (date_range.get("from") or "20040101").replace("-", "")
        end = (date_range.get("to") or date.today().isoformat()).replace("-", "")
        search_parts.append(f"receivedate:[{start}+TO+{end}]")

    search = " AND ".join(f"({part})" for part in search_parts)
    count_params = {"search": search}
    yearly_params = {"search": search, "count": "receivedate"}
    query_url = f"{base_url}?{urlencode(count_params)}"

    warnings: list[str] = []
    total_count = 0
    yearly_counts: dict[str, int] = {}
    try:
        response = requests.get(base_url, params=count_params, timeout=timeout)
        response.raise_for_status()
        total_count = int(response.json().get("meta", {}).get("results", {}).get("total", 0))
    except Exception as exc:
        warnings.append(f"openFDA event total failed: {exc}")

    try:
        response = requests.get(base_url, params=yearly_params, timeout=timeout)
        response.raise_for_status()
        for bucket in response.json().get("results", []):
            year = str(bucket.get("time", ""))[:4]
            if year:
                yearly_counts[year] = yearly_counts.get(year, 0) + int(bucket.get("count", 0))
    except Exception as exc:
        warnings.append(f"openFDA event yearly counts failed: {exc}")

    items = []
    if total_count or yearly_counts:
        items.append(
            {
                "drug": drug,
                "reaction": reaction or "",
                "count": total_count,
                "serious_count": None,
                "yearly_counts": dict(sorted(yearly_counts.items())[-max_results:]),
                "query_url": query_url,
                "source": "openFDA FAERS",
                "evidence_note": "FAERS reports are signals and cannot establish incidence or causality.",
            }
        )

    return _base_result(
        "openFDA FAERS",
        {"drug": drug, "reaction": reaction or "", "date_range": dict(date_range or {}), "max_results": max_results},
        items,
        warnings,
    )


def _flatten_label(record: Mapping[str, Any], drug: str, query_url: str) -> dict[str, Any]:
    openfda = record.get("openfda", {})
    return {
        "drug": drug,
        "brand_names": openfda.get("brand_name", []),
        "generic_names": openfda.get("generic_name", []),
        "indications_and_usage": record.get("indications_and_usage", []),
        "warnings": record.get("warnings", []) or record.get("warnings_and_cautions", []),
        "adverse_reactions": record.get("adverse_reactions", []),
        "dosage_and_administration": record.get("dosage_and_administration", []),
        "set_id": record.get("set_id", ""),
        "effective_time": record.get("effective_time", ""),
        "query_url": query_url,
        "source": "openFDA Drug Label",
    }


def _base_result(source: str, query: dict[str, Any], items: list[dict[str, Any]], warnings: list[str]) -> dict[str, Any]:
    return {
        "query": query,
        "retrieved_at": date.today().isoformat(),
        "source": source,
        "items": items,
        "warnings": warnings,
        "next_page": None,
    }
