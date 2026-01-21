# CLAUDE.MD - Project Context & Guidelines

## Project Overview
**Name:** Vocab2Post
**Goal:** A self-hosted Python microservice that accepts a PDF URL via webhook, extracts vocabulary using Text extraction, generates a creative passage via AI, and publishes it to an existing WordPress site for consumption via RSS(Support other release ways in the future, now only).

## Tech Stack
* **Language:** Python 3.10+
* **Web Framework:** FastAPI (Asynchronous)
* **Server:** Uvicorn (ASGI)
* **PDF Processing:** `pdfplumber`
* **AI/LLM:** New API (configurable for other providers)
* **CMS Integration:** WordPress REST API
* **Deployment:** Nginx (Reverse Proxy) + Systemd

## Architecture Workflow
1.  **Ingest:** Endpoint `/webhook` receives `POST` JSON payload `{"url": "..."}`.
2.  **Response:** Immediate `200 OK` returned to client (Android) to prevent timeout.
3.  **Background Process:**
    * Download PDF from URL.
    * Extract text content using `pdfplumber`,throw away irrelevant information.
    * Send text to LLM to generate HTML-formatted vocabulary passage.
    * Authenticate with WordPress via Application Password.
    * Post content to `/wp-json/wp/v2/posts`.

## Environment Variables (.env)
* `WP_URL`: URL to WordPress API (e.g., `https://example.com/wp-json/wp/v2/posts`)
* `WP_USER`: WordPress Username
* `WP_APP_PASSWORD`: WordPress Application Password (not login password)
* `AI_API_KEY`: API Key for AI service
* `PORT`: Local port for Uvicorn (default: 8940)

## Coding Standards & Patterns
* **Asynchronous:** Use `async def` for route handlers. Use `BackgroundTasks` for the processing pipeline.
* **Typing:** Strict type hinting using `pydantic` models for request/response validation.
* **Error Handling:** Wrap external calls (Download, PDF parsing, AI, WP) in try/except blocks; log errors but do not crash the server.
* **Structure:**
    * `main.py`: App entry point and route definitions.
    * `services.py`: Business logic (PDF download, extraction, WordPress posting).
    * `config.py`: Environment variable management.

## Deployment Context (Nginx & Systemd)
* **Service Name:** `vocab-automation`
* **Local Address:** `127.0.0.1:8940` (or configured port)
* **Nginx Location Block Pattern:**
    ```nginx
    location /api/vocab/ {
        proxy_pass [http://127.0.0.1:8940/](http://127.0.0.1:8940/);
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    ```

## Development Commands
* **Install Dependencies:** `pip install -r requirements.txt`
* **Run Dev Server:** `uvicorn main:app --reload`
* **Run Production:** `uvicorn main:app --host 127.0.0.1 --port 8940`