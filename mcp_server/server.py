from __future__ import annotations

from typing import Any

from .literature import search_literature as run_literature_search


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

    return mcp


def main() -> None:
    build_server().run()


if __name__ == "__main__":
    main()

