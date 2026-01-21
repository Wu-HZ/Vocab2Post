from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from services import process_pdf

app = FastAPI()

class WebhookPayload(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
async def index():
    return """<!DOCTYPE html>
<html><head><title>Vocab2Post</title>
<style>body{font-family:sans-serif;max-width:500px;margin:50px auto;padding:20px}
input{width:100%;padding:10px;margin:10px 0;box-sizing:border-box}
button{padding:10px 20px;cursor:pointer}</style></head>
<body><h1>Vocab2Post</h1>
<form onsubmit="send(event)"><input id="url" placeholder="Paste PDF URL here" required>
<button type="submit">Submit</button></form><p id="msg"></p>
<script>async function send(e){e.preventDefault();
const r=await fetch('/webhook',{method:'POST',headers:{'Content-Type':'application/json'},
body:JSON.stringify({url:document.getElementById('url').value})});
document.getElementById('msg').textContent=r.ok?'Submitted!':'Error';}</script>
</body></html>"""

@app.post("/webhook")
async def webhook(payload: WebhookPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_pdf, payload.url)
    return {"status": "accepted"}

if __name__ == "__main__":
    import uvicorn
    from config import settings
    uvicorn.run(app, host="127.0.0.1", port=settings.PORT)
