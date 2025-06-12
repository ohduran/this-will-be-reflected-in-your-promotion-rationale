import sys
from contextlib import AsyncExitStack
import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.streamable_http import streamablehttp_client as http_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class MCPClient:

    def __init__(self) -> None:
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_db_mcp_server(self, container: str, port: int):

        async with http_client(f"http://{container}:{port}/mcp") as transport:
            async with ClientSession(transport[0], transport[1]) as session:
                await session.initialize()
                response = await self.session.list_tools()

        tools = response.tools()
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        messages = [
            {
                "role": "user",
                "content": query,
                }
        ]

        response = await self.session.list_tools()

        available_tools = [{
                           "name": tool.name,
                           "description": tool.description,
                           "input_schema": tool.inputSchema,
        } for tool in response.tools]

        response = self.anthropic.message.create(
            model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                message=messages,
                tools=available_tools
        )

        final_text = []

        assistant_message_content = []
        for content in response.content:
            if content.type == "text":
                final_text_append(content.text)
                assistant_message_content.append(content)

            elif content.type == "tool_use":
                tool_name = content.name
                tool_args = content.input

                # Execute
                result = await self.session.call_tool(tool_name, tool_args)
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                assistant_message_content.append(content)
                messages.append({
                                "role": "assistant",
                                "content": assistant_message_content
                })

                messages.append({
                                "role": "user",
                                "content": [
                                {
                                "type": "tool_result",
                                "tool_use_id": content.id,
                                "content": result.content,
                                },
                                ]
                })

                response = self.anthropic.messages.create(
                    model="claude-3-5-sonnet-20241022",
                        max_tokens=1000,
                        messages=messages,
                        tools=available_tools)

                final_text.append(response.content[0].text)

        return "\n".join(final_text)

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    client = MCPClient()
    try:
        # Use the correct container name and port as integer
        await client.connect_to_db_mcp_server("postgres_mcp_api", 9000)
        # Do something meaningful, e.g., call a tool and print the result
        result = await client.session.call_tool("get_psp_status", {})
        print(result)  # <-- This will show up in the Celery logs
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
