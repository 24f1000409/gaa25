import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

app = FastAPI(title="Incident Agent API")

# Define strict request schema so missing/invalid payloads fail with HTTP 422
class IncidentRequest(BaseModel):
    # Adjust field names to match your assignment prompt requirements
    text: str = Field(..., min_length=1)  # Required field
    incident_id: Optional[str] = None

@app.get("/")
def read_root():
    return {"status": "ok", "service": "incident-agent"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/v2/incidents", status_code=status.HTTP_200_OK)
def handle_incident(request: IncidentRequest):
    """
    FastAPI will automatically return 422 if the request payload 
    does not match the IncidentRequest schema.
    """
    # Return structure expected by the assignment specification
    return {
        "root_cause": "sample_root_cause",
        "evidence_ids": [],
        "tool_dispatches": []
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
