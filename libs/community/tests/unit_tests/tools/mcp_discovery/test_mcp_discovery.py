import asyncio
from typing import Any, Dict

import pytest

from langchain_community.tools.mcp_discovery.tool import MCPDiscoveryTool


class _MockResponse:
    def __init__(self, payload: Dict[str, Any]):
        self._payload = payload

    async def json(self) -> Dict[str, Any]:
        return self._payload

    async def __aenter__(self) -> "_MockResponse":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None


class _MockSession:
    def __init__(self, payload: Dict[str, Any]):
        self._payload = payload

    def post(self, *args: Any, **kwargs: Any) -> _MockResponse:
        return _MockResponse(self._payload)

    async def __aenter__(self) -> "_MockSession":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None


@pytest.fixture
def patch_aiohttp(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = {
        "total_found": 1,
        "recommendations": [
            {
                "name": "math-tool",
                "description": "Does math",
                "category": "math",
            }
        ],
    }

    monkeypatch.setattr(
        "aiohttp.ClientSession",
        lambda: _MockSession(payload),
    )


def test_mcp_discovery_run(patch_aiohttp: None) -> None:
    tool = MCPDiscoveryTool(api_url="http://test-api")

    result = tool.run("calculator")

    assert result.startswith("Found 1 tools:")
    assert "math-tool" in result
    assert "Category: math" in result


def test_mcp_discovery_arun(patch_aiohttp: None) -> None:
    tool = MCPDiscoveryTool(api_url="http://test-api")

    result = asyncio.run(tool.arun("calculator"))

    assert "math-tool" in result


def test_mcp_discovery_no_total_found(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = {
        "recommendations": [
            {
                "name": "search-tool",
                "description": "Searches",
                "category": "search",
            }
        ]
    }

    monkeypatch.setattr(
        "aiohttp.ClientSession",
        lambda: _MockSession(payload),
    )

    tool = MCPDiscoveryTool(api_url="http://test-api")

    result = tool.run("search")

    assert result.startswith("Following tools are found:")
    assert "search-tool" in result
