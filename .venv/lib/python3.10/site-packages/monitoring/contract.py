from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

# datatypes, event shapes, allowed event names
# for - starting/finishing, query generation, call API, normalization, deduplication, storing in psql

EventType = Literal["starting", "finishing", "query_generation", "call_api", "normalization", "deduplication", "storing_in_psql"]

@dataclass
class MonitoringEvent:
    run_id: str
    event_type: EventType
    payload: dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    err: str | None = None