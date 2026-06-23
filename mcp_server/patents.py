from __future__ import annotations

from datetime import date
from typing import Any, Mapping
from urllib.parse import quote_plus

import requests


def search_patents(
    query: str,
    jurisdictions: list[str] | None = None,
    date_range: Mapping[str, str] | None = None,
    max_results: int = 25,
    base_url: str = "https://api.patentsview.org/patents/query",
    timeout: int = 60,
) -> dict[str, Any]:
    """Search public patent metadata and fall back to traceable patent search links."""
    fields = [
        "patent_number",
        "patent_title",
        "patent_abstract",
        "patent_date",
        "assignees.assignee_organization",
        "inventors.inventor_first_name",
        "inventors.inventor_last_name",
    ]
    payload: dict[str, Any] = {
        "q": {"_text_any": {"patent_title": query}},
        "f": fields,
        "o": {"per_page": max(1, min(max_results, 100))},
    }

    warnings: list[str] = []
    try:
        response = requests.post(base_url, json=payload, timeout=timeout)
        response.raise_for_status()
        records = response.json().get("patents", [])
    except Exception as exc:
        warnings.append(f"PatentsView structured search unavailable: {exc}")
        return _result(query, jurisdictions, date_range, max_results, _fallback_search_links(query, jurisdictions, date_range), warnings)

    items: list[dict[str, Any]] = []
    requested_jurisdictions = {item.upper() for item in (jurisdictions or [])}
    for record in records:
        item = _flatten_patent(record)
        if requested_jurisdictions and item["jurisdiction"] not in requested_jurisdictions:
            continue
        if date_range and not _within_date_range(item.get("publication_date", ""), date_range):
            continue
        items.append(item)
        if len(items) >= max_results:
            break

    if not items:
        warnings.append("No structured patent records returned; use fallback search links for manual review.")
        items = _fallback_search_links(query, jurisdictions, date_range)

    return _result(query, jurisdictions, date_range, max_results, items, warnings)


def _flatten_patent(record: Mapping[str, Any]) -> dict[str, Any]:
    patent_number = str(record.get("patent_number", ""))
    assignees = [
        assignee.get("assignee_organization", "")
        for assignee in record.get("assignees", [])
        if assignee.get("assignee_organization")
    ]
    inventors = [
        " ".join(part for part in [inventor.get("inventor_first_name", ""), inventor.get("inventor_last_name", "")] if part)
        for inventor in record.get("inventors", [])
    ]
    return {
        "source": "PatentsView",
        "id": patent_number,
        "jurisdiction": "US",
        "title": record.get("patent_title", ""),
        "abstract": record.get("patent_abstract", ""),
        "publication_date": record.get("patent_date", ""),
        "assignees": assignees,
        "inventors": inventors,
        "url": f"https://patents.google.com/patent/US{patent_number}" if patent_number else "",
        "evidence_note": "",
    }


def _fallback_search_links(
    query: str,
    jurisdictions: list[str] | None,
    date_range: Mapping[str, str] | None,
) -> list[dict[str, Any]]:
    encoded = quote_plus(query)
    jurisdictions_text = ",".join(jurisdictions or [])
    date_text = ""
    if date_range:
        date_text = f" from {date_range.get('from', '')} to {date_range.get('to', '')}".strip()
    return [
        {
            "source": "Google Patents search link",
            "id": "",
            "jurisdiction": jurisdictions_text or "global",
            "title": f"Google Patents search: {query}",
            "abstract": "Fallback search link; review results manually and cite individual patent publications.",
            "publication_date": "",
            "assignees": [],
            "inventors": [],
            "url": f"https://patents.google.com/?q={encoded}",
            "evidence_note": f"Use for manual patent landscape review{(' ' + date_text) if date_text else ''}.",
        },
        {
            "source": "Espacenet search link",
            "id": "",
            "jurisdiction": jurisdictions_text or "global",
            "title": f"Espacenet search: {query}",
            "abstract": "Fallback search link; review results manually and cite individual patent publications.",
            "publication_date": "",
            "assignees": [],
            "inventors": [],
            "url": f"https://worldwide.espacenet.com/patent/search?q={encoded}",
            "evidence_note": "Use for family/legal status review when structured API data is unavailable.",
        },
        {
            "source": "PatentsView search link",
            "id": "",
            "jurisdiction": "US",
            "title": f"PatentsView search: {query}",
            "abstract": "Fallback search link; review results manually and cite individual US patent records.",
            "publication_date": "",
            "assignees": [],
            "inventors": [],
            "url": f"https://patentsview.org/patents?search={encoded}",
            "evidence_note": "Use for US patent metadata when PatentsView structured API is unavailable.",
        },
    ]


def _within_date_range(value: str, date_range: Mapping[str, str]) -> bool:
    if not value:
        return True
    start = date_range.get("from")
    end = date_range.get("to")
    if start and value < start:
        return False
    if end and value > end:
        return False
    return True


def _result(
    query: str,
    jurisdictions: list[str] | None,
    date_range: Mapping[str, str] | None,
    max_results: int,
    items: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    return {
        "query": {
            "query": query,
            "jurisdictions": jurisdictions or [],
            "date_range": dict(date_range or {}),
            "max_results": max_results,
        },
        "retrieved_at": date.today().isoformat(),
        "source": "public-patent-search",
        "items": items[:max_results] if max_results else items,
        "warnings": warnings,
        "next_page": None,
    }
