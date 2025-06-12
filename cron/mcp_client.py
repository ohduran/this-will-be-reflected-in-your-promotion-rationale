import sys
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class MCPClient:

    def __init__(self) -> None:
        self.session = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_db_mcp_server(self, server_script_path: str):
        server_params = StdioServerParameters(
            command="python",
            args = [server_script_path],
            env=None,
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))

        self.stdio, self.write = stdio_transport

        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

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
        await client.connect_to_db_mcp_server(sys.argv[1])
    finally:
        await client.cleanup()
