# Patient Health Record (PHR) System

**Product idea:** A secure, cloud-hosted system for managing electronic health records (EHRs). The design must satisfy regulatory requirements for resilience and disaster recovery (DR).

## Replication requirement

- **Primary replication:** Master–slave (primary/replica) replication to provide high availability and read-scaling within the primary region.
- **Disaster Recovery (DR) replica:** An additional, geographically separated asynchronous replica located in a different availability zone or region to meet regulatory DR requirements and protect against regional outages.

## Key benefits

- **Disaster recovery:** If an entire data center or region fails, the remote DR replica can be brought online to restore service and minimize downtime.
- **Regulatory compliance:** Off-site, asynchronous replicas help satisfy regulations that mandate geographically separated backups and recoverability.
- **Patient-care continuity:** Reduces the risk of prolonged service interruption, helping clinicians access critical patient records when needed.

## Notes / Recommendations

- Define and document RTO (Recovery Time Objective) and RPO (Recovery Point Objective) for both primary and DR replicas.
- Perform regular DR drills and failover testing to validate recovery procedures.
- Monitor replication lag and automated alerts for replica health and data consistency.
