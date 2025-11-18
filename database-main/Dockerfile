FROM postgres:15.13

ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=123456
ENV POSTGRES_DB=main-db_patient_health_record

# Copy migration scripts to be executed automatically on container startup
COPY migrations/2025-11-18/*.sql /docker-entrypoint-initdb.d/

EXPOSE 5432