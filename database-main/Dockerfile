FROM postgres:15.13

# 1.
# Set environment variables for PostgreSQL
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=123456
ENV POSTGRES_DB=main-db_patient_health_record

#2. 
# Replication settings
ENV REPLICATION_USER=repl_user
ENV REPLICATION_PASSWORD=your_secure_replication_password

# 3.
# Copy migration scripts to be executed automatically on container startup
COPY migrations/2025-11-18/*.sql /docker-entrypoint-initdb.d/

# 4. 
# Copy replication setup script
COPY scripts/setup-replication.sh /docker-entrypoint-initdb.d/99-setup-replication.sh
# Make the replication setup script executable
RUN chmod +x /docker-entrypoint-initdb.d/99-setup-replication.sh

# Ensure the script is run on container startup
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["postgres"]


EXPOSE 5432