CREATE TABLE IF NOT EXISTS sentiments (
    id SERIAL PRIMARY KEY,
    company VARCHAR(255),
    views INTEGER
);