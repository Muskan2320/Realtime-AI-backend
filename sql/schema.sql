-- Session table: stores active user sessions message logs
CREATE TABLE sessions (
    session_id uuid primary key,
    user_id text,

    start_time timestamptz not null default now(),
    end_time timestamptz,
    duration_seconds integer,

    summary text,
    created_at timestamptz default now()
);

-- Events table: stores detailed chronological events within sessions
CREATE table events (
    event_id uuid primary key,
    session_id uuid references sessions(session_id) on delete cascade,

    role text not null,
    content text,

    event_type text not null,
    created_at timestamptz not null default now()
);