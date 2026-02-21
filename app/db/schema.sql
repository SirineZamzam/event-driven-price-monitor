-- EVENTS = raw facts (what actually happened)

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    item TEXT NOT NULL,
    old_price NUMERIC,
    new_price NUMERIC NOT NULL,
    currency TEXT NOT NULL,
    observed_at TIMESTAMP NOT NULL DEFAULT NOW(),
    processed BOOLEAN NOT NULL DEFAULT FALSE
);

-- DECISIONS = interpretations (what the system thinks)

CREATE TABLE decisions (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id),
    summary TEXT NOT NULL,
    model TEXT NOT NULL,
    prompt TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);