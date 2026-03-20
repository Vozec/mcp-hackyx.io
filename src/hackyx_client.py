import json
import httpx
from typing import Optional


TYPESENSE_URL = "https://api.hackyx.io"
TYPESENSE_API_KEY = "rbhL5yhPrBwYLVRTEubeqiALYzbVpPMT"
COLLECTION = "contents"
SEARCH_FIELDS = "title, description, tags, content, cwe, program, source"


async def search_articles(
    query: str = "*",
    tags: Optional[str] = None,
    cwe: Optional[str] = None,
    program: Optional[str] = None,
    source: Optional[str] = None,
    page: int = 1,
    per_page: int = 10,
) -> dict:
    """Search hackyx articles via Typesense multi_search API."""
    filters = []
    if tags:
        filters.append(f"tags:=[`{tags}`]")
    if cwe:
        filters.append(f"cwe:=[`{cwe}`]")
    if program:
        filters.append(f"program:=[`{program}`]")
    if source:
        filters.append(f"source:=[`{source}`]")

    filter_by = " && ".join(filters) if filters else ""

    search_params = {
        "query_by": SEARCH_FIELDS,
        "num_typos": "1",
        "typo_tokens_threshold": 1,
        "prefix": False,
        "highlight_full_fields": SEARCH_FIELDS,
        "collection": COLLECTION,
        "q": query,
        "facet_by": "cwe,program,source,tags",
        "max_facet_values": 10,
        "page": page,
        "per_page": per_page,
    }
    if filter_by:
        search_params["filter_by"] = filter_by

    payload = {"searches": [search_params]}

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(
            f"{TYPESENSE_URL}/multi_search",
            headers={
                "X-Typesense-Api-Key": TYPESENSE_API_KEY,
                "Content-Type": "text/plain",
            },
            content=json.dumps(payload),
        )
        resp.raise_for_status()
        return resp.json()
