import os

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response

app = FastAPI(
    title="CentopeIA Gateway",
    version="0.2.0-dev",
)

CORE_URL = os.getenv("CORE_URL", "http://core:8000")
CHAT_TIMEOUT_SECONDS = float(
    os.getenv("CHAT_TIMEOUT_SECONDS", "120")
)


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

@app.post("/chat")
async def chat(payload: dict):
    try:
        async with httpx.AsyncClient(
            timeout=CHAT_TIMEOUT_SECONDS
        ) as client:
            response = await client.post(
                f"{CORE_URL}/chat",
                json=payload,
            )

        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get(
                "content-type",
                "application/json",
            ),
        )

    except httpx.TimeoutException as exc:
        raise HTTPException(
            status_code=504,
            detail="Core chat request timed out",
        ) from exc

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to reach Core",
        ) from exc

