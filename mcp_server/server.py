from __future__ import annotations

from typing import Any

from .clinical_trials import search_clinical_trials as run_clinical_trials_search
from .literature import search_literature as run_literature_search
from .patents import search_patents as run_patent_search
from .safety import (
    search_adverse_events as run_adverse_event_search,
    search_drug_labels as run_drug_label_search,
)


def build_server() -> Any:
    try:
        from mcp.server.fastmcp import FastMCP
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "The Python package 'mcp' is required to run this server. "
            "Install dependencies with: pip install -r requirements.txt"
        ) from exc

    mcp = FastMCP("pharma-research")

    @mcp.tool()
    def search_literature(
        query: str,
        sources: list[str] | None = None,
        date_range: dict[str, str] | None = None,
        max_results: int = 50,
    ) -> dict[str, Any]:
        """Search biomedical literature across PubMed, Europe PMC, and Crossref."""
        return run_literature_search(
            query=query,
            sources=sources,
            date_range=date_range,
            max_results=max_results,
        )

    @mcp.tool()
    def search_clinical_trials(
        condition: str | None = None,
        intervention: str | None = None,
        phase: list[str] | None = None,
        status: list[str] | None = None,
        max_results: int = 25,
    ) -> dict[str, Any]:
        """Search ClinicalTrials.gov API v2 for study metadata."""
        return run_clinical_trials_search(
            condition=condition,
            intervention=intervention,
            phase=phase,
            status=status,
            max_results=max_results,
        )

    @mcp.tool()
    def search_drug_labels(drug: str, max_results: int = 5) -> dict[str, Any]:
        """Search openFDA drug label sections for a generic or brand name."""
        return run_drug_label_search(drug=drug, max_results=max_results)

    @mcp.tool()
    def search_adverse_events(
        drug: str,
        reaction: str | None = None,
        date_range: dict[str, str] | None = None,
        max_results: int = 10,
    ) -> dict[str, Any]:
        """Search openFDA FAERS report counts for a drug and optional reaction."""
        return run_adverse_event_search(
            drug=drug,
            reaction=reaction,
            date_range=date_range,
            max_results=max_results,
        )

    @mcp.tool()
    def search_patents(
        query: str,
        jurisdictions: list[str] | None = None,
        date_range: dict[str, str] | None = None,
        max_results: int = 25,
    ) -> dict[str, Any]:
        """Search public patent metadata for early patent landscaping."""
        return run_patent_search(
            query=query,
            jurisdictions=jurisdictions,
            date_range=date_range,
            max_results=max_results,
        )

    return mcp


def main() -> None:
    build_server().run()


if __name__ == "__main__":
    main()
