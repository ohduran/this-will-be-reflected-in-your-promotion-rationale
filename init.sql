CREATE TABLE IF NOT EXISTS psp_status (
    id SERIAL PRIMARY KEY,
    provider_name VARCHAR(255) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO psp_status (provider_name, is_active) VALUES
    ('checkout', true),
    ('dlocal', true),
    ('braintree', true),
    ('shift4', true)
ON CONFLICT (provider_name) DO NOTHING;