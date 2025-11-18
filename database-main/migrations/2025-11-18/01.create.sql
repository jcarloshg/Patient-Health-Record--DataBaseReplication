CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE PatientRegister (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL CHECK (date_of_birth >= '1900-01-01' AND date_of_birth <= CURRENT_DATE),
    email VARCHAR(254) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    address VARCHAR(100) NOT NULL,
    emergency_contact VARCHAR(50) NOT NULL,
    allergies TEXT[] DEFAULT ARRAY[]::TEXT[],
    medical_history TEXT[] DEFAULT ARRAY[]::TEXT[],
    current_medications TEXT[] DEFAULT ARRAY[]::TEXT[]
);