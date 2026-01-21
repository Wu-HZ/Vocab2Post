import httpx
import pdfplumber
import base64
import tempfile
import logging
import json
from config import settings

logger = logging.getLogger(__name__)

async def download_pdf(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=60)
        response.raise_for_status()
        return response.content

def extract_text(pdf_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(pdf_bytes)
        f.flush()
        with pdfplumber.open(f.name) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

async def generate_passage(text: str) -> tuple[str, str]:
    prompt = f"""Based on the following vocabulary content, generate a creative passage.
You MUST respond with valid JSON only, no other text:
{{"title": "your creative title", "content": "<p>your HTML content here</p>"}}

Vocabulary:
{text}"""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://b4u.qzz.io/v1/messages",
            headers={
                "Authorization": f"Bearer {settings.AI_API_KEY}",
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            },
            json={
                "model": "claude-4.5-sonnet-think",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4096
            },
            timeout=120
        )
        response.raise_for_status()
        result = response.json()["content"][0]["text"]
        # Extract JSON from response
        start = result.find("{")
        end = result.rfind("}") + 1
        data = json.loads(result[start:end])
        return data["title"], data["content"]

async def post_to_wordpress(title: str, content: str) -> dict:
    auth = base64.b64encode(f"{settings.WP_USER}:{settings.WP_APP_PASSWORD}".encode()).decode()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.WP_URL,
            headers={"Authorization": f"Basic {auth}"},
            json={"title": title, "content": content, "status": "publish"},
            timeout=30
        )
        response.raise_for_status()
        return response.json()

async def process_pdf(url: str):
    try:
        pdf_bytes = await download_pdf(url)
        text = extract_text(pdf_bytes)
        title, passage_html = await generate_passage(text)
        await post_to_wordpress(title, passage_html)
        logger.info(f"Successfully processed: {url}")
    except Exception as e:
        logger.error(f"Failed to process {url}: {e}")
