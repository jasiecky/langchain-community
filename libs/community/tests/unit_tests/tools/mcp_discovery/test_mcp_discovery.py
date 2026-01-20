import asyncio
from typing import Any, Dict

import pytest

from langchain_community.tools.mcp_discovery.tool import MCPDiscoveryTool


class _MockResponse:
    def __init__(self, payload: Dict[str, Any]) -> None:
        self._payload = payload

    async def json(self) -> Dict[str, Any]:
        return self._payload

    async def __aenter__(self) -> "_MockResponse":
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        return None


class _MockSession:
    def __init__(self, payload: Dict[str, Any]) -> None:
        self._payload = payload

    def post(self, *args: Any, **kwargs: Any) -> _MockResponse:
        return _MockResponse(self._payload)

    async def __aenter__(self) -> "_MockSession":
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        return None


def _make_tool(api_url: str) -> MCPDiscoveryTool:
    """Create MCPDiscoveryTool without invoking Pydantic __init__."""
    tool = MCPDiscoveryTool.__new__(MCPDiscoveryTool)
    tool.api_url = api_url
    return tool


@pytest.fixture
def patch_aiohttp(monkeypatch: pytest.MonkeyPatch) -> None:
    payload: Dict[str, Any] = {
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
    tool = _make_tool("http://test-api")

    result: str = tool._run("calculator")

    assert result.startswith("Found 1 tools:")
    assert "math-tool" in result
    assert "Category: math" in result


def test_mcp_discovery_arun(patch_aiohttp: None) -> None:
    tool = _make_tool("http://test-api")

    result: str = asyncio.run(tool._arun("calculator"))

    assert "math-tool" in result


def test_mcp_discovery_no_total_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload: Dict[str, Any] = {
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

    tool = _make_tool("http://test-api")

    result: str = tool._run("search")

    assert result.startswith("Following tools are found:")
    assert "search-tool" in result
