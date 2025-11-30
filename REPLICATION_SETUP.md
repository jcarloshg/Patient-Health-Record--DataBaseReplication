# PostgreSQL Streaming Replication Setup

This project implements PostgreSQL streaming replication with a primary (master) and replica (slave) database configuration.

## Architecture

- **db-main (Primary)**: The main database where all write operations occur
- **db-slave (Replica)**: The replica database that synchronizes data from the primary in real-time

## How It Works

1. **Primary Database (`db-main`)**:
   - Accepts all write operations (INSERT, UPDATE, DELETE)
   - Configured with Write-Ahead Logging (WAL) to stream changes
   - Creates a replication user with appropriate permissions
   - Port: 5432

2. **Replica Database (`db-slave`)**:
   - Automatically synchronizes all data from the primary
   - Read-only mode (hot standby)
   - Uses `pg_basebackup` to clone initial data from primary
   - Continuously streams WAL changes from primary
   - Port: 5433

## Setup Instructions

### 1. Start the Databases

```bash
# Build and start both databases
docker-compose up -d --build

# Check the logs
docker-compose logs -f
```

### 2. Verify Replication Status

#### On Primary (db-main):
```bash
# Check replication status
docker exec -it db-main psql -U admin -d db_patient_health_record -c "SELECT * FROM pg_stat_replication;"

# You should see the replica connection listed
```

#### On Replica (db-slave):
```bash
# Check if running in recovery mode (replica mode)
docker exec -it db-slave psql -U admin -d db_patient_health_record -c "SELECT pg_is_in_recovery();"

# Should return 't' (true)
```

### 3. Test Replication

#### Insert data on Primary:
```bash
docker exec -it db-main psql -U admin -d db_patient_health_record -c "
INSERT INTO PatientRegister (first_name, last_name, date_of_birth, email, phone_number, address, emergency_contact)
VALUES ('John', 'Doe', '1990-01-01', 'john.doe@example.com', '1234567890', '123 Main St', 'Jane Doe');
"
```

#### Verify data on Replica:
```bash
docker exec -it db-slave psql -U admin -d db_patient_health_record -c "SELECT * FROM PatientRegister;"
```

The data should appear on the replica within seconds!

## Important Notes

### Write Operations
- **Only write to `db-main`** (port 5432)
- The replica (`db-slave`) is **read-only**
- Any write attempts to the replica will fail

### Connection Strings

**Primary (Write):**
```
postgresql://admin:123456@localhost:5432/db_patient_health_record
```

**Replica (Read):**
```
postgresql://admin:123456@localhost:5433/db_patient_health_record
```

### Application Configuration

In your application, configure:
- **Write operations**: Connect to `db-main:5432`
- **Read operations**: Connect to `db-slave:5433` (for read scaling)

## Monitoring Replication

### Check Replication Lag
```bash
docker exec -it db-main psql -U admin -d db_patient_health_record -c "
SELECT 
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    sync_state
FROM pg_stat_replication;
"
```

### Check Replica Delay
```bash
docker exec -it db-slave psql -U admin -d db_patient_health_record -c "
SELECT 
    now() - pg_last_xact_replay_timestamp() AS replication_delay;
"
```

## Troubleshooting

### Replica not connecting:
1. Check if primary is running: `docker ps | grep db-main`
2. Check primary logs: `docker logs db-main`
3. Verify network connectivity: `docker exec db-slave ping db-main`

### Replication stopped:
1. Check replication status on primary
2. Review replica logs: `docker logs db-slave`
3. Restart replica: `docker-compose restart db-slave`

### Reset Replication:
```bash
# Stop containers
docker-compose down

# Remove volumes (WARNING: This deletes all data!)
docker volume rm patient-healt-record_db-main patient-healt-record_db-slave

# Restart
docker-compose up -d --build
```

## Technical Details

### Replication Configuration

**Primary Settings (`postgresql.conf`):**
- `wal_level = replica`: Enables WAL logging for replication
- `max_wal_senders = 10`: Maximum concurrent replication connections
- `max_replication_slots = 10`: Maximum replication slots
- `hot_standby = on`: Allows read queries on replicas

**Replica Settings:**
- `hot_standby = on`: Enables read-only queries
- `primary_conninfo`: Connection string to primary server

### Security

- Replication user: `replicator`
- Replication password: `replicator_password` (change in production!)
- Authentication: MD5 (consider using SCRAM-SHA-256 in production)

## Production Recommendations

1. **Use strong passwords** for the replication user
2. **Configure SSL/TLS** for replication connections
3. **Set up monitoring** for replication lag
4. **Configure automatic failover** using tools like Patroni or repmgr
5. **Regular backups** of both primary and replica
6. **Network isolation** using proper firewall rules
7. **Use replication slots** to prevent WAL deletion before replica catches up

## Benefits of This Setup

✅ **High Availability**: If primary fails, replica can be promoted
✅ **Read Scaling**: Distribute read queries across replicas
✅ **Data Safety**: Multiple copies of data
✅ **Disaster Recovery**: Quick recovery from failures
✅ **Zero Data Loss**: Synchronous replication option available

## Next Steps

- Set up connection pooling (PgBouncer)
- Implement automatic failover (Patroni)
- Add more replicas for better read scaling
- Configure monitoring with Prometheus + Grafana
