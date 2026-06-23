from mcp_server.literature import LiteratureProvider, search_literature


class StaticProvider(LiteratureProvider):
    def __init__(self, name, items=None, error=None):
        self.name = name
        self._items = items or []
        self._error = error

    def search(self, query, date_range=None, max_results=50):
        if self._error:
            raise RuntimeError(self._error)
        return self._items


def test_search_literature_merges_sources_and_dedupes_by_doi():
    providers = {
        "pubmed": StaticProvider(
            "pubmed",
            [
                {
                    "source": "pubmed",
                    "id": "PMID:1",
                    "doi": "10.1000/example",
                    "title": "PD-1 in gastric cancer",
                    "publication_date": "2024-01-01",
                }
            ],
        ),
        "crossref": StaticProvider(
            "crossref",
            [
                {
                    "source": "crossref",
                    "id": "10.1000/example",
                    "doi": "10.1000/EXAMPLE",
                    "title": "PD-1 in gastric cancer",
                    "publication_date": "2024-01-01",
                }
            ],
        ),
    }

    result = search_literature(
        query="PD-1 gastric cancer",
        sources=["pubmed", "crossref"],
        date_range={"from": "2020-01-01", "to": "2026-06-23"},
        max_results=10,
        providers=providers,
    )

    assert result["source"] == "multi-source-literature"
    assert result["query"]["query"] == "PD-1 gastric cancer"
    assert result["warnings"] == []
    assert len(result["items"]) == 1
    assert result["items"][0]["dedupe_key"] == "doi:10.1000/example"
    assert result["items"][0]["sources"] == ["pubmed", "crossref"]


def test_search_literature_keeps_successful_sources_when_one_fails():
    providers = {
        "pubmed": StaticProvider(
            "pubmed",
            [
                {
                    "source": "pubmed",
                    "id": "PMID:2",
                    "title": "Unique title",
                    "publication_date": "2023-05-01",
                }
            ],
        ),
        "openalex": StaticProvider("openalex", error="rate limited"),
    }

    result = search_literature(
        query="CLDN18.2 gastric cancer",
        sources=["pubmed", "openalex"],
        max_results=10,
        providers=providers,
    )

    assert len(result["items"]) == 1
    assert result["items"][0]["id"] == "PMID:2"
    assert result["warnings"] == ["openalex failed: rate limited"]


def test_search_literature_rejects_unknown_source():
    result = search_literature(
        query="osimertinib pneumonitis",
        sources=["unknown"],
        providers={},
    )

    assert result["items"] == []
    assert result["warnings"] == ["unknown source skipped: unknown"]
