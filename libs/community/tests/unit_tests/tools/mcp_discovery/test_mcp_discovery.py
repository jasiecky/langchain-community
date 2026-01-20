# import asyncio
# from typing import Any, Dict

# import pytest

# from langchain_community.tools.mcp_discovery.tool import MCPDiscoveryTool


# class _MockResponse:
#     def __init__(self, payload: Dict[str, Any]) -> None:
#         self._payload = payload

#     async def json(self) -> Dict[str, Any]:
#         return self._payload

#     async def __aenter__(self) -> "_MockResponse":
#         return self

#     async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
#         return None


# class _MockSession:
#     def __init__(self, payload: Dict[str, Any]) -> None:
#         self._payload = payload

#     def post(self, *args: Any, **kwargs: Any) -> _MockResponse:
#         return _MockResponse(self._payload)

#     async def __aenter__(self) -> "_MockSession":
#         return self

#     async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
#         return None


# @pytest.fixture
# def patch_aiohttp(monkeypatch: pytest.MonkeyPatch) -> None:
#     payload: Dict[str, Any] = {
#         "total_found": 1,
#         "recommendations": [
#             {
#                 "name": "math-tool",
#                 "description": "Does math",
#                 "category": "math",
#             }
#         ],
#     }

#     monkeypatch.setattr(
#         "aiohttp.ClientSession",
#         lambda: _MockSession(payload),
#     )


# def test_mcp_discovery_arun(patch_aiohttp: None) -> None:
#     tool = MCPDiscoveryTool(api_url="http://test-api")

#     result = asyncio.run(tool._arun("calculator"))

#     assert result.startswith("Found 1 tools:")
#     assert "math-tool" in result
#     assert "Category: math" in result


# def test_mcp_discovery_run_returns_task(patch_aiohttp: None) -> None:
#     tool = MCPDiscoveryTool(api_url="http://test-api")

#     result = tool._run("calculator")

#     assert isinstance(result, asyncio.Task)

#     output = asyncio.get_event_loop().run_until_complete(result)

#     assert "math-tool" in output
#     assert "Category: math" in output


# def test_mcp_discovery_no_total_found(
#     monkeypatch: pytest.MonkeyPatch,
# ) -> None:
#     payload: Dict[str, Any] = {
#         "recommendations": [
#             {
#                 "name": "search-tool",
#                 "description": "Searches",
#                 "category": "search",
#             }
#         ]
#     }

#     monkeypatch.setattr(
#         "aiohttp.ClientSession",
#         lambda: _MockSession(payload),
#     )

#     tool = MCPDiscoveryTool(api_url="http://test-api")

#     result = tool._run("search")

#     assert isinstance(result, asyncio.Task)

#     output = asyncio.get_event_loop().run_until_complete(result)

#     assert output.startswith("Following tools are found:")
#     assert "search-tool" in output
