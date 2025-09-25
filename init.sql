CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    username VARCHAR(100),
    fullname VARCHAR(100),
    location VARCHAR(100),
    timestamp TIMESTAMPTZ(0) DEFAULT now()

);


CREATE TABLE IF NOT EXISTS user_problems (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    problem TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS admin_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'admin',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT now()
);

INSERT INTO admin_users (username, password_hash, role)
VALUES ('admin', '$2b$12$1KdZ/Fai5KKHotfLKJ6WoeNFmAwtY4vo88.yu0Ts4cOiVxMnf0cdy', 'admin')
ON CONFLICT (username) DO NOTHING;

ALTER DATABASE telegram_bot_db SET timezone TO 'Europe/Moscow';