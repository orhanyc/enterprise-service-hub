from uuid import UUID

from .models import ServiceRequest, ServiceRequestCreate


class RequestStore:
    def __init__(self) -> None:
        self.requests: dict[UUID, ServiceRequest] = {}
        self.idempotency: dict[str, UUID] = {}

    def create(self, payload: ServiceRequestCreate, key: str) -> ServiceRequest:
        if key in self.idempotency:
            return self.requests[self.idempotency[key]]
        item = ServiceRequest(**payload.model_dump())
        self.requests[item.id] = item
        self.idempotency[key] = item.id
        return item

    def list(self, region: str | None = None) -> list[ServiceRequest]:
        items = list(self.requests.values())
        return [item for item in items if not region or item.region == region]

    def get(self, request_id: UUID) -> ServiceRequest | None:
        return self.requests.get(request_id)

