from uuid import UUID

from fastapi import FastAPI, Header, HTTPException

from .models import ServiceRequest, ServiceRequestCreate, StatusUpdate
from .store import RequestStore


app = FastAPI(title="Enterprise Service Hub", version="0.1.0")
store = RequestStore()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/requests", response_model=ServiceRequest, status_code=201)
def create_request(
    payload: ServiceRequestCreate,
    idempotency_key: str = Header(alias="Idempotency-Key"),
) -> ServiceRequest:
    return store.create(payload, idempotency_key)


@app.get("/requests", response_model=list[ServiceRequest])
def list_requests(region: str | None = None) -> list[ServiceRequest]:
    return store.list(region)


@app.patch("/requests/{request_id}", response_model=ServiceRequest)
def update_request(request_id: UUID, payload: StatusUpdate) -> ServiceRequest:
    item = store.get(request_id)
    if not item:
        raise HTTPException(status_code=404, detail="Request not found")
    item.status = payload.status
    item.audit.append(f"status.changed:{payload.status}")
    return item


@app.get("/metrics")
def metrics() -> dict[str, int]:
    items = store.list()
    return {
        "total_requests": len(items),
        "critical_open": sum(
            item.priority == "critical" and item.status != "resolved" for item in items
        ),
        "resolved": sum(item.status == "resolved" for item in items),
    }

