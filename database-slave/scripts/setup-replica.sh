#!/bin/bash
set -e

# This script configures PostgreSQL as a replica (slave) server

echo "🔧 Setting up PostgreSQL replica server..."

# Remove existing data directory contents (replica will sync from primary)
if [ -d "$PGDATA" ] && [ "$(ls -A $PGDATA)" ]; then
    echo "⚠️  Cleaning existing data directory for replica setup..."
    rm -rf "$PGDATA"/*
fi

# Wait for primary server to be ready
until PGPASSWORD='replicator_password' pg_isready -h db-main -p 5432 -U replicator; do
  echo "⏳ Waiting for primary server (db-main) to be ready..."
  sleep 3
done

echo "✅ Primary server is ready"

# Use pg_basebackup to clone the primary database
echo "📦 Cloning database from primary server..."
PGPASSWORD='replicator_password' pg_basebackup \
    -h db-main \
    -D "$PGDATA" \
    -U replicator \
    -v \
    -P \
    -W \
    -R

echo "✅ Base backup completed"

# Configure standby settings
cat >> "$PGDATA/postgresql.conf" <<EOF

# --- Standby Settings ---
hot_standby = on
primary_conninfo = 'host=db-main port=5432 user=replicator password=replicator_password'
EOF

echo "✅ Standby configuration completed"

# Set proper permissions
chmod 700 "$PGDATA"
chown -R postgres:postgres "$PGDATA"

echo "🎉 Replica server setup completed!"
