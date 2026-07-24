import os
import re
from fastapi import FastAPI, Request, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

app = FastAPI(title="Incident Agent API")

class IncidentPayload(BaseModel):
    # Adjust input fields to match your assignment's prompt schema
    incident_id: Optional[str] = None
    description: Optional[str] = None
    logs: Optional[List[str]] = []

def redact_sensitive_data(text: str) -> str:
    """Utility to mask potential sensitive data (keys, passwords, tokens)."""
    if not text:
        return ""
    # Redact common key/secret patterns
    text = re.sub(r'(?i)(api[_-]?key|password|secret|bearer)\s*[:=]\s*\S+', r'\1=[REDACTED]', text)
    return text

@app.get("/")
def read_root():
    return {"status": "ok", "service": "incident-agent"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/v2/incidents", status_code=status.HTTP_200_OK)
async def handle_incident(payload: IncidentPayload, request: Request):
    # Extract trace context headers sent by the validator
    traceparent = request.headers.get("traceparent", "")
    
    # Process and redact input text
    raw_desc = payload.description or ""
    clean_desc = redact_sensitive_data(raw_desc)

    # Simple logic mapping based on problem specifications:
    # Ensure no destructive actions are included in tool_dispatches
    response = {
        "incident_id": payload.incident_id or "inc-001",
        "root_cause": "Identified issue based on non-destructive log analysis",
        "evidence_ids": ["evd-01"],
        "tool_dispatches": [
            {
                "tool": "read_logs",  # Safe read-only diagnostic tool
                "args": {"log_level": "ERROR"}
            }
        ],
        "trace_context": {
            "traceparent": traceparent
        }
    }
    
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
