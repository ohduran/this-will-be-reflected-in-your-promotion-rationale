import asyncpg
from mcp.server.fastmcp import FastMCP
import os
from typing import Any

mcp = FastMCP("Postgres MCP")

DB_CONFIG = {
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "database": os.getenv("DB_NAME", "app_db"),
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

async def get_db_pool():
    return await asyncpg.create_pool(**DB_CONFIG)

@mcp.tool()
async def get_psp_status() -> list[dict[str, Any]]:
    """Get all PSP (provider) statuses."""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, provider_name, is_active, last_checked FROM psp_status")
        return [dict(row) for row in rows]

@mcp.tool()
async def set_psp_status(provider_name: str, is_active: bool) -> str:
    """Set the active status of a PSP (provider)."""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE psp_status SET is_active = $1, last_checked = NOW() WHERE provider_name = $2",
            is_active, provider_name
        )
    return f"Provider '{provider_name}' status set to {'active' if is_active else 'inactive'}."

if __name__ == "__main__":
    mcp.run() 