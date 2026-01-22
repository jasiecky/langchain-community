# import asyncio

# from langchain_community.tools.mcp_discovery.tool import MCPDiscoveryTool

# API_URL = "http://127.0.0.1:8000/mcp"  # ← ZMIEŃ NA SWÓJ ENDPOINT


# async def main() -> None:
#     tool = MCPDiscoveryTool(api_url=API_URL)

#     print("=== ASYNC RUN ===")
#     result_async = await tool.arun("I need a tool to add Add two numbers.")
#     print(result_async)

#     print("\n=== SYNC RUN ===")
#     result_sync = tool.run("I need any tool")
#     print(result_sync)


# if __name__ == "__main__":
#     asyncio.run(main())
