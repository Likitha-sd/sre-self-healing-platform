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
