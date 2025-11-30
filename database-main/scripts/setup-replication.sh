#!/bin/bash
set -e

# This script configures PostgreSQL as a primary (master) server for replication

echo ""
echo "=========================================================== "
echo "=========================================================== "
echo " Starting "
echo "🔧 Configuring PostgreSQL primary server for replication..."
echo ""
echo "=========================================================== "
echo "=========================================================== "
echo ""


echo ""
echo " ======== Createing Replication User - Start ======== "
echo ""

# Wait for PostgreSQL to start
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done

# --- Create Replication User using Environment Variables ---
echo "Creating replication user: ${REPLICATION_USER}"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create replication user if it doesn't exist
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '${REPLICATION_USER}') THEN
            CREATE USER ${REPLICATION_USER} WITH REPLICATION ENCRYPTED PASSWORD '${REPLICATION_PASSWORD}';
        END IF;
    END
    \$\$;
EOSQL


echo ""
echo "✅ Replication user created successfully"
echo " ======== Createing Replication User - End ======== "
echo ""


echo ""
echo " ======== Configure postgresql.conf for replication - Start ======== "
echo ""
# Note: $PGDATA is the default location for the data directory in the official PostgreSQL image
cat >> "$PGDATA/postgresql.conf" <<EOF

# --- Replication Settings ---
# Core settings for replication
listen_addresses = '*'    # Allows external connections from replicas

# Replication settings
wal_level = replica
max_wal_senders = 5     # Enough for 3 replicas + 2 spare slots
max_replication_slots = 3 # One slot per replica for robust replication
# port = 5432

EOF

echo ""
echo "✅ PostgreSQL configuration updated"
echo " ======== Configure postgresql.conf for replication - End ======== "
echo ""



echo ""
echo " ======== Configure pg_hba.conf to allow replication connections - Start ======== "
echo ""

echo "host replication ${REPLICATION_USER} 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"

echo "✅ Authentication configuration updated"

# Reload PostgreSQL configuration to apply changes to postgresql.conf and pg_hba.conf
# This is crucial as the changes are written to disk.
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT pg_reload_conf();"

echo ""
echo " ======== Configure pg_hba.conf to allow replication connections - End ======== "
echo ""


echo ""
echo "=========================================================== "
echo "=========================================================== "
echo " Ending "
echo "🔧 Configuring PostgreSQL primary server for replication..."
echo "🎉 Primary server configuration completed! The primary is ready for replicas to connect."
echo ""
echo "=========================================================== "
echo "=========================================================== "
echo ""