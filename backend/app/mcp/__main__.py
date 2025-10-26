"""Entry point for running MCP server as a module.

Usage:
    python -m backend.app.mcp
"""

import asyncio

from backend.app.mcp.server import main

if __name__ == '__main__':
	asyncio.run(main())
