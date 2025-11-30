SELECT * FROM pg_stat_replication;

SELECT
    pid,
    usename,
    application_name,
    client_addr,
    state,
    sync_state
FROM pg_stat_replication;