CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE PatientRegister (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL CHECK (
        date_of_birth >= '1900-01-01'
        AND date_of_birth <= CURRENT_DATE
    ),
    email VARCHAR(254) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    address VARCHAR(100) NOT NULL,
    emergency_contact VARCHAR(50) NOT NULL,
    allergies TEXT [] DEFAULT ARRAY[]::TEXT [],
    medical_history TEXT [] DEFAULT ARRAY[]::TEXT [],
    current_medications TEXT [] DEFAULT ARRAY[]::TEXT []
);

-- // ─────────────────────────────────────
-- // ─────────────────────────────────────
-- 1.
-- adding indexes for performance optimization for columns frequently queried
-- // ─────────────────────────────────────
-- // ─────────────────────────────────────

CREATE INDEX idx_first_name ON PatientRegister (lower(first_name));

CREATE INDEX idx_last_name ON PatientRegister (lower(last_name));

-- // ─────────────────────────────────────
-- // ─────────────────────────────────────
-- 2.
-- normalizing email addresses to lowercase to ensure uniqueness and consistency
-- // ─────────────────────────────────────
-- // ─────────────────────────────────────

-- Add a generated column 'email_normalized' that stores the lowercase, trimmed version of the email for normalization
-- always -> computed at insert/update time
-- stored -> physically stored in the table
ALTER TABLE PatientRegister
ADD COLUMN email_normalized VARCHAR(254) GENERATED ALWAYS AS (LOWER(TRIM(email))) STORED;

CREATE INDEX idx_patient_email_normalized ON PatientRegister (email_normalized);

-- -- Update statistics for query planner
-- ANALYZE PatientRegister;

-- -- Rebuild indexes if needed
-- REINDEX TABLE PatientRegister;

-- -- Vacuum to reclaim space
-- VACUUM ANALYZE PatientRegister;