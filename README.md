# Self-Healing Production API Platform

A production-oriented REST API platform built with **FastAPI, SQL, Docker, Kubernetes, Prometheus, Grafana, Terraform, and GitHub Actions**.

The project combines application engineering with SRE practices to demonstrate reliable API development, automated recovery, dependency resilience, observability, and infrastructure automation.

## Architecture

```text
                         ┌──────────────────┐
                         │      Client      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   REST API       │
                         │   FastAPI        │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
           ┌─────────────────┐        ┌──────────────────┐
           │ Service Layer   │        │ Dependency API   │
           │ Business Logic  │        │ HTTP Service     │
           └────────┬────────┘        └──────────────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ Repository      │
           │ Layer           │
           └────────┬────────┘
                    │
                    ▼
              ┌───────────┐
              │  SQLite   │
              └───────────┘

              Kubernetes Cluster
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   ┌──────────────┐    ┌──────────────┐
   │ API Replica  │    │ API Replica  │
   └──────────────┘    └──────────────┘
          │
          ├── Liveness / Readiness
          ├── Resource Limits
          └── Horizontal Pod Autoscaler

          Observability
          ┌──────────────┐
          │ Prometheus   │
          └──────┬───────┘
                 ▼
          ┌──────────────┐
          │ Grafana      │
          └──────────────┘

          Infrastructure
          ┌──────────────┐
          │  Terraform   │
          └──────────────┘

          CI
          ┌──────────────┐
          │GitHub Actions│
          └──────────────┘
## Key Capabilities

### Application Engineering

- Versioned REST API using `/api/v1/items`
- CRUD operations for application resources
- Pydantic request/response validation
- Enum-based status validation
- Layered application architecture
- Service and repository separation
- SQL-backed persistence using SQLite
- Automatic OpenAPI/Swagger documentation
- Automated API tests with Pytest

### Reliability Engineering

- Kubernetes-based deployment
- Multiple API replicas
- Liveness and readiness probes
- Kubernetes self-healing after pod failure
- CPU and memory resource requests/limits
- Horizontal Pod Autoscaler
- Dependency timeout handling
- Automatic retries with bounded retry count
- Circuit breaker protection
- Graceful degradation when dependencies fail

### Observability

- Prometheus metrics
- Grafana dashboards
- HTTP request metrics
- Request latency tracking
- Error monitoring
- Kubernetes workload visibility

### Infrastructure & Automation

- Docker containerization
- Kubernetes manifests
- Terraform infrastructure configuration
- GitHub Actions CI pipeline
- Automated test execution on pushes and pull requests
