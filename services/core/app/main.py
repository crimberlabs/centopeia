import os

import psycopg
import redis
from fastapi import FastAPI, HTTPException

from app.model_gateway.gateway import ModelGateway
from app.model_gateway.models import ChatRequest, ChatResponse

from app.worker_registry import (
    WorkerHeartbeatRequest,
    WorkerRegisterRequest,
    get_worker,
    heartbeat_worker,
    list_workers,
    register_worker,
)


app = FastAPI(
    title="CentopeIA Core",
    version="0.4.0-dev",
)

model_gateway = ModelGateway()


def check_postgres() -> bool:
    try:
        with psycopg.connect(
            host=os.getenv("POSTGRES_HOST", "postgres"),
            port=5432,
            dbname=os.getenv("POSTGRES_DB", "centopeia"),
            user=os.getenv("POSTGRES_USER", "centopeia"),
            password=os.getenv("POSTGRES_PASSWORD"),
            connect_timeout=3,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return cursor.fetchone()[0] == 1
    except Exception:
        return False


def check_redis() -> bool:
    try:
        client = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=6379,
            socket_connect_timeout=3,
            socket_timeout=3,
        )
        return bool(client.ping())
    except Exception:
        return False


@app.get("/health")
async def health():
    postgres_ok = check_postgres()
    redis_ok = check_redis()

    dependencies = {
        "postgres": "healthy" if postgres_ok else "unhealthy",
        "redis": "healthy" if redis_ok else "unhealthy",
    }

    return {
        "service": "centopeia-core",
        "version": "0.3.0",
        "status": "healthy"
        if postgres_ok and redis_ok
        else "degraded",
        "dependencies": dependencies,
    }


@app.post("/workers/register")
def workers_register(payload: WorkerRegisterRequest):
    return register_worker(payload)


@app.post("/workers/{worker_id}/heartbeat")
def workers_heartbeat(
    worker_id: str,
    payload: WorkerHeartbeatRequest,
):
    return heartbeat_worker(worker_id, payload)


@app.get("/workers")
def workers_list():
    return list_workers()


@app.get("/workers/{worker_id}")
def workers_get(worker_id: str):
    return get_worker(worker_id)


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        return model_gateway.chat(payload)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc
