# Patient Health Record (PHR) System - 🚧 Under Development...

## Requirements Overview

**Product idea:** A secure, cloud-hosted system for managing electronic health records (EHRs). The design must satisfy regulatory requirements for resilience and disaster recovery (DR).

### Replication requirement

- **Primary replication:** Master–slave (primary/replica) replication to provide high availability and read-scaling within the primary region.
- **Disaster Recovery (DR) replica:** An additional, geographically separated asynchronous replica located in a different availability zone or region to meet regulatory DR requirements and protect against regional outages.

### Key benefits

- **Disaster recovery:** If an entire data center or region fails, the remote DR replica can be brought online to restore service and minimize downtime.
- **Regulatory compliance:** Off-site, asynchronous replicas help satisfy regulations that mandate geographically separated backups and recoverability.
- **Patient-care continuity:** Reduces the risk of prolonged service interruption, helping clinicians access critical patient records when needed.

### Notes / Recommendations

- Define and document RTO (Recovery Time Objective) and RPO (Recovery Point Objective) for both primary and DR replicas.
- Perform regular DR drills and failover testing to validate recovery procedures.
- Monitor replication lag and automated alerts for replica health and data consistency.

## Technical Specifications

### Architecture Overview

The Patient Health Record (PHR) system implements a **Clean Architecture** pattern with a focus on high availability, disaster recovery, and regulatory compliance. The architecture separates concerns into distinct layers: domain, application, infrastructure, and presentation.

### Technology Stack

#### Backend

- **Language:** Python 3.12
- **Web Framework:** FastAPI 0.121.2
- **Data Validation:** Pydantic 2.12.4
- **ORM:** SQLAlchemy 2.0.44
- **ASGI Server:** Uvicorn 0.38.0
- **HTTP Client:** HTTPX 0.28.1
- **Testing:** Pytest 9.0.1
- **Environment Management:** python-dotenv 1.0.0

#### Database Layer

- **Primary Database:** PostgreSQL 15.13
- **Replication Type:** Streaming Replication (WAL-based)
- **Database Driver:** psycopg2-binary 2.9.9
- **Connection Pooling:** SQLAlchemy QueuePool
  - Pool size: 5 connections (configurable)
  - Max overflow: 10 connections
  - Pool timeout: 30 seconds
  - Pool recycle: 3600 seconds (1 hour)

#### Containerization & Orchestration

- **Container Runtime:** Docker
- **Orchestration:** Docker Compose
- **Base Image:** postgres:15.13

### Database Architecture

#### Database Topology

```
┌─────────────────────────────────────────────────────────────┐
│                     Primary Region                           │
│                                                               │
│  ┌──────────────┐    Streaming      ┌──────────────┐        │
│  │   db-main    │   Replication     │   db-slave   │        │
│  │  (Primary)   │ ──────────────>   │  (Replica)   │        │
│  │  Port: 5432  │   Synchronous     │  Port: 5433  │        │
│  └──────────────┘                   └──────────────┘        │
│         │                                    │               │
│         │ Write Operations                   │ Read Queries  │
│         └────────────────┬───────────────────┘               │
│                          │                                   │
└──────────────────────────┼───────────────────────────────────┘
                           │
                      Application
                         Layer
```

#### Database Configuration

**Primary Database (db-main):**

- **Host:** localhost:5432
- **Database Name:** `main-db_patient_health_record`
- **Role:** Master/Primary - Handles all write operations
- **WAL Level:** `replica` (enables streaming replication)
- **Max WAL Senders:** 10 concurrent replication connections
- **Max Replication Slots:** 10
- **Archive Mode:** Enabled (archive_command: '/bin/true')
- **Hot Standby:** Enabled

**Replica Database (db-slave):**

- **Host:** localhost:5433
- **Database Name:** `db_patient_health_record`
- **Role:** Hot Standby - Read-only replica
- **Replication Method:** Streaming (pg_basebackup)
- **Replication User:** `replicator`
- **Connection Mode:** Asynchronous streaming
- **Hot Standby:** Enabled (allows read queries)

#### Replication Features

1. **Streaming Replication**

   - Real-time WAL (Write-Ahead Log) streaming from primary to replica
   - Sub-second replication lag under normal conditions
   - Automatic recovery on connection interruptions

