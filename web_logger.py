from fastapi import FastAPI, Request
import uvicorn
import json
from datetime import datetime
import os

app = FastAPI()

LOG_FILE = "sample_log.json"
@app.get("/")
def health_check():
    return {"status": "running"}

@app.post("/log_attempt")
async def log_attempt(req: Request):
    data = await req.json()
    data['timestamp'] = datetime.utcnow().isoformat()
    data['firewall'] = data.get('firewall', 'unknown')
    data['location'] = data.get('location', 'unknown')

    # ✅ Ensure the log file exists and starts with a valid JSON list
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)

    # ✅ Append the new log to the existing JSON list
    with open(LOG_FILE, 'r+') as f:
        try:
            existing = json.load(f)
        except json.JSONDecodeError:
            existing = []
        existing.append(data)
        f.seek(0)
        json.dump(existing, f, indent=4)

    return {"status": "logged"}

# Run using: uvicorn web_logger:app --reload
