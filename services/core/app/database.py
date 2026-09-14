import os

import psycopg
from psycopg.rows import dict_row


def get_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=5432,
        dbname=os.getenv("POSTGRES_DB", "centopeia"),
        user=os.getenv("POSTGRES_USER", "centopeia"),
        password=os.getenv("POSTGRES_PASSWORD"),
        connect_timeout=3,
        row_factory=dict_row,
    )
