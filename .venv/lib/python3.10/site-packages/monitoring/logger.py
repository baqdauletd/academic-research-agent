import json

from monitoring.contract import EventType, MonitoringEvent

def log_event(event: MonitoringEvent) -> None:
    print(
        json.dumps(
            {
                "run_id": event.run_id,
                "event_type": event.event_type,
                "timestamp": event.timestamp,
                "payload": event.payload,
                "error": event.err,
            }
        )
    )


def log_query_generation(run_id: str, prompt: str, generated_queries: list[str], err: str | None = None) -> None:
    log_event(
        MonitoringEvent(
            run_id=run_id,
            event_type="query_generation",
            payload={
                "prompt": prompt,
                "queries": generated_queries,
            },
            err=err,
        )
    )