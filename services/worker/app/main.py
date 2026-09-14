from fastapi import FastAPI
from pydantic import BaseModel, Field

import os
import socket

app = FastAPI(
    title="CentopeIA Worker",
    version="0.1.0"
)

WORKER_NAME = os.getenv("WORKER_ID", socket.gethostname())

class JobRequest(BaseModel):
    job_id: str
    task: str
    payload: dict = Field(default_factory=dict)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "worker": WORKER_NAME,
        "service": "centopeia-worker",
        "version": "0.1.0"
    }


@app.post("/jobs")
def execute_job(job: JobRequest):
    if job.task == "echo":
        result = job.payload.get("message")

        return {
            "job_id": job.job_id,
            "status": "completed",
            "worker": WORKER_NAME,
            "result": result
        }

    return {
        "job_id": job.job_id,
        "status": "rejected",
        "worker": WORKER_NAME,
        "error": f"Unsupported task: {job.task}"
    }
