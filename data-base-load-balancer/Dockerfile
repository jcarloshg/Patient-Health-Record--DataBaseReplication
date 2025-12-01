# File: Dockerfile.haproxy
FROM haproxy:latest

# Copy the HAProxy configuration file into the default location
COPY app/haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

# Expose the port for PostgreSQL application connections (5432)
EXPOSE 5432

# Expose the port for the optional HAProxy statistics page (8080)
EXPOSE 8080

# The base image's ENTRYPOINT already runs HAProxy, so no CMD is needed.k