CREATE TABLE IF NOT EXISTS psp_status (
    id SERIAL PRIMARY KEY,
    provider_name VARCHAR(255) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    errors_count INT NOT NULL DEFAULT 0,
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO psp_status (provider_name, is_active) VALUES
    ('checkout', true, 0),
    ('dlocal', true, 0),
    ('braintree', true, 0),
    ('shift4', true, 0)
ON CONFLICT (provider_name) DO NOTHING;

