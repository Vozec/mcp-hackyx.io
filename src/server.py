from mcp.server.fastmcp import FastMCP
from typing import Optional
from hackyx_client import search_articles

mcp = FastMCP(
    "hackyx",
    instructions=(
        "Hackyx is a cybersecurity search engine that indexes writeups, articles, "
        "and bug bounty reports. Use the search tool to find relevant security content "
        "by keyword, tags, CWE, bug bounty program, or source."
    ),
    host="0.0.0.0",
    port=8000,
)


def _format_hit(hit: dict) -> dict:
    """Extract relevant fields from a Typesense hit."""
    doc = hit.get("document", {})
    return {
        "title": doc.get("title", ""),
        "description": doc.get("description", ""),
        "url": doc.get("url", ""),
        "tags": doc.get("tags", []),
        "cwe": doc.get("cwe", []),
        "program": doc.get("program", ""),
        "source": doc.get("source", ""),
    }


def _format_facets(facet_counts: list) -> dict:
    """Extract facet values from Typesense response."""
    result = {}
    for facet in facet_counts:
        name = facet.get("field_name", "")
        values = [
            {"value": v["value"], "count": v["count"]}
            for v in facet.get("counts", [])
        ]
        result[name] = values
    return result


@mcp.tool()
async def search(
    query: str = "*",
    tags: Optional[str] = None,
    cwe: Optional[str] = None,
    program: Optional[str] = None,
    source: Optional[str] = None,
    page: int = 1,
    per_page: int = 10,
) -> dict:
    """
    Search cybersecurity articles indexed by Hackyx.

    Args:
        query: Search query (keywords). Use "*" to match all.
        tags: Filter by tag (e.g. "xss", "sqli", "ssrf", "rce").
        cwe: Filter by CWE identifier (e.g. "CWE-79", "CWE-89").
        program: Filter by bug bounty program name.
        source: Filter by article source (e.g. "hackerone", "medium").
        page: Page number (default 1).
        per_page: Results per page (default 10, max 50).
    """
    per_page = min(per_page, 50)

    data = await search_articles(
        query=query,
        tags=tags,
        cwe=cwe,
        program=program,
        source=source,
        page=page,
        per_page=per_page,
    )

    results = data.get("results", [{}])
    first = results[0] if results else {}

    hits = [_format_hit(h) for h in first.get("hits", [])]
    found = first.get("found", 0)
    facets = _format_facets(first.get("facet_counts", []))

    return {
        "total": found,
        "page": page,
        "per_page": per_page,
        "articles": hits,
        "facets": facets,
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
