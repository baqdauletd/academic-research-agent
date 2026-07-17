from uuid import uuid4

from monitoring.contract import MonitoringEvent
from monitoring.logger import log_event
from tools.query import generate_queries

prompt = input("Enter your prompt: ")
run_id = str(uuid4())

try:
    generated_queries = generate_queries(prompt)
    log_event(
        MonitoringEvent(
            run_id=run_id,
            event_type="query_generation",
            payload={"prompt": prompt, "queries": generated_queries},
        )
    )
    print(generated_queries)
except Exception as e:
    log_event(
        MonitoringEvent(
            run_id=run_id,
            event_type="query_generation",
            payload={"prompt": prompt, "queries": generated_queries},
            err=str(e),
        )
    )
    raise

#starting, query generation, call API, normalization, deduplication, storing in psql, finishing