2. **Data Consistency**

   - All write operations committed to primary before returning success
   - Replica receives changes through continuous WAL streaming
   - Automatic conflict resolution (primary always wins)

3. **High Availability**
   - Health checks configured with 10-second intervals
   - Automatic container restart on failure
   - Network isolation through dedicated Docker bridge network

### Data Model

#### PatientRegister Entity

```sql
CREATE TABLE PatientRegister (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Personal Information
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,

    -- Contact Details
    email VARCHAR(254) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    address VARCHAR(100) NOT NULL,
    emergency_contact VARCHAR(50) NOT NULL,

    -- Medical Information
    allergies TEXT[] DEFAULT ARRAY[]::TEXT[],
    medical_history TEXT[] DEFAULT ARRAY[]::TEXT[],
    current_medications TEXT[] DEFAULT ARRAY[]::TEXT[],

    -- Constraints
    CHECK (date_of_birth >= '1900-01-01' AND date_of_birth <= CURRENT_DATE)
);
```

**Field Specifications:**

- **UUID:** Auto-generated using `uuid_generate_v4()` PostgreSQL extension
- **Personal Data:** 50-character limit for names
- **Date Validation:** Birth date between 1900-01-01 and current date
- **Email:** Maximum 254 characters (RFC 5321 compliant)
- **Phone:** 10-15 characters (international format support)
- **Arrays:** PostgreSQL native array types for flexible medical data storage

### Application Architecture

#### Layer Structure

```
presentation/          # API endpoints, controllers (FastAPI routes)
    └── REST API Layer

app/
    ├── create_patient_register/    # Bounded context
    │   ├── application/            # Use cases, business logic
    │   │   └── create_patient_register.py
    │   ├── domain/                 # Domain models, repositories interfaces
    │   │   ├── models/
    │   │   │   └── patient_register.py
    │   │   └── repos/
    │   │       └── create_patient_repo.py
    │   └── infra/                  # Infrastructure implementations
    │       └── persistence/
    │           └── db/
    │               └── create_patient_register_postgress.py
    │
    └── shared/                     # Shared kernel
        ├── domain/
        │   └── models/
        │       ├── custom_response.py
        │       └── model_error_exception.py
        └── infra/
            └── persistence/
                └── postgres_sql/
                    └── utils/
                        ├── connection.py
                        └── patient_register_model.py
```

#### Design Patterns

1. **Repository Pattern**

   - Abstract data access through repository interfaces
   - Clean separation between domain and infrastructure
   - Enables easy testing with mock repositories

2. **Use Case Pattern**

   - Business logic encapsulated in dedicated use case classes
   - Single Responsibility: Each use case handles one business operation
   - Example: `CreatePatientRegisterUseCase`

3. **Domain-Driven Design (DDD)**

   - Bounded contexts for different business capabilities
   - Domain models with built-in validation
   - Rich domain entities with behavior

4. **Dependency Injection**
   - Loose coupling between layers
   - Constructor injection for repositories
   - Facilitates unit testing

### Data Validation Strategy

#### Multi-Layer Validation

1. **Domain Layer Validation (Pydantic)**

   ```python
   - String length constraints (min/max)
   - Email format validation (regex pattern)
   - Date range validation (1900-01-01 to present)
   - Phone number format (10-15 characters)
   - Required vs optional fields
   ```

2. **Database Constraint Validation**

   ```sql
   - NOT NULL constraints
   - CHECK constraints (date_of_birth range)
   - VARCHAR length limits
   - Primary key uniqueness (UUID)
   ```

3. **Error Handling**
   - Custom exceptions: `ModelErrorException`
   - Standardized responses: `CustomResponse`
   - Detailed error messages with field-level context

### Security Considerations

#### Database Security

- Authentication required for all database connections
- Separate replication user with limited privileges
- MD5 password authentication (upgrade to SCRAM-SHA-256 for production)
- Network isolation through Docker networks

#### Application Security

- Input validation at multiple layers
- SQL injection prevention through ORM (SQLAlchemy)
- Environment variable configuration (no hardcoded credentials)
- Connection pooling prevents resource exhaustion

