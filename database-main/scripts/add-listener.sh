#!/bin/bash
set -e


echo ""
echo " ======== Configure pg_hba.conf to allow replication connections - Start ======== "
echo ""
echo "host replication ${REPLICATION_USER} 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"

# Check for required argument (IP address)
if [ -z "$1" ]; then
	echo "Usage: $0 <REPLICATION_CLIENT_IP>"
	exit 1
fi

REPLICATION_CLIENT_IP="$1"

echo "host replication ${REPLICATION_USER} ${REPLICATION_CLIENT_IP} md5" >> "$PGDATA/pg_hba.conf"
echo "✅ Authentication configuration updated"


# echo "Restarting PostgreSQL to apply changes..."
# systemctl restart postgresql

echo "Reload PostgreSQL configuration to apply changes to postgresql.conf and pg_hba.conf"
# This is crucial as the changes are written to disk.
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT pg_reload_conf();"

# echo "Current contents of \$PGDATA/pg_hba.conf:"
# cat "$PGDATA/pg_hba.conf"

echo ""
echo " ======== Configure pg_hba.conf to allow replication connections - End ======== "
echo ""


# // ─────────────────────────────────────
# How to run the script
# // ─────────────────────────────────────

# 1. Make sure the script has execute permissions. If not, run:
# chmod +x add-listener.sh

# 2. run the script with the IP address of the replication client as an argument:
# ./add-listener.sh 000.000.0.000