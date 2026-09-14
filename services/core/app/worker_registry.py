import json
from datetime import datetime, timezone
from ipaddress import ip_address
from typing import Literal

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

from app.database import get_connection


class WorkerRegisterRequest(BaseModel):
    worker_id: str = Field(min_length=1, max_length=128)
    address: str
    port: int = Field(ge=1, le=65535)
    version: str = Field(min_length=1, max_length=64)
    capabilities: list[str] = Field(default_factory=list)

    @field_validator("worker_id", "version")
    @classmethod
    def validate_non_blank(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("must not be blank")

        return value

    @field_validator("address")
    @classmethod
    def validate_address(cls, value: str) -> str:
        try:
            return str(ip_address(value))
        except ValueError as exc:
            raise ValueError(
                "must be a valid IPv4 or IPv6 address"
            ) from exc


class WorkerHeartbeatRequest(BaseModel):
    observed_status: Literal[
        "unknown",
        "healthy",
        "unhealthy",
        "offline",
    ] = "healthy"


def register_worker(payload: WorkerRegisterRequest):
    now = datetime.now(timezone.utc)

    query = """
        INSERT INTO worker (
            worker_id,
            address,
            port,
            version,
            administrative_status,
            observed_status,
            capabilities,
            registered_at,
            last_seen_at,
            created_at,
            updated_at
        )
        VALUES (
            %(worker_id)s,
            %(address)s,
            %(port)s,
            %(version)s,
            'enabled',
            'healthy',
            %(capabilities)s::jsonb,
            %(now)s,
            %(now)s,
            %(now)s,
            %(now)s
        )
        ON CONFLICT (worker_id)
        DO UPDATE SET
            address = EXCLUDED.address,
            port = EXCLUDED.port,
            version = EXCLUDED.version,
            capabilities = EXCLUDED.capabilities,
            observed_status = 'healthy',
            last_seen_at = EXCLUDED.last_seen_at,
            updated_at = EXCLUDED.updated_at
        RETURNING *;
    """

    params = {
        "worker_id": payload.worker_id,
        "address": payload.address,
        "port": payload.port,
        "version": payload.version,
        "capabilities": json.dumps(payload.capabilities),
        "now": now,
    }

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            worker = cursor.fetchone()

    return worker


def heartbeat_worker(
    worker_id: str,
    payload: WorkerHeartbeatRequest,
):
    now = datetime.now(timezone.utc)

    query = """
        UPDATE worker
        SET
            observed_status = %(observed_status)s,
            last_seen_at = %(now)s,
            updated_at = %(now)s
        WHERE worker_id = %(worker_id)s
        RETURNING *;
    """

    params = {
        "worker_id": worker_id,
        "observed_status": payload.observed_status,
        "now": now,
    }

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            worker = cursor.fetchone()

    if worker is None:
        raise HTTPException(
            status_code=404,
            detail="Worker not found",
        )

    return worker


def list_workers():
    query = """
        SELECT *
        FROM worker
        ORDER BY worker_id;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            workers = cursor.fetchall()

    return workers


def get_worker(worker_id: str):
    query = """
        SELECT *
        FROM worker
        WHERE worker_id = %(worker_id)s;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                query,
                {"worker_id": worker_id},
            )
            worker = cursor.fetchone()

    if worker is None:
        raise HTTPException(
            status_code=404,
            detail="Worker not found",
        )

    return worker
