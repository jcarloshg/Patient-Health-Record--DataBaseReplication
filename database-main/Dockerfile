FROM postgres:15.13

ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=123456
ENV POSTGRES_DB=main-db_patient_health_record

# Copy migration scripts to be executed automatically on container startup
COPY migrations/2025-11-18/*.sql /docker-entrypoint-initdb.d/

# Copy replication setup script
COPY scripts/setup-replication.sh /docker-entrypoint-initdb.d/99-setup-replication.sh
RUN chmod +x /docker-entrypoint-initdb.d/99-setup-replication.sh

EXPOSE 5432