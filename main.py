from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from services import process_pdf

app = FastAPI()

class WebhookPayload(BaseModel):
    url: str

@app.post("/webhook")
async def webhook(payload: WebhookPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_pdf, payload.url)
    return {"status": "accepted"}

if __name__ == "__main__":
    import uvicorn
    from config import settings
    uvicorn.run(app, host="127.0.0.1", port=settings.PORT)
