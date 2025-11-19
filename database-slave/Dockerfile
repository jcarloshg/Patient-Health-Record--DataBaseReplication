FROM postgres:15.13

ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=123456
ENV POSTGRES_DB=db_patient_health_record

# Copy the replica setup script
COPY scripts/setup-replica.sh /usr/local/bin/setup-replica.sh
RUN chmod +x /usr/local/bin/setup-replica.sh

# Override the default entrypoint to run replica setup
ENTRYPOINT ["/bin/bash", "-c", "/usr/local/bin/setup-replica.sh && docker-entrypoint.sh postgres"]

EXPOSE 5432