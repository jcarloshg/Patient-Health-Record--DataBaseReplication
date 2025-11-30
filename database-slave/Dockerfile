FROM postgres:15.13


# 1. Set environment variables
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=123456
ENV POSTGRES_DB=db_patient_health_record
# Replication settings (match db-main)
ENV REPLICATION_USER=repl_user
ENV REPLICATION_PASSWORD=your_secure_replication_password

# 2. Copy migration scripts to be executed automatically on container startup
COPY migrations/2025-11-18/*.sql /docker-entrypoint-initdb.d/

# 3. Copy the replica setup script
COPY scripts/setup-replica.sh /usr/local/bin/setup-replica.sh
RUN chmod +x /usr/local/bin/setup-replica.sh

# 4. Override the default entrypoint to run replica setup
ENTRYPOINT ["/bin/bash", "-c", "/usr/local/bin/setup-replica.sh && docker-entrypoint.sh postgres"]

EXPOSE 5432