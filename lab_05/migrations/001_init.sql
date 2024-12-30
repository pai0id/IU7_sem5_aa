-- Active: 1732497983719@@127.0.0.1@5433@aa
-- +goose Up
-- +goose StatementBegin

CREATE TABLE IF NOT EXISTS recipies (
    id INT PRIMARY KEY,
    issue_id INT DEFAULT '9170',
    url TEXT NOT NULL,
    title TEXT NOT NULL,
    ingredients JSONB[] NOT NULL,
    steps TEXT[],
    image_url TEXT
);

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

DROP TABLE recipies;

-- +goose StatementEnd
