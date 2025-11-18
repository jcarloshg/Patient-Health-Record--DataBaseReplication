# Patient Health Record (PHR) System - Use Cases

## Additional Use Cases for DR and Replication

### 5. Failover to DR Replica

**Actor:** System Administrator, Automated Monitoring System

**Description:** Switch operations to the disaster recovery replica when primary region is unavailable.

**Preconditions:**

- Primary region or data center is experiencing an outage
- DR replica is up-to-date within acceptable RPO

**Main Flow:**

1. Monitoring system detects primary region failure
2. System alerts administrators
3. Administrator initiates failover procedure (or automated failover triggers)
4. System promotes DR replica to primary
5. System redirects traffic to DR region
6. System continues operations with acceptable data loss (within RPO)

**Postconditions:**

- DR replica is now serving as primary
- Service is restored with minimal downtime (within RTO)
- Audit log captures failover event

---

### 6. Synchronize Replicas

**Actor:** Automated Replication System

**Description:** Continuously replicate data changes from primary to replicas.

**Preconditions:**

- Replication infrastructure is configured and operational

**Main Flow:**

1. Change occurs in primary database (Create, Update, Delete)
2. System captures change in transaction log
3. System replicates synchronously to master-slave replicas
4. System replicates asynchronously to DR replica
5. System monitors replication lag
6. System alerts if lag exceeds threshold

**Postconditions:**

- All replicas contain consistent data
- Replication lag is within acceptable limits
- System health metrics are updated

---

## Notes

- All operations must comply with HIPAA, GDPR, or applicable healthcare data regulations
- Implement role-based access control (RBAC) for all CRUD operations
- Maintain comprehensive audit trails for compliance
- Regular DR drills should test Read and Failover use cases
- Monitor replication lag continuously to ensure RPO compliance
