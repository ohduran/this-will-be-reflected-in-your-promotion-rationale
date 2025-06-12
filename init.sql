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

-- PSP TRANSACTION LOG TABLE
CREATE TABLE IF NOT EXISTS psp_transaction_log (
    id SERIAL PRIMARY KEY,
    provider_name VARCHAR(255) NOT NULL,
    request_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL, -- e.g. 'success', 'error'
    error_code VARCHAR(255), -- optional, for debugging specific error types
    request_id VARCHAR(255), -- optional, for traceability if needed
    additional_info JSONB -- optional, store arbitrary info from PSP response
);

INSERT INTO psp_transaction_log (provider_name, status, error_code, request_id, additional_info, request_timestamp) VALUES
    ('checkout', 'success', NULL, 'req-001', '{}', NOW() - interval '4 minutes'),
    ('checkout', 'success', 'timeout', 'req-002', '{}', NOW() - interval '3 minutes'),
    ('checkout', 'success', NULL, 'req-003', '{}', NOW() - interval '2 minutes'),
    ('checkout', 'success', 'internal_error', 'req-004', '{}', NOW() - interval '1 minute'),
    ('dlocal', 'success', NULL, 'req-005', '{}', NOW() - interval '4 minutes'),
    ('dlocal', 'success', NULL, 'req-006', '{}', NOW() - interval '2 minutes'),
    ('braintree', 'error', 'network_failure', 'req-007', '{}', NOW() - interval '5 minutes'),
    ('braintree', 'error', 'network_failure', 'req-008', '{}', NOW() - interval '4 minutes'),
    ('braintree', 'error', NULL, 'req-009', '{}', NOW() - interval '2 minutes'),
    ('shift4', 'success', NULL, 'req-010', '{}', NOW() - interval '3 minutes'),
    ('shift4', 'success', NULL, 'req-011', '{}', NOW() - interval '1 minute');