import os

import httpx
from fastapi import FastAPI

app = FastAPI(
    title="CentopeIA Gateway",
    version="0.1.0",
)

CORE_URL = os.getenv("CORE_URL", "http://core:8000")


@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f"{CORE_URL}/health")
            response.raise_for_status()
            core_health = response.json()

        return {
            "service": "centopeia-gateway",
            "version": "0.1.0",
            "status": "healthy",
            "core": core_health,
        }

    except Exception:
        return {
            "service": "centopeia-gateway",
            "version": "0.1.0",
            "status": "degraded",
            "core": {
                "status": "unreachable"
            },
        }
