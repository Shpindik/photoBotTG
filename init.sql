CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    fullname VARCHAR(255),
    location TEXT,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS user_problems (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    problem TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS phone_number (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    phone VARCHAR(20) NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_user_phone FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
