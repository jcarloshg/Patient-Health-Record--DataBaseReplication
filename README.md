# 🏥 Patient Health Record (PHR) System - 🚧 Under Development...

## Overview

A secure, cloud-hosted Patient Health Record (PHR) system designed with **PostgreSQL Streaming Replication** to ensure high availability, disaster recovery, and regulatory compliance for healthcare environments.

### 🔄 Data Replication Architecture

- **Master-Slave Replication:** Implements PostgreSQL WAL-based streaming replication with one primary database (db-main) and two hot standby replicas (db-slave-01, db-slave-02)
- **Real-Time Synchronization:** Sub-second replication lag under normal conditions with asynchronous streaming for optimal performance
- **Read Scalability:** Write operations directed to primary (port 5432), read operations distributed across replicas (ports 5433, 5434) for horizontal scaling
- **High Availability:** Hot standby replicas can be promoted to primary during failover scenarios, ensuring minimal downtime
- **Data Protection:** Multiple data copies across isolated containers with automatic WAL streaming and point-in-time recovery capabilities

### 🏗️ System Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                          🌐 Application Layer                                   │
│                       (FastAPI + Uvicorn - Python 3.12)                        │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │  📡 REST API Endpoints                                                  │  │
│  │  • POST /patient-register (Create)  • GET /patient-register (Read)     │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
└────────────────────┬──────────────────────────────────────┬────────────────────┘
                     │                                      │
                     │ Write Operations                     │ Read Operations
                     │ (Create, Update, Delete)             │ (Query with Criteria)
                     │                                      │
┌────────────────────▼──────────────────┐    ┌─────────────▼─────────────────────┐
│   🔌 Connection Pool (Write)          │    │   🔌 Connection Pool (Read)       │
│   • Pool Size: 5                      │    │   • Distributed Load              │
│   • Max Overflow: 10                  │    │   • Read-Only Queries             │
│   • Timeout: 30s                      │    │   • Criteria Pattern              │
└────────────────────┬──────────────────┘    └─────────────┬─────────────────────┘
                     │                                      │
                     │                                      │
┌────────────────────┼──────────────────────────────────────┼────────────────────┐
│                    │       🐳 Docker Network              │                    │
│                    │       (replication-network)          │                    │
│                    │                                      │                    │
│     ┌──────────────▼──────────────┐                      │                    │
│     │   💾 db-main (Primary)      │                      │                    │
│     │   ━━━━━━━━━━━━━━━━━━━━━━━  │                      │                    │
│     │   🔹 Port: 5432             │                      │                    │
│     │   🔹 Role: Master           │                      │                    │
│     │   🔹 Operations: READ+WRITE │                      │                    │
│     │   🔹 PostgreSQL 15.13       │                      │                    │
│     │                             │                      │                    │
│     │   WAL Configuration:        │                      │                    │
│     │   • wal_level = replica     │                      │                    │
│     │   • max_wal_senders = 5     │                      │                    │
│     │   • archive_mode = on       │                      │                    │
│     └───────┬──────────────┬──────┘                      │                    │
│             │              │                             │                    │
│             │ WAL Stream   │ WAL Stream                  │                    │
│             │ (Async)      │ (Async)                     │                    │
│    ┌────────▼────────┐  ┌──▼──────────────┐             │                    │
│    │  💾 db-slave-01 │  │  💾 db-slave-02 │◄────────────┘                    │
│    │  (Hot Standby)  │  │  (Hot Standby)  │                                  │
│    │  ─────────────  │  │  ─────────────  │                                  │
│    │  🔹 Port: 5433  │  │  🔹 Port: 5434  │                                  │
│    │  🔹 READ ONLY   │  │  🔹 READ ONLY   │                                  │
│    │  🔹 Replication │  │  🔹 Replication │                                  │
│    │     User: repl  │  │     User: repl  │                                  │
│    │  🔹 Recovery    │  │  🔹 Recovery    │                                  │
│    │     Mode: ON    │  │     Mode: ON    │                                  │
│    └─────────────────┘  └─────────────────┘                                  │
│                                                                                │
│  📊 Monitoring:                                                                │
│  • pg_stat_replication (Primary)                                              │
│  • pg_is_in_recovery() (Replicas)                                             │
│  • Replication Lag Monitoring                                                 │
│  • Health Checks: pg_isready (10s interval)                                   │
└────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────┐
│                          💾 Persistent Storage Layer                           │
│                                                                                 │
│    🗃️ db-main-volume      🗃️ db-slave-01-volume      🗃️ db-slave-02-volume   │
│    (Docker Volume)        (Docker Volume)            (Docker Volume)          │
└────────────────────────────────────────────────────────────────────────────────┘
```

### 🎯 Key Features

- **Clean Architecture:** Domain-Driven Design with clear separation between presentation, application, domain, and infrastructure layers
- **Type-Safe Validation:** Multi-layer validation using Pydantic (application) and PostgreSQL constraints (database)
- **Flexible Querying:** Advanced Criteria Pattern for dynamic, type-safe queries with filters, ordering, and pagination
- **Security-First:** MD5 authentication, network isolation, SQL injection prevention through SQLAlchemy ORM
- **Production-Ready:** Connection pooling, health checks, monitoring tools, and comprehensive error handling

## 📋 Table of Contents

- [🏥 Patient Health Record (PHR) System - 🚧 Under Development...](#-patient-health-record-phr-system----under-development)
  - [📋 Table of Contents](#-table-of-contents)
  - [📖 Requirements Overview](#-requirements-overview)
    - [🔄 Replication Requirement](#-replication-requirement)
    - [✨ Key Benefits](#-key-benefits)
    - [📝 Notes / Recommendations](#-notes--recommendations)
  - [⚙️ Technical Specifications](#️-technical-specifications)
    - [🏗️ Architecture Overview](#️-architecture-overview)
    - [💻 Technology Stack](#-technology-stack)
    - [🗄️ Database Architecture](#️-database-architecture)
    - [📊 Data Model](#-data-model)
    - [🏛️ Application Architecture](#️-application-architecture)
    - [✅ Data Validation Strategy](#-data-validation-strategy)
    - [🔐 Security Considerations](#-security-considerations)
    - [⚡ Performance Optimizations](#-performance-optimizations)
    - [📈 Monitoring \& Observability](#-monitoring--observability)
    - [🚀 Deployment Configuration](#-deployment-configuration)
    - [🧪 Testing Strategy](#-testing-strategy)
    - [📏 Scalability Considerations](#-scalability-considerations)
    - [💾 Backup \& Recovery](#-backup--recovery)
    - [📜 Compliance \& Regulatory](#-compliance--regulatory)
  - [🔍 Criteria Pattern for Querying Patient Records](#-criteria-pattern-for-querying-patient-records)
    - [🎯 Pattern Overview](#-pattern-overview)
    - [🧩 Components](#-components)
    - [🔧 Implementation Details](#-implementation-details)
    - [📝 Usage Example](#-usage-example)
    - [💡 Benefits](#-benefits)
  - [🧪 Testing Documentation](#-testing-documentation)
    - [📂 Test Structure](#-test-structure)
    - [🔬 Unit Tests](#-unit-tests)
    - [📡 API Testing with HTTP Files](#-api-testing-with-http-files)
    - [🏃 Running Tests](#-running-tests)
  - [📚 Documentation](#-documentation)
  - [🛠️ Development Workflow](#️-development-workflow)
  - [🌐 API Endpoints](#-api-endpoints)

## 📖 Requirements Overview

**Product idea:** A secure, cloud-hosted system for managing electronic health records (EHRs). The design must satisfy regulatory requirements for resilience and disaster recovery (DR).

### 🔄 Replication Requirement

- **Primary replication:** Master–slave (primary/replica) replication to provide high availability and read-scaling within the primary region.
- **Disaster Recovery (DR) replica:** An additional, geographically separated asynchronous replica located in a different availability zone or region to meet regulatory DR requirements and protect against regional outages.

### ✨ Key Benefits

- **🔥 Disaster recovery:** If an entire data center or region fails, the remote DR replica can be brought online to restore service and minimize downtime.
- **📋 Regulatory compliance:** Off-site, asynchronous replicas help satisfy regulations that mandate geographically separated backups and recoverability.
- **🏥 Patient-care continuity:** Reduces the risk of prolonged service interruption, helping clinicians access critical patient records when needed.

### 📝 Notes / Recommendations

- Define and document RTO (Recovery Time Objective) and RPO (Recovery Point Objective) for both primary and DR replicas.
- Perform regular DR drills and failover testing to validate recovery procedures.
- Monitor replication lag and automated alerts for replica health and data consistency.

## ⚙️ Technical Specifications

### 🏗️ Architecture Overview

The Patient Health Record (PHR) system implements a **Clean Architecture** pattern with a focus on high availability, disaster recovery, and regulatory compliance. The architecture separates concerns into distinct layers: domain, application, infrastructure, and presentation.

### 💻 Technology Stack

#### 🐍 Backend

- **Language:** Python 3.12
- **Web Framework:** FastAPI 0.121.2
- **Data Validation:** Pydantic 2.12.4
- **ORM:** SQLAlchemy 2.0.44
- **ASGI Server:** Uvicorn 0.38.0
- **HTTP Client:** HTTPX 0.28.1
- **Testing:** Pytest 9.0.1
- **Environment Management:** python-dotenv 1.0.0

#### 🗄️ Database Layer

- **Primary Database:** PostgreSQL 15.13
- **Replication Type:** Streaming Replication (WAL-based)
- **Database Driver:** psycopg2-binary 2.9.9
- **Connection Pooling:** SQLAlchemy QueuePool
  - Pool size: 5 connections (configurable)
  - Max overflow: 10 connections
  - Pool timeout: 30 seconds
  - Pool recycle: 3600 seconds (1 hour)

#### 🐳 Containerization & Orchestration

- **Container Runtime:** Docker
- **Orchestration:** Docker Compose
- **Base Image:** postgres:15.13

### 🗄️ Database Architecture

#### 🔗 Database Topology

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

#### ⚙️ Database Configuration

**Primary Database (db-main):**

- **Host:** localhost:5432
- **Database Name:** `db_patient_health_record`
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

#### 🔄 Replication Features

1. **📡 Streaming Replication**

   - Real-time WAL (Write-Ahead Log) streaming from primary to replica
   - Sub-second replication lag under normal conditions
   - Automatic recovery on connection interruptions

2. **✅ Data Consistency**

   - All write operations committed to primary before returning success
   - Replica receives changes through continuous WAL streaming
   - Automatic conflict resolution (primary always wins)

3. **🔝 High Availability**
   - Health checks configured with 10-second intervals
   - Automatic container restart on failure
   - Network isolation through dedicated Docker bridge network

### � Database Replication Implementation

#### 🎯 Replication Overview

The PHR system implements **PostgreSQL Streaming Replication** using Write-Ahead Log (WAL) shipping to maintain real-time data synchronization between the primary database and two replica databases. This implementation provides high availability, read scalability, and disaster recovery capabilities.

#### 🏗️ Replication Architecture

```
                          ┌─────────────────────────────────────┐
                          │     Replication Network             │
                          │     (Docker Bridge Network)         │
                          │                                     │
                          │                                     │
┌─────────────────────────┼─────────────────────────────────────┼──────────────────────────┐
│                         │                                     │                          │
│  ┌──────────────────────▼─────────┐                           │                          │
│  │       db-main (Primary)         │                           │                          │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │                           │                          │
│  │  Port: 5432                     │                           │                          │
│  │  Role: Master/Primary           │                           │                          │
│  │  Operations: READ + WRITE       │                           │                          │
│  │                                 │                           │                          │
│  │  WAL Configuration:             │                           │                          │
│  │  • wal_level = replica          │                           │                          │
│  │  • max_wal_senders = 5          │                           │                          │
│  │  • max_replication_slots = 3    │                           │                          │
│  │  • archive_mode = on            │                           │                          │
│  └─────────┬──────────────┬────────┘                           │                          │
│            │              │                                    │                          │
│            │ WAL Stream   │ WAL Stream                         │                          │
│            │              │                                    │                          │
│   ┌────────▼────────┐  ┌──▼──────────────┐                    │                          │
│   │  db-slave-01    │  │  db-slave-02    │                    │                          │
│   │   (Replica 1)   │  │   (Replica 2)   │                    │                          │
│   │  ─────────────  │  │  ─────────────  │                    │                          │
│   │  Port: 5433     │  │  Port: 5434     │                    │                          │
│   │  Role: Hot      │  │  Role: Hot      │                    │                          │
│   │  Standby        │  │  Standby        │                    │                          │
│   │  Operations:    │  │  Operations:    │                    │                          │
│   │  READ ONLY      │  │  READ ONLY      │                    │                          │
│   │                 │  │                 │                    │                          │
│   │  Recovery:      │  │  Recovery:      │                    │                          │
│   │  • hot_standby  │  │  • hot_standby  │                    │                          │
│   │    = on         │  │    = on         │                    │                          │
│   │  • primary_     │  │  • primary_     │                    │                          │
│   │    conninfo     │  │    conninfo     │                    │                          │
│   └─────────────────┘  └─────────────────┘                    │                          │
│                                                                │                          │
└────────────────────────────────────────────────────────────────┴──────────────────────────┘
```

#### 🛠️ Primary Database Configuration (db-main)

The primary database is configured as the master node that handles all write operations and streams WAL records to replicas.

**Setup Process (`setup-replication.sh`):**

1. **🔑 Replication User Creation**

   ```sql
   CREATE USER repl_user WITH REPLICATION
   ENCRYPTED PASSWORD 'your_secure_replication_password';
   ```

   - Dedicated user with `REPLICATION` privilege
   - Used exclusively for replication connections
   - Separate from application database user

2. **⚙️ PostgreSQL Configuration (`postgresql.conf`)**

   ```ini
   # Core replication settings
   listen_addresses = '*'              # Accept connections from any IP
   wal_level = replica                 # Enable WAL for replication
   max_wal_senders = 5                 # Support up to 5 concurrent replicas
   max_replication_slots = 3           # One slot per replica for reliability
   ```

3. **🔐 Authentication Configuration (`pg_hba.conf`)**

   ```
   host replication repl_user 0.0.0.0/0 md5
   ```

   - Allows replication connections from any IP in the Docker network
   - MD5 password authentication (upgradeable to SCRAM-SHA-256)
   - Restricted to the `replication` database

4. **🔄 Configuration Reload**
   ```sql
   SELECT pg_reload_conf();
   ```
   - Applies configuration changes without restart
   - Ensures settings take effect immediately

**Dockerfile Configuration:**

```dockerfile
# Environment variables
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=123456
ENV POSTGRES_DB=db_patient_health_record
ENV REPLICATION_USER=repl_user
ENV REPLICATION_PASSWORD=your_secure_replication_password

# Migration scripts executed on initialization
COPY migrations/2025-11-18/*.sql /docker-entrypoint-initdb.d/

# Replication setup script (executed as last init script)
COPY scripts/setup-replication.sh /docker-entrypoint-initdb.d/99-setup-replication.sh

# Management scripts
COPY scripts/add-listener.sh /manage-db/add-listener.sh
```

#### 🔄 Replica Database Configuration (db-slave-01, db-slave-02)

Replica databases are configured as hot standby nodes that continuously stream changes from the primary.

**Setup Process (`setup-replica.sh`):**

1. **🧹 Data Directory Preparation**

   ```bash
   # Remove existing data to ensure clean replication
   rm -rf "$PGDATA"/*
   ```

   - Ensures no conflicting data exists
   - Prepares for base backup from primary

2. **⏳ Primary Server Readiness Check**

   ```bash
   until PGPASSWORD="$REPLICATION_PASSWORD" \
     pg_isready -h db-main -p 5432 -U "$REPLICATION_USER"; do
     echo "⏳ Waiting for primary server (db-main) to be ready..."
     sleep 3
   done
   ```

   - Waits for primary database to be fully operational
   - Uses Docker network DNS resolution (`db-main` hostname)
   - Prevents replication setup failures due to timing issues

3. **📦 Base Backup Creation**

   ```bash
   PGPASSWORD="$REPLICATION_PASSWORD" pg_basebackup \
     -h db-main \
     -D "$PGDATA" \
     -U "$REPLICATION_USER" \
     -v \           # Verbose output
     -P \           # Progress reporting
     -W \           # Force password prompt (use PGPASSWORD env)
     -R             # Create standby configuration automatically
   ```

   - Clones entire database from primary using streaming protocol
   - Creates initial data consistency point
   - Automatically generates replication configuration

4. **⚙️ Standby Configuration**

   ```ini
   # postgresql.conf additions
   hot_standby = on
   primary_conninfo = 'host=db-main port=5432
                       user=repl_user
                       password=your_secure_replication_password'
   ```

   - `hot_standby`: Enables read queries on replica
   - `primary_conninfo`: Connection string for streaming replication

5. **🔒 Permissions Setup**
   ```bash
   chmod 700 "$PGDATA"
   chown -R postgres:postgres "$PGDATA"
   ```
   - Ensures proper security for data directory
   - Required by PostgreSQL for operation

**Dockerfile Configuration:**

```dockerfile
# Environment variables (must match primary)
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=123456
ENV POSTGRES_DB=db_patient_health_record
ENV REPLICATION_USER=repl_user
ENV REPLICATION_PASSWORD=your_secure_replication_password

# Migration scripts (for schema reference, not executed)
COPY migrations/2025-11-18/*.sql /docker-entrypoint-initdb.d/

# Replica setup script
COPY scripts/setup-replica.sh /usr/local/bin/setup-replica.sh

# Custom entrypoint to run setup before postgres
ENTRYPOINT ["/bin/bash", "-c",
  "/usr/local/bin/setup-replica.sh && docker-entrypoint.sh postgres"]
```

#### 🐳 Docker Compose Orchestration

**Service Dependencies:**

```yaml
db-slave-01:
  depends_on:
    db-main:
      condition: service_healthy # Wait for primary to be healthy
```

**Health Check Configuration:**

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U admin -d db_patient_health_record"]
  interval: 10s
  timeout: 5s
  retries: 5
```

- Ensures database is ready before dependents start
- Prevents replication setup failures
- Enables orchestration-level health monitoring

**Network Configuration:**

```yaml
networks:
  replication-network:
    driver: bridge
```

- Isolated network for database communication
- DNS resolution between services (db-main, db-slave-01, db-slave-02)
- Security through network segmentation

**Volume Persistence:**

```yaml
volumes:
  db-main:
    driver: local
  db-slave-01:
    driver: local
  db-slave-02:
    driver: local
```

- Separate volumes for each database instance
- Data persists across container restarts
- Enables backup and disaster recovery

#### 📊 Replication Monitoring

**Check Replication Status (Primary):**

```sql
SELECT * FROM pg_stat_replication;
```

Returns information about active replication connections:

- `application_name`: Replica identifier
- `state`: streaming, catchup, or startup
- `sent_lsn`, `write_lsn`, `flush_lsn`: WAL positions
- `sync_state`: async or sync

**Check Replica Status (Replica):**

```sql
-- Verify running in recovery mode
SELECT pg_is_in_recovery();  -- Should return 't' (true)

-- Check replication lag
SELECT
    now() - pg_last_xact_replay_timestamp() AS replication_lag;
```

**Monitor WAL Status:**

```sql
-- Primary: Check WAL sender processes
SELECT pid, usename, application_name, client_addr, state, sync_state
FROM pg_stat_replication;

-- Replica: Check WAL receiver status
SELECT status, received_lsn, last_msg_send_time, last_msg_receipt_time
FROM pg_stat_wal_receiver;
```

#### 🔄 Replication Workflow

**Write Operation Flow:**

```
1. Application → db-main (Port 5432)
2. db-main processes INSERT/UPDATE/DELETE
3. db-main writes changes to WAL
4. WAL sender processes stream changes to replicas
5. db-slave-01 & db-slave-02 receive and apply WAL records
6. Replicas become queryable for reads (hot standby)
```

**Read Operation Flow:**

```
1. Application → db-slave-01 (Port 5433) OR db-slave-02 (Port 5434)
2. Replica serves read-only queries
3. Load distributed across replicas
4. Primary database freed for write operations
```

#### 🛡️ Replication Features & Benefits

1. **🚀 Zero Downtime Reads**

   - Read queries served by replicas without impacting primary
   - Horizontal read scalability with multiple replicas
   - Reduced latency through load distribution

2. **🔄 Continuous Synchronization**

   - Near real-time data replication (sub-second lag typical)
   - Asynchronous streaming for performance
   - Automatic reconnection on network interruptions

3. **💪 High Availability**

   - Replicas can be promoted to primary on failure
   - Manual failover capability with minimal data loss
   - Foundation for automatic failover implementations

4. **📈 Performance Benefits**

   - Read load offloaded from primary
   - Primary dedicated to write operations
   - Improved application response times

5. **🔒 Data Protection**
   - Multiple copies of data across containers
   - Point-in-time recovery capability
   - Protection against data corruption on single node

#### ⚠️ Operational Considerations

**Connection Management:**

```
Primary (Write):  postgresql://admin:123456@localhost:5432/db_patient_health_record
Replica 1 (Read): postgresql://admin:123456@localhost:5433/db_patient_health_record
Replica 2 (Read): postgresql://admin:123456@localhost:5434/db_patient_health_record
```

**Application Configuration Best Practices:**

- Configure separate connection pools for read and write operations
- Route write operations exclusively to primary (port 5432)
- Distribute read operations across replicas (ports 5433, 5434)
- Implement retry logic for transient replication lag
- Monitor replication lag and adjust routing accordingly

**Replication Lag Management:**

- Typical lag: < 1 second under normal load
- Monitor using `pg_stat_replication` and `pg_last_xact_replay_timestamp()`
- Consider read-after-write consistency requirements
- Route critical reads to primary if consistency required

**Maintenance Operations:**

- Replicas automatically apply schema changes from primary
- No manual intervention required for DDL statements
- Vacuum and analyze operations replicated automatically
- Index creation replicated to maintain query performance

#### 🚨 Failover Procedures

**Manual Failover (Promote Replica to Primary):**

1. **Stop Primary (if accessible):**

   ```bash
   docker stop db-main
   ```

2. **Promote Replica:**

   ```bash
   docker exec -it db-slave-01 \
     psql -U admin -d db_patient_health_record \
     -c "SELECT pg_promote();"
   ```

3. **Update Application Configuration:**

   - Redirect write traffic to newly promoted primary
   - Update connection strings to use new primary address

4. **Rebuild Failed Primary as Replica:**
   - Follow replica setup process
   - Point to new primary for replication

**Recovery After Failover:**

- Review application logs for failed transactions during outage
- Verify data consistency across all replicas
- Update monitoring and alerting to reflect new topology
- Document incident and recovery procedure

#### 📋 Replication Setup Verification

**Step-by-Step Validation:**

1. **Start Services:**

   ```bash
   docker-compose up -d --build
   ```

2. **Verify Primary Status:**

   ```bash
   docker exec -it db-main \
     psql -U admin -d db_patient_health_record \
     -c "SELECT * FROM pg_stat_replication;"
   ```

   Expected: Two rows showing connections from db-slave-01 and db-slave-02

3. **Verify Replica Status:**

   ```bash
   docker exec -it db-slave-01 \
     psql -U admin -d db_patient_health_record \
     -c "SELECT pg_is_in_recovery();"
   ```

   Expected: `t` (true)

4. **Test Data Replication:**

   ```bash
   # Insert on primary
   docker exec -it db-main \
     psql -U admin -d db_patient_health_record \
     -c "INSERT INTO PatientRegister (first_name, last_name,
          date_of_birth, email, phone_number, address, emergency_contact)
         VALUES ('Test', 'User', '1990-01-01', 'test@example.com',
          '1234567890', '123 Test St', 'Emergency Contact');"

   # Verify on replica
   docker exec -it db-slave-01 \
     psql -U admin -d db_patient_health_record \
     -c "SELECT * FROM PatientRegister WHERE first_name = 'Test';"
   ```

   Expected: Data appears on replica within seconds

#### 🔧 Troubleshooting

**Replica Not Connecting:**

- Verify network connectivity: `docker exec ubuntu-service ping db-main`
- Check primary logs: `docker logs db-main`
- Verify replication user credentials
- Ensure `pg_hba.conf` allows replication connections

**Replication Lag:**

- Check network latency between containers
- Monitor primary server load and I/O performance
- Review `max_wal_senders` configuration
- Consider increasing WAL retention with `wal_keep_size`

**Replica Stuck in Recovery:**

- Check replica logs: `docker logs db-slave-01`
- Verify WAL files available on primary
- Ensure no corruption in `$PGDATA` directory
- Consider rebuilding replica with fresh `pg_basebackup`

#### 🚀 Future Enhancements

1. **🌍 Geographic Distribution**

   - Deploy replicas in different AWS regions or availability zones
   - Implement cascading replication for hierarchical topology
   - Add disaster recovery replica with delayed apply

2. **🤖 Automatic Failover**

   - Integrate with Patroni or repmgr for automatic failover
   - Implement VIP (Virtual IP) for transparent failover
   - Configure automatic promotion of healthy replica

3. **📊 Advanced Monitoring**

   - Deploy Prometheus exporters for PostgreSQL metrics
   - Configure Grafana dashboards for replication visualization
   - Set up alerts for replication lag thresholds

4. **🔄 Synchronous Replication**
   - Configure `synchronous_standby_names` for critical data
   - Ensure zero data loss on failover
   - Balance performance vs. consistency requirements

### �📊 Data Model

#### 👤 PatientRegister Entity

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

### 🏛️ Application Architecture

#### 📁 Layer Structure

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

#### 🎨 Design Patterns

1. **🗂️ Repository Pattern**

   - Abstract data access through repository interfaces
   - Clean separation between domain and infrastructure
   - Enables easy testing with mock repositories

2. **🎯 Use Case Pattern**

   - Business logic encapsulated in dedicated use case classes
   - Single Responsibility: Each use case handles one business operation
   - Example: `CreatePatientRegisterUseCase`

3. **🏗️ Domain-Driven Design (DDD)**

   - Bounded contexts for different business capabilities
   - Domain models with built-in validation
   - Rich domain entities with behavior

4. **💉 Dependency Injection**
   - Loose coupling between layers
   - Constructor injection for repositories
   - Facilitates unit testing

### ✅ Data Validation Strategy

#### 🛡️ Multi-Layer Validation

1. **🔍 Domain Layer Validation (Pydantic)**

   ```python
   - String length constraints (min/max)
   - Email format validation (regex pattern)
   - Date range validation (1900-01-01 to present)
   - Phone number format (10-15 characters)
   - Required vs optional fields
   ```

2. **🗄️ Database Constraint Validation**

   ```sql
   - NOT NULL constraints
   - CHECK constraints (date_of_birth range)
   - VARCHAR length limits
   - Primary key uniqueness (UUID)
   ```

3. **⚠️ Error Handling**
   - Custom exceptions: `ModelErrorException`
   - Standardized responses: `CustomResponse`
   - Detailed error messages with field-level context

### 🔐 Security Considerations

#### 🔒 Database Security

- Authentication required for all database connections
- Separate replication user with limited privileges
- MD5 password authentication (upgrade to SCRAM-SHA-256 for production)
- Network isolation through Docker networks

#### 🛡️ Application Security

- Input validation at multiple layers
- SQL injection prevention through ORM (SQLAlchemy)
- Environment variable configuration (no hardcoded credentials)
- Connection pooling prevents resource exhaustion

### ⚡ Performance Optimizations

1. **🔌 Connection Pooling**

   - Pre-established database connections
   - Reduces connection overhead
   - Configurable pool size based on load

2. **📖 Read Scaling**

   - Write operations to primary (db-main)
   - Read operations distributed to replica (db-slave)
   - Reduces load on primary database

3. **🔄 Asynchronous Processing**
   - ASGI server (Uvicorn) for async request handling
   - FastAPI native async support
   - Non-blocking I/O operations

### 📈 Monitoring & Observability

#### 💚 Health Checks

- **Database Health:** `pg_isready` checks every 10 seconds
- **Replication Status:** `pg_stat_replication` view
- **Replica Lag:** `pg_last_xact_replay_timestamp()` monitoring

#### 📋 Logging

- SQLAlchemy query logging (development mode)
- Application-level error logging
- Replication setup logs for debugging

### 🚀 Deployment Configuration

#### 🔧 Environment Variables

```bash
# Database Connection
POSTGRES_USER=admin
POSTGRES_PASSWORD=****** (secured)
POSTGRES_DB=db_patient_health_record
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Connection Pool
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

#### 🌐 Docker Network

- **Network Name:** `replication-network`
- **Driver:** bridge
- **Purpose:** Isolated communication between db-main and db-slave
- **DNS Resolution:** Containers resolve each other by service name

#### 💾 Volumes

- **db-main:** Persistent storage for primary database
- **db-slave:** Persistent storage for replica database
- **Driver:** local
- **Lifecycle:** Persist beyond container lifecycle

### 🧪 Testing Strategy

#### 🔬 Unit Testing

- **Framework:** Pytest 9.0.1
- **Scope:** Domain models, use cases, repositories
- **Isolation:** Mock database connections
- **Coverage:** Business logic validation

#### 📂 Test Structure

```
test/
    └── unit/
        └── create_patient_register/
            └── application/
                └── test_create_patient_register.py
```

### 📏 Scalability Considerations

#### 📊 Current Implementation

- Single primary, single replica architecture
- Suitable for small to medium workloads
- Foundation for horizontal scaling

#### 🚀 Future Enhancements

1. **📚 Multiple Read Replicas**

   - Add more db-slave instances
   - Load balance read queries across replicas
   - Geographic distribution for reduced latency

2. **🔌 Connection Pooling Service**

   - PgBouncer for connection management
   - Reduced connection overhead
   - Better resource utilization

3. **🔄 Automatic Failover**

   - Patroni or repmgr for HA management
   - Automatic primary promotion
   - VIP (Virtual IP) for transparent failover

4. **🌍 Disaster Recovery Region**
   - Geographically separated async replica
   - Cross-region replication
   - Regulatory compliance for data residency

### 💾 Backup & Recovery

#### 📦 Current Backup Strategy

- Volume-based persistence (Docker volumes)
- Base backup through `pg_basebackup`
- WAL archiving enabled (configured for future use)

#### 🔄 Recovery Capabilities

- Point-in-time recovery (PITR) foundation
- Replica promotion to primary
- Data persistence across container restarts

### 📜 Compliance & Regulatory

#### 📋 Data Handling

- UUID-based patient identification
- Structured medical data storage
- Audit trail foundation (extensible)

#### ⏱️ Availability Targets

- **RTO (Recovery Time Objective):** < 5 minutes (manual failover)
- **RPO (Recovery Point Objective):** < 1 minute (replication lag)
- **Uptime Target:** 99.9% (foundation for HA)

## 🔍 Criteria Pattern for Querying Patient Records

The PHR system implements a sophisticated **Criteria Pattern** to provide flexible and type-safe querying capabilities for patient records. This pattern allows dynamic query construction with filters, ordering, and pagination.

### 🎯 Pattern Overview

The Criteria Pattern decouples query construction from query execution, enabling:

- **Dynamic filtering** based on various patient attributes
- **Flexible ordering** (ascending/descending)
- **Pagination** support for large datasets
- **Type safety** through structured classes
- **SQL injection prevention** through parameterized queries

### 🧩 Components

#### 1. **Filter Class** (`src/app/shared/domain/criteria/criteria.py`)

Represents a single query filter with field, operator, and value:

```python
class Filter:
    def __init__(self, field: str, operator: str, value: any):
        self.field = field        # e.g., "last_name"
        self.operator = operator  # e.g., "EQUAL", "LESS_THAN"
        self.value = value        # e.g., "Smith"
```

**Supported Operators:**

- `EQUAL` → `=`
- `NOT_EQUAL` → `!=`
- `LESS_THAN` → `<`
- `LESS_THAN_OR_EQUAL` → `<=`
- `GREATER_THAN` → `>`
- `GREATER_THAN_OR_EQUAL` → `>=`

#### 2. **Order Class**

Handles sorting of query results:

```python
class Order:
    def __init__(self, field: str, direction: OrderDirection):
        self.field = field              # e.g., "date_of_birth"
        self.direction = direction       # "ASC" or "DESC"
```

#### 3. **Pagination Class**

Manages result pagination:

```python
class Pagination:
    def __init__(self, page: int, per_page: int):
        self.page = page           # Current page number (1-based)
        self.per_page = per_page   # Results per page
```

#### 4. **Criteria Class**

Aggregates all query parameters:

```python
class Criteria:
    def __init__(self):
        self.filters: list[Filter] = []
        self.orders: Order = None
        self.pagination: Pagination = None
```

#### 5. **CriteriaParser Class**

Converts HTTP query parameters to Criteria objects:

```python
class CriteriaParser:
    def dict_to_criteria(self, query_params: dict[str, any]) -> Criteria:
        # Parses filters, orders, and pagination from query params
```

#### 6. **CriteriaToSQL Class** (`src/app/shared/domain/criteria/criteria_to_sql.py`)

Converts Criteria objects to parameterized SQL queries:

```python
class CriteriaToSQL:
    def get_select_query_parametrized(self) -> tuple[str, dict]:
        # Returns SQL query string and parameter dictionary
```

### 🔧 Implementation Details

#### Query Parameter Format

The API accepts query parameters in the following format:

```http
GET /patient-register?0_field=last_name&0_operator=EQUAL&0_value=Smith&1_field=first_name&1_operator=EQUAL&1_value=John&orderBy=date_of_birth&order=DESC&page=1&per_page=10
```

**Parameters:**

- `{n}_field`: Field name for nth filter
- `{n}_operator`: Comparison operator for nth filter
- `{n}_value`: Value to filter by for nth filter
- `orderBy`: Field to sort by
- `order`: Sort direction (ASC/DESC)
- `page`: Page number (default: 1)
- `per_page`: Results per page (default: 10)

#### SQL Generation Process

1. **Parse** query parameters into Criteria object
2. **Build** WHERE clause from filters
3. **Add** ORDER BY clause if specified
4. **Apply** pagination with LIMIT/OFFSET
5. **Return** parameterized query to prevent SQL injection

**Example Generated SQL:**

```sql
SELECT * FROM patientregister
WHERE last_name = :where_param_1 AND first_name = :where_param_2
ORDER BY date_of_birth DESC
LIMIT 10 OFFSET 0
```

With parameters: `{'where_param_1': 'Smith', 'where_param_2': 'John'}`

### 📝 Usage Example

#### In the Route Handler (`src/presentation/routes/get_patient_registation_routes.py`)

```python
@get_patient_registation_route.get("/patient-register")
async def get_patient_registration(request: Request):
    # 1. Extract query parameters
    query_params = request.query_params
    query_params_primitives = query_params.__dict__.get('_dict')

    # 2. Parse into Criteria object
    criteria_parser = CriteriaParser()
    criteria = criteria_parser.dict_to_criteria(query_params_primitives)

    # 3. Execute use case with criteria
    use_case = GetPatientRegistationUseCase(get_patient_postgress)
    props = GetPatientRegistationProps()
    props["criteria"] = criteria

    response = use_case.execute(props)
    return JSONResponse(...)
```

#### In the Repository (`src/app/get_patient_registation/infra/persistence/slave_db/get_patient_postgress.py`)

```python
def get(self, criteria) -> list[PatientRegister]:
    # 1. Convert Criteria to SQL
    criteria_to_sql = CriteriaToSQL()
    criteria_to_sql.set_table_name("patientregister")
    criteria_to_sql.set_where_by_criteria(criteria)
    criteria_to_sql.set_order_by_criteria(criteria)
    criteria_to_sql.set_pagination_by_criteria(criteria)

    # 2. Get parameterized query
    sql_query, params = criteria_to_sql.get_select_query_parametrized()

    # 3. Execute safely with parameters
    result = db.execute(text(sql_query), params)

    # 4. Map results to domain objects
    return patient_register_list
```

### 💡 Benefits

- ✅ **Type Safety**: Structured classes prevent invalid queries
- ✅ **Security**: Parameterized queries prevent SQL injection
- ✅ **Flexibility**: Dynamic query construction without code changes
- ✅ **Maintainability**: Clear separation of concerns
- ✅ **Testability**: Easy to unit test individual components
- ✅ **Read Optimization**: Queries execute on read replica (db-slave)
- ✅ **Scalability**: Efficient pagination for large datasets

## 🧪 Testing Documentation

The PHR system implements comprehensive testing strategies covering unit tests and API endpoint testing to ensure code quality and reliability.

### 📂 Test Structure

```
backend/
├── test/                           # Test directory
│   └── unit/                       # Unit tests
│       └── create_patient_register/
│           └── application/
│               └── test_create_patient_register.py
├── docs/                           # API testing files
│   ├── create-patient-record.http  # POST endpoint tests
│   └── get-patient-record.http     # GET endpoint tests with criteria
└── pytest.ini                      # Pytest configuration
```

### 🔬 Unit Tests

Located in: `backend/test/unit/`

#### Test Framework: Pytest 9.0.1

**Configuration (`pytest.ini`):**

```ini
[pytest]
python_files = test**.py
```

#### Test Coverage: `test_create_patient_register.py`

This test suite validates the `CreatePatientRegisterUseCase` with three main scenarios:

##### 1. **❌ Test Invalid Date Format**

```python
def test_create_patient_register_invalid_data(self):
    """Test invalid patient register data (wrong date_of_birth format)."""
```

- **Purpose**: Validates Pydantic validation for malformed date strings
- **Input**: Invalid date format `"1980-01-1998"`
- **Expected**: HTTP 400 response with validation error
- **Assertion**: `response.code == 400` and `response.is_success is False`

##### 2. **⚠️ Test Out-of-Range Date**

```python
def test_create_patient_register_out_of_range(self):
    """Test patient register data with out-of-range date_of_birth."""
```

- **Purpose**: Validates business rule enforcement (dates between 1900-01-01 and present)
- **Input**: Date before minimum allowed `"1880-01-01"`
- **Expected**: HTTP 400 with specific error details
- **Assertions**:
  - `response.code == 400`
  - `response.message == "Data validation error"`
  - `response.data['property'] == "date_of_birth"`

##### 3. **✅ Test Valid Patient Creation**

```python
def test_create_patient_register_valid_data(self):
    """Test valid patient register data."""
```

- **Purpose**: Validates successful patient record creation
- **Input**: Complete valid patient data with UUID
- **Expected**: HTTP 200 with patient data in response
- **Assertions**:
  - `response.code == 200`
  - `response.is_success is True`
  - `response.message == "Patient register created successfully"`
  - `response.data is not None`

#### Test Setup & Teardown

```python
def setup_method(self, method):
    """Setup code before each test."""
    createPatientRegisterPostgress = CreatePatientRegisterPostgress()
    self.create_patient_repo = createPatientRegisterPostgress
    self.use_case = CreatePatientRegisterUseCase(self.create_patient_repo)

def teardown_method(self, method):
    """Teardown code after each test."""
    pass
```

### 📡 API Testing with HTTP Files

Located in: `backend/docs/`

These files allow manual and automated API endpoint testing using HTTP client extensions (e.g., REST Client for VS Code).

#### 1. **Create Patient Record** (`create-patient-record.http`)

```http
POST http://localhost:8000/patient-register
Content-Type: application/json

{
    "uuid": "7b878376-057d-4203-950a-f4bb4f2f9805",
    "first_name": "Jose Carlos",
    "last_name": "Huerta",
    "date_of_birth": "1990-05-15",
    "email": "jane.smith@example.com",
    "phone_number": "1234567890",
    "address": "123 Main St, Springfield",
    "emergency_contact": "John Smith",
    "allergies": ["penicillin", "latex"],
    "medical_history": ["hypertension", "asthma"],
    "current_medications": ["lisinopril", "albuterol"]
}
```

**Purpose**: Test patient record creation endpoint
**Validates**:

- Request payload structure
- Field validation (Pydantic)
- Database persistence (primary and replica)
- Event bus functionality

#### 2. **Get Patient Records with Criteria** (`get-patient-record.http`)

Multiple query examples demonstrating the Criteria Pattern:

##### Simple Filter Query:

```http
GET http://localhost:8000/patient-register?0_field=last_name&0_operator=EQUAL&0_value=Torres&page=1&per_page=1
```

##### Multiple Filters:

```http
GET http://localhost:8000/patient-register?0_field=last_name&0_operator=EQUAL&0_value=Lee&1_field=first_name&1_operator=EQUAL&1_value=Paula&page=1&per_page=1
```

##### Comparison Operators:

```http
GET http://localhost:8000/patient-register?0_field=last_name&0_operator=LESS_THAN&0_value=L&page=1&per_page=2&1_field=first_name&1_operator=EQUAL&1_value=Paula
```

**Tests validate**:

- Criteria parsing from query parameters
- SQL generation with parameterization
- Multiple filter combinations
- Pagination functionality
- Read operations on replica database

### 🏃 Running Tests

#### Run All Unit Tests:

```bash
cd backend
pytest
```

#### Run Specific Test File:

```bash
pytest test/unit/create_patient_register/application/test_create_patient_register.py
```

#### Run with Verbose Output:

```bash
pytest -v
```

#### Run with Coverage:

```bash
pytest --cov=src --cov-report=html
```

#### API Testing:

1. Install REST Client extension in VS Code
2. Open `.http` files in `backend/docs/`
3. Click "Send Request" above each HTTP request
4. View responses inline

### 🎯 Test Best Practices

1. **Isolation**: Each test is independent and doesn't affect others
2. **Mocking**: Tests use actual PostgreSQL connections (integration-style unit tests)
3. **Assertions**: Multiple assertions per test for comprehensive validation
4. **Documentation**: Clear docstrings explain test purpose
5. **Setup/Teardown**: Proper initialization and cleanup

### 🚀 Future Testing Enhancements

- 🔄 **Integration Tests**: End-to-end API testing
- 📊 **Load Testing**: Performance testing with multiple concurrent requests
- 🔐 **Security Testing**: Authentication and authorization tests
- 📈 **Coverage Goals**: Achieve >80% code coverage
- 🤖 **CI/CD Integration**: Automated testing in deployment pipeline

### 📚 Documentation

- **📖 Main Documentation:** `README.md`
- **🔄 Replication Guide:** `REPLICATION_SETUP.md`
- **📋 Use Cases:** `DOCS/use-cases/`
  - 1️⃣ Create Patient Health Record
  - 2️⃣ Read Patient Health Record
  - 3️⃣ Update Patient Health Record
  - 4️⃣ Delete Patient Health Record

## 🛠️ Development Workflow

1. **💻 Local Development:** Connect to localhost:5432 (primary)
2. **🧪 Testing:** Unit tests with mocked repositories
3. **🔧 Integration Testing:** Docker Compose environment
4. **✅ Replication Verification:** Query both primary and replica

## 🌐 API Endpoints

**Current Implementation:**

```
POST   /patient-register                # ✅ Create patient record (Implemented)
GET    /patient-register                # ✅ Query patient records with criteria (Implemented)
```

**Future Implementation:**

```
GET    /api/v1/patients/{uuid}          # 🔄 Read specific patient record
PUT    /api/v1/patients/{uuid}          # 🔄 Update patient record
DELETE /api/v1/patients/{uuid}          # 🔄 Delete patient record
GET    /api/v1/health                   # 🔄 System health check
GET    /api/v1/replication/status       # 🔄 Replication status
```
