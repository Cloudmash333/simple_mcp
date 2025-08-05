#!/usr/bin/env python3
import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import logging
logging.basicConfig(level=logging.DEBUG)

# Create the server instance
server = Server("math-operations")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="add",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number to add"
                    },
                    "b": {
                        "type": "number", 
                        "description": "The second number to add"
                    }
                },
                "required": ["a", "b"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "add":
        # Extract the numbers from arguments
        a = arguments.get("a")
        b = arguments.get("b")
        
        # Validate inputs
        if a is None or b is None:
            return [TextContent(
                type="text",
                text="Error: Both 'a' and 'b' parameters are required"
            )]
        
        try:
            # Perform the addition
            result = float(a) + float(b)
            return [TextContent(
                type="text",
                text=f"The sum of {a} and {b} is {result}"
            )]
        except (ValueError, TypeError):
            return [TextContent(
                type="text",
                text="Error: Both parameters must be valid numbers"
            )]
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def main():
    """Run the server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())