-- Create accounts table
CREATE TABLE IF NOT EXISTS test_backend_dev.accounts (
    id text PRIMARY KEY,
    name text,
    industry text,
    employee_count int,
    annual_revenue double,
    website text,
    is_active boolean,
    created_at timestamp,
    updated_at timestamp
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_accounts_name ON test_backend_dev.accounts (name);
CREATE INDEX IF NOT EXISTS idx_accounts_industry ON test_backend_dev.accounts (industry);
CREATE INDEX IF NOT EXISTS idx_accounts_is_active ON test_backend_dev.accounts (is_active); 