#!/bin/bash
set -e

# This script configures PostgreSQL as a primary (master) server for replication

echo "🔧 Configuring PostgreSQL primary server for replication..."

# Wait for PostgreSQL to start
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done

# Create replication user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create replication user if it doesn't exist
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = 'replicator') THEN
            CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';
        END IF;
    END
    \$\$;
    
    -- Grant necessary permissions
    GRANT CONNECT ON DATABASE "$POSTGRES_DB" TO replicator;
EOSQL

echo "✅ Replication user created successfully"

# Configure postgresql.conf for replication
cat >> "$PGDATA/postgresql.conf" <<EOF

# --- Replication Settings ---
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
hot_standby = on
archive_mode = on
archive_command = '/bin/true'
EOF

echo "✅ PostgreSQL configuration updated"

# Configure pg_hba.conf to allow replication connections
echo "host replication replicator 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"

echo "✅ Authentication configuration updated"

# Reload PostgreSQL configuration
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT pg_reload_conf();"

echo "🎉 Primary server configuration completed!"
