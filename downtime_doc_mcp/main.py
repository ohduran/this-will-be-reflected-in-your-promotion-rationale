import httpx
from mcp.server.fastmcp import FastMCP
import os


mcp = FastMCP("Downtime Document")

DOCUMENT_ID = os.getenv("DOCUMENT_ID")

async def make_google_doc_request(document_id: str) -> dict[str, str]:

    url = f"https://docs.google.com/document/d/{document_id}/export?format=txt"

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as error:
            raise Exception(f" HTTP Error: {error}: {response.text}")

@mcp.tool()
async def downtime_document_content(question: str):
    content = await make_google_doc_request(document_id=DOCUMENT_ID)

    result = f"Question: {question}/n"
    result += f"Content: {content}"
    
    return result

if __name__ == "__main__":
    mcp.run()