### Performance Optimizations

1. **Connection Pooling**

   - Pre-established database connections
   - Reduces connection overhead
   - Configurable pool size based on load

2. **Read Scaling**

   - Write operations to primary (db-main)
   - Read operations distributed to replica (db-slave)
   - Reduces load on primary database

3. **Asynchronous Processing**
   - ASGI server (Uvicorn) for async request handling
   - FastAPI native async support
   - Non-blocking I/O operations

### Monitoring & Observability

#### Health Checks

- **Database Health:** `pg_isready` checks every 10 seconds
- **Replication Status:** `pg_stat_replication` view
- **Replica Lag:** `pg_last_xact_replay_timestamp()` monitoring

#### Logging

- SQLAlchemy query logging (development mode)
- Application-level error logging
- Replication setup logs for debugging

### Deployment Configuration

#### Environment Variables

```bash
# Database Connection
POSTGRES_USER=admin
POSTGRES_PASSWORD=****** (secured)
POSTGRES_DB=main-db_patient_health_record
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Connection Pool
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

#### Docker Network

- **Network Name:** `replication-network`
- **Driver:** bridge
- **Purpose:** Isolated communication between db-main and db-slave
- **DNS Resolution:** Containers resolve each other by service name

#### Volumes

- **db-main:** Persistent storage for primary database
- **db-slave:** Persistent storage for replica database
- **Driver:** local
- **Lifecycle:** Persist beyond container lifecycle

### Testing Strategy

#### Unit Testing

- **Framework:** Pytest 9.0.1
- **Scope:** Domain models, use cases, repositories
- **Isolation:** Mock database connections
- **Coverage:** Business logic validation

#### Test Structure

```
test/
    └── unit/
        └── create_patient_register/
            └── application/
                └── test_create_patient_register.py
```

### Scalability Considerations

#### Current Implementation

- Single primary, single replica architecture
- Suitable for small to medium workloads
- Foundation for horizontal scaling

#### Future Enhancements

1. **Multiple Read Replicas**

   - Add more db-slave instances
   - Load balance read queries across replicas
   - Geographic distribution for reduced latency

2. **Connection Pooling Service**

   - PgBouncer for connection management
   - Reduced connection overhead
   - Better resource utilization

3. **Automatic Failover**

   - Patroni or repmgr for HA management
   - Automatic primary promotion
   - VIP (Virtual IP) for transparent failover

4. **Disaster Recovery Region**
   - Geographically separated async replica
   - Cross-region replication
   - Regulatory compliance for data residency

### Backup & Recovery

#### Current Backup Strategy

- Volume-based persistence (Docker volumes)
- Base backup through `pg_basebackup`
- WAL archiving enabled (configured for future use)

#### Recovery Capabilities

- Point-in-time recovery (PITR) foundation
- Replica promotion to primary
- Data persistence across container restarts

### Compliance & Regulatory

#### Data Handling

- UUID-based patient identification
- Structured medical data storage
- Audit trail foundation (extensible)

#### Availability Targets

- **RTO (Recovery Time Objective):** < 5 minutes (manual failover)
- **RPO (Recovery Point Objective):** < 1 minute (replication lag)
- **Uptime Target:** 99.9% (foundation for HA)

### Documentation

- **Main Documentation:** `README.md`
- **Replication Guide:** `REPLICATION_SETUP.md`
- **Use Cases:** `DOCS/use-cases/`
  - 1.  Create Patient Health Record
  - 2.  Read Patient Health Record
  - 3.  Update Patient Health Record
  - 4.  Delete Patient Health Record

### Development Workflow

1. **Local Development:** Connect to localhost:5432 (primary)
2. **Testing:** Unit tests with mocked repositories
3. **Integration Testing:** Docker Compose environment
4. **Replication Verification:** Query both primary and replica

### API Endpoints (Future Implementation)

```
POST   /api/v1/patients              # Create patient record
GET    /api/v1/patients/{uuid}       # Read patient record
PUT    /api/v1/patients/{uuid}       # Update patient record
DELETE /api/v1/patients/{uuid}       # Delete patient record
GET    /api/v1/health                # System health check
GET    /api/v1/replication/status    # Replication status
```
