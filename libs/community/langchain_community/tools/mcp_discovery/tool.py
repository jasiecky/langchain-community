"""Tools for discovering MCP tools via the MCP Discovery API."""

from __future__ import annotations

import asyncio
from typing import Optional

import aiohttp

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool


class MCPDiscoveryTool(BaseTool):
    """Tool for discovering MCP tools using the MCP Discovery API."""

    name: str = "mcp_discovery"
    description: str = """
    Can be used to discover MCP tools based on a natural language description.
    Returns a human-readable list of recommended MCP tools with their name,
    description, and category.
    """

    api_url: str

    def __init__(self, api_url: str):
        """Initialize the MCPDiscoveryTool.

        Args:
            api_url: URL of the MCP Discovery API endpoint.
        """
        super().__init__()
        self.api_url = api_url

    async def _request(self, user_request: str, limit: int) -> dict:
        """Perform a request to the MCP Discovery API."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_url,
                json={"need": user_request, "limit": limit},
            ) as response:
                return await response.json()

    def _format_response(self, data: dict) -> str:
        """Format the MCP Discovery API response."""
        tools_json = data.get("recommendations", [])
        total_found = data.get("total_found", -1)

        if total_found == -1:
            output = "Following tools are found:\n"
        else:
            output = f"Found {total_found} tools:\n"

        if tools_json:
            for index, tool in enumerate(tools_json, start=1):
                output += f"{index}. Name: {tool.get('name')},\n"
                output += f"   Description: {tool.get('description')},\n"
                output += f"   Category: {tool.get('category')}\n\n"
            return output.strip()

        return output

    def _run(
        self,
        tool_input: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Run the MCP Discovery tool synchronously.

        The input should be a natural language description of the desired tool.
        """
        try:
            return asyncio.run(self._arun(tool_input))
        except RuntimeError:
            # Event loop already running
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self._arun(tool_input))

    async def _arun(
        self,
        tool_input: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Run the MCP Discovery tool asynchronously."""
        try:
            data = await self._request(tool_input, limit=5)
            return self._format_response(data)
        except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
            return f"Error discovering tools: {exc}"
