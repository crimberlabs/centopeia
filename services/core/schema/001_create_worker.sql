CREATE TABLE IF NOT EXISTS worker (
    worker_id TEXT PRIMARY KEY,

    address INET NOT NULL,

    port INTEGER NOT NULL,

    version TEXT NOT NULL,

    administrative_status TEXT NOT NULL DEFAULT 'enabled',

    observed_status TEXT NOT NULL DEFAULT 'unknown',

    capabilities JSONB NOT NULL DEFAULT '[]'::jsonb,

    registered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT ck_worker__port_range
        CHECK (port BETWEEN 1 AND 65535),

    CONSTRAINT ck_worker__administrative_status
        CHECK (
            administrative_status IN (
                'enabled',
                'drained',
                'disabled'
            )
        ),

    CONSTRAINT ck_worker__observed_status
        CHECK (
            observed_status IN (
                'unknown',
                'healthy',
                'unhealthy',
                'offline'
            )
        ),

    CONSTRAINT ck_worker__capabilities_array
        CHECK (jsonb_typeof(capabilities) = 'array')
);

CREATE INDEX IF NOT EXISTS idx_worker__administrative_status
    ON worker (administrative_status);

CREATE INDEX IF NOT EXISTS idx_worker__observed_status
    ON worker (observed_status);

CREATE INDEX IF NOT EXISTS idx_worker__last_seen_at
    ON worker (last_seen_at);
