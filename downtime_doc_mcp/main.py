import httpx
from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("Downtime Document")

GOOGLE_DOC_API_KEY = os.getenv("GOOGLE_DOC_API_KEY")
DOCUMENT_ID = os.getenv("DOCUMENT_ID")

async def make_google_doc_request(document_id: str, api_key: str) -> dict[str, str]:

    url = f"https://docs.googleapis.com/v1/documents/{document_id}"
    params = {'key': api_key}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as error:
            raise Exception(f" HTTP Error: {error}: {response.text}")

@mcp.tool()
async def downtime_document_content(question: str):
    content = await make_google_doc_request(document_id=DOCUMENT_ID, api_key=GOOGLE_DOC_API_KEY)

    result = f"Question: {question}/n"
    result += f"Content: {content}"
    
    return result

if __name__ == "__main__":
    mcp.run()
