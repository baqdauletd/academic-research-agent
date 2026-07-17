from uuid import uuid4

from monitoring.logger import log_query_generation
from tools.query import generate_queries

prompt = input("Enter your prompt: ")
run_id = str(uuid4())
generated_queries: list[str] = []

try:
    generated_queries = generate_queries(prompt)
    log_query_generation(run_id, prompt, generated_queries)
except Exception as e:
    log_query_generation(run_id, prompt, generated_queries, err=str(e))
    raise

#starting, query generation, call API, normalization, deduplication, storing in psql, finishing
