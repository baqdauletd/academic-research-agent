from dataclasses import replace
from datetime import date

from app.search.models import UserSearchPrompt


DEFAULT_TARGET_COUNT = 10
MIN_TARGET_COUNT = 1
MAX_TARGET_COUNT = 50
MIN_PUBLICATION_YEAR = 1900


class SearchValidationError(ValueError):
    """Raised when a parsed search prompt cannot be searched safely."""


def _normalize_text_items(items: list[str]) -> list[str]:
    normalized_items: list[str] = []
    seen: set[str] = set()

    for item in items:
        normalized = " ".join(item.split())
        deduplication_key = normalized.casefold()
        if normalized and deduplication_key not in seen:
            seen.add(deduplication_key)
            normalized_items.append(normalized)

    return normalized_items


def _validate_year(year: int | None, field_name: str) -> None:
    if year is None:
        return

    if isinstance(year, bool) or not isinstance(year, int):
        raise SearchValidationError(f"{field_name} must be a whole year.")

    if not MIN_PUBLICATION_YEAR <= year <= date.today().year:
        raise SearchValidationError(
            f"{field_name} must be between {MIN_PUBLICATION_YEAR} and {date.today().year}."
        )


def validate_search_prompt(prompt: UserSearchPrompt) -> UserSearchPrompt:
    """Return a normalized prompt or raise SearchValidationError."""

    raw_prompt = " ".join(prompt.raw_prompt.split())
    keywords = _normalize_text_items(prompt.search_keywords)

    if not raw_prompt:
        raise SearchValidationError("Prompt must not be empty.")
    if not keywords:
        raise SearchValidationError("Search topic must not be empty.")
    if isinstance(prompt.target_count, bool) or not isinstance(prompt.target_count, int):
        raise SearchValidationError("Target count must be a whole number.")
    if not MIN_TARGET_COUNT <= prompt.target_count <= MAX_TARGET_COUNT:
        raise SearchValidationError(
            f"Target count must be between {MIN_TARGET_COUNT} and {MAX_TARGET_COUNT}."
        )

    _validate_year(prompt.year_from, "year_from")
    _validate_year(prompt.year_to, "year_to")
    if prompt.year_from is not None and prompt.year_to is not None:
        if prompt.year_from > prompt.year_to:
            raise SearchValidationError("year_from cannot be later than year_to.")

    inclusions = _normalize_text_items(prompt.inclusions)
    exclusions = _normalize_text_items(prompt.exclusions)
    overlapping_terms = {term.casefold() for term in inclusions} & {
        term.casefold() for term in exclusions
    }
    if overlapping_terms:
        raise SearchValidationError("A term cannot be both included and excluded.")

    return replace(
        prompt,
        raw_prompt=raw_prompt,
        search_keywords=keywords,
        inclusions=inclusions,
        exclusions=exclusions,
        venues=_normalize_text_items(prompt.venues),
        authors=_normalize_text_items(prompt.authors),
    )
