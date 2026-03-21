# MCP Hackyx

A [Model Context Protocol](https://modelcontextprotocol.io/) server for [Hackyx](https://hackyx.io/), the cybersecurity search engine created by [@aituglo](https://x.com/aituglo).

Search writeups, bug bounty reports, and security articles by keywords, tags, CWE, program, or source — directly from your AI assistant.

## Tools

| Tool | Description |
|------|-------------|
| `search` | Search indexed cybersecurity articles with optional filters (`tags`, `cwe`, `program`, `source`) |

## Quick Start

```bash
docker compose up -d
```

The MCP endpoint is available at `http://localhost:8000/mcp` (Streamable HTTP).

## Connect to Claude

Add to your MCP config:

```json
{
  "mcpServers": {
    "hackyx": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```
