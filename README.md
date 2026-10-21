# Enterprise Service Hub

Enterprise Service Hub is a compact backend for managing internal service requests across regions. It demonstrates typed APIs, idempotent writes, workflow state, audit events, filtering and operational metrics.

## Architecture

```mermaid
flowchart LR
    C[Web or mobile client] --> A[FastAPI service]
    A --> I[Idempotency guard]
    I --> S[Request store]
    S --> W[Status workflow]
    W --> M[Metrics and audit events]
```

## Features

- Create and track regional service requests
- Prevent duplicate writes with idempotency keys
- Validate payloads with typed schemas
- Record workflow changes in an audit trail
- Filter requests by region
- Expose health and service metrics endpoints

## API example

```bash
curl -X POST http://localhost:8000/requests \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: request-1001" \
  -d '{"title":"Checkout alert","description":"Elevated failures","service":"payments","priority":"critical"}'
```

## Local setup

```bash
pip install -e .
uvicorn service_hub.api:app --reload
```

Interactive API documentation is available at `/docs`.

## Cloud deployment

`cloud/app.yaml` provides a small Google App Engine configuration. The API can also run on Cloud Run, AWS App Runner or another Python application service. Replace the in-memory store with a managed SQL database for persistent deployments.

## Scope

This is an independently designed portfolio demonstration using generated examples. It does not represent any Apple system or private architecture.

## License

MIT
