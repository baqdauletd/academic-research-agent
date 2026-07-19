from uuid import uuid4

from monitoring.research import log_query_generation
from app.tools.query import generate_queries


def run_query_generation(prompt: str, run_id: str | None = None) -> list[str]:
    run_id = run_id or str(uuid4())
    generated_queries: list[str] = []
    print(prompt)

    try:
        generated_queries = generate_queries(prompt)
        log_query_generation(run_id, prompt, generated_queries)
        return generated_queries
    except Exception as e:
        log_query_generation(run_id, prompt, generated_queries, error=str(e))
        raise


def main() -> None:
    prompt = input("Enter your prompt: ")
    generated_queries = run_query_generation(prompt)
    print(generated_queries)


if __name__ == "__main__":
    main()

#starting, query generation, call API, normalization, deduplication, storing in psql, finishing
