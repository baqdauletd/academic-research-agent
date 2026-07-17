import re


REMOVAL_PHRASES = (
    "i",
    "me",
    "give",
    "want",
    "please",
    "show",
    "find",
    "research",
    "papers",
    "paper",
    "studies",
    "study",
    "articles",
    "article",
    "about",
)

FILLER_WORDS = {
    "a",
    "an",
    "for",
    "me",
    "of",
    "on",
    "please",
    "the",
    "with",
}


def _normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def clean_prompt(prompt: str) -> str:
    cleaned = prompt.lower().strip()

    for phrase in REMOVAL_PHRASES:
        cleaned = re.sub(rf"\b{re.escape(phrase)}\b", " ", cleaned)

    cleaned = re.sub(r"[^a-z0-9.\-+\s]", " ", cleaned)
    tokens = [token for token in cleaned.split() if token not in FILLER_WORDS]
    return _normalize_whitespace(" ".join(tokens))


def generate_queries(prompt: str, max_queries: int = 3) -> list[str]:
    base_query = clean_prompt(prompt)
    if not base_query:
        return []

    tokens = base_query.split()
    candidates = [base_query]

    if len(tokens) > 1:
        candidates.append(" ".join(tokens[::-1]))

    if len(tokens) > 2:
        candidates.append(" ".join(tokens[1:] + tokens[:1]))

    unique_queries: list[str] = []
    seen: set[str] = set()
    for query in candidates:
        normalized = _normalize_whitespace(query)
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_queries.append(normalized)
        if len(unique_queries) >= max_queries:
            break

    return unique_queries
