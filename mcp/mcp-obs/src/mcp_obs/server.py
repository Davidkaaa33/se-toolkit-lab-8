import os
from typing import Any
import httpx
from fastmcp import FastMCP

mcp = FastMCP("mcp-obs")

VLOGS_URL = os.getenv("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428").rstrip("/")
VTRACES_URL = os.getenv("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428").rstrip("/")

@mcp.tool
async def logs_search(query: str, limit: int = 50) -> dict[str, Any]:
    url = f"{VLOGS_URL}/select/logsql/query"
    params = {"query": query, "limit": str(limit)}
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return {"query": query, "status": r.status_code, "data": r.json()}

@mcp.tool
async def logs_error_count(minutes: int = 10, service_name: str = "Learning Management Service") -> dict[str, Any]:
    q = f'_time:{minutes}m service.name:"{service_name}" severity:ERROR'
    result = await logs_search(q, limit=500)
    data = result.get("data", {})
    rows = data if isinstance(data, list) else data.get("hits", data.get("data", []))
    return {"query": q, "error_count": len(rows)}

@mcp.tool
async def traces_list(service: str = "Learning Management Service", limit: int = 20) -> dict[str, Any]:
    url = f"{VTRACES_URL}/select/jaeger/api/traces"
    params = {"service": service, "limit": str(limit)}
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return {"service": service, "status": r.status_code, "data": r.json()}

@mcp.tool
async def traces_get(trace_id: str) -> dict[str, Any]:
    url = f"{VTRACES_URL}/select/jaeger/api/traces/{trace_id}"
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url)
        r.raise_for_status()
        return {"trace_id": trace_id, "status": r.status_code, "data": r.json()}

def main():
    mcp.run()

if __name__ == "__main__":
    main()
