# Vocab2Post

PDF vocabulary to WordPress passage automation via AI.

## Environment Variables (.env)
* `WP_URL`: WordPress API endpoint
* `WP_USER`: WordPress username
* `WP_APP_PASSWORD`: WordPress Application Password
* `AI_API_KEY`: API key for AI service
* `PORT`: Local port (default: 8940)

## Coding Standards
* Use `async def` for all route handlers and external calls
* Use `BackgroundTasks` for the processing pipeline
* Wrap external calls in try/except; log errors, don't crash
* Keep structure: `main.py` (routes), `services.py` (logic), `config.py` (env)
