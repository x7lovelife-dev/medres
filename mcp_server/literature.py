from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import re
from typing import Any, Mapping, Protocol

import requests


LiteratureItem = dict[str, Any]


class LiteratureProvider(Protocol):
    name: str

    def search(
        self,
        query: str,
        date_range: Mapping[str, str] | None = None,
        max_results: int = 50,
    ) -> list[LiteratureItem]:
        ...


def search_literature(
    query: str,
    sources: list[str] | None = None,
    date_range: Mapping[str, str] | None = None,
    max_results: int = 50,
    providers: Mapping[str, LiteratureProvider] | None = None,
) -> dict[str, Any]:
    """Search multiple literature providers and merge duplicate records."""
    selected_sources = sources or ["pubmed", "europe_pmc", "crossref"]
    provider_map = dict(providers or default_literature_providers())
    warnings: list[str] = []
    merged: dict[str, LiteratureItem] = {}

    for source in selected_sources:
        provider = provider_map.get(source)
        if provider is None:
            warnings.append(f"unknown source skipped: {source}")
            continue

        try:
            items = provider.search(query, date_range=date_range, max_results=max_results)
        except Exception as exc:  # Keep other sources usable when one API fails.
            warnings.append(f"{source} failed: {exc}")
            continue

        for item in items:
            normalized = normalize_literature_item(item, fallback_source=source)
            key = normalized["dedupe_key"]
            if key in merged:
                existing_sources = merged[key].setdefault("sources", [])
                for item_source in normalized.get("sources", []):
                    if item_source not in existing_sources:
                        existing_sources.append(item_source)
                merged[key] = prefer_richer_item(merged[key], normalized)
            else:
                merged[key] = normalized

    return {
        "query": {
            "query": query,
            "sources": selected_sources,
            "date_range": dict(date_range or {}),
            "max_results": max_results,
        },
        "retrieved_at": date.today().isoformat(),
        "source": "multi-source-literature",
        "items": list(merged.values())[:max_results],
        "warnings": warnings,
        "next_page": None,
    }


def normalize_literature_item(
    item: Mapping[str, Any],
    fallback_source: str,
) -> LiteratureItem:
    source = str(item.get("source") or fallback_source)
    doi = normalize_doi(item.get("doi"))
    title = clean_text(item.get("title") or "")
    dedupe_key = f"doi:{doi}" if doi else f"title:{normalize_title(title)}"
    normalized = {
        "source": source,
        "sources": [source],
        "id": item.get("id") or "",
        "doi": doi,
        "title": title,
        "authors": item.get("authors") or [],
        "journal_or_server": item.get("journal_or_server") or "",
        "publication_date": item.get("publication_date") or "",
        "abstract": clean_text(item.get("abstract") or ""),
        "url": item.get("url") or "",
        "dedupe_key": dedupe_key,
        "evidence_note": item.get("evidence_note") or "",
    }
    return normalized


def prefer_richer_item(current: LiteratureItem, candidate: LiteratureItem) -> LiteratureItem:
    result = dict(current)
    for key in ["id", "doi", "title", "authors", "journal_or_server", "publication_date", "abstract", "url", "evidence_note"]:
        if not result.get(key) and candidate.get(key):
            result[key] = candidate[key]
    result["sources"] = current.get("sources", candidate.get("sources", []))
    return result


def normalize_doi(value: Any) -> str:
    if not value:
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", text)
    text = re.sub(r"^doi:\s*", "", text)
    return text


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value)).strip()


def default_literature_providers() -> dict[str, LiteratureProvider]:
    return {
        "pubmed": PubMedProvider(),
        "europe_pmc": EuropePmcProvider(),
        "crossref": CrossrefProvider(),
    }


@dataclass
class PubMedProvider:
    name: str = "pubmed"
    base_url: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    timeout: int = 20

    def search(
        self,
        query: str,
        date_range: Mapping[str, str] | None = None,
        max_results: int = 50,
    ) -> list[LiteratureItem]:
        term = query
        if date_range and (date_range.get("from") or date_range.get("to")):
            start = date_range.get("from", "1900-01-01").replace("-", "/")
            end = date_range.get("to", "3000-12-31").replace("-", "/")
            term = f"{query} AND ({start}:{end}[dp])"

        esearch = requests.get(
            f"{self.base_url}/esearch.fcgi",
            params={"db": "pubmed", "term": term, "retmode": "json", "retmax": max_results},
            timeout=self.timeout,
        )
        esearch.raise_for_status()
        ids = esearch.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []

        esummary = requests.get(
            f"{self.base_url}/esummary.fcgi",
            params={"db": "pubmed", "id": ",".join(ids), "retmode": "json"},
            timeout=self.timeout,
        )
        esummary.raise_for_status()
        payload = esummary.json().get("result", {})

        items: list[LiteratureItem] = []
        for pmid in ids:
            record = payload.get(pmid, {})
            article_ids = record.get("articleids") or []
            doi = next((entry.get("value") for entry in article_ids if entry.get("idtype") == "doi"), "")
            items.append(
                {
                    "source": self.name,
                    "id": f"PMID:{pmid}",
                    "doi": doi,
                    "title": record.get("title", ""),
                    "authors": [author.get("name", "") for author in record.get("authors", [])],
                    "journal_or_server": record.get("fulljournalname") or record.get("source", ""),
                    "publication_date": record.get("pubdate", ""),
                    "abstract": "",
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                }
            )
        return items


@dataclass
class EuropePmcProvider:
    name: str = "europe_pmc"
    base_url: str = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    timeout: int = 20

    def search(
        self,
        query: str,
        date_range: Mapping[str, str] | None = None,
        max_results: int = 50,
    ) -> list[LiteratureItem]:
        params = {"query": query, "format": "json", "pageSize": max_results}
        response = requests.get(self.base_url, params=params, timeout=self.timeout)
        response.raise_for_status()
        records = response.json().get("resultList", {}).get("result", [])
        items: list[LiteratureItem] = []
        for record in records:
            pmid = record.get("pmid")
            pmcid = record.get("pmcid")
            source_id = f"PMID:{pmid}" if pmid else f"PMCID:{pmcid}" if pmcid else record.get("id", "")
            items.append(
                {
                    "source": self.name,
                    "id": source_id,
                    "doi": record.get("doi", ""),
                    "title": record.get("title", ""),
                    "authors": record.get("authorString", "").split(", ") if record.get("authorString") else [],
                    "journal_or_server": record.get("journalTitle") or record.get("source", ""),
                    "publication_date": record.get("firstPublicationDate") or record.get("pubYear", ""),
                    "abstract": record.get("abstractText", ""),
                    "url": record.get("fullTextUrlList", {}).get("fullTextUrl", [{}])[0].get("url", "")
                    if record.get("fullTextUrlList")
                    else "",
                }
            )
        return items


@dataclass
class CrossrefProvider:
    name: str = "crossref"
    base_url: str = "https://api.crossref.org/works"
    timeout: int = 20

    def search(
        self,
        query: str,
        date_range: Mapping[str, str] | None = None,
        max_results: int = 50,
    ) -> list[LiteratureItem]:
        params = {"query.bibliographic": query, "rows": max_results}
        response = requests.get(self.base_url, params=params, timeout=self.timeout)
        response.raise_for_status()
        records = response.json().get("message", {}).get("items", [])
        items: list[LiteratureItem] = []
        for record in records:
            issued = record.get("issued", {}).get("date-parts", [[]])[0]
            publication_date = "-".join(str(part) for part in issued) if issued else ""
            authors = [
                " ".join(part for part in [author.get("given", ""), author.get("family", "")] if part)
                for author in record.get("author", [])
            ]
            doi = record.get("DOI", "")
            items.append(
                {
                    "source": self.name,
                    "id": doi,
                    "doi": doi,
                    "title": (record.get("title") or [""])[0],
                    "authors": authors,
                    "journal_or_server": (record.get("container-title") or [""])[0],
                    "publication_date": publication_date,
                    "abstract": clean_text(record.get("abstract", "")),
                    "url": record.get("URL", ""),
                }
            )
        return items
