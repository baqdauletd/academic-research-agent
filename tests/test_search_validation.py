from datetime import date

import pytest

from app.search.models import UserSearchPrompt
from app.search.validation import SearchValidationError, validate_search_prompt


def make_prompt(**changes: object) -> UserSearchPrompt:
    values: dict[str, object] = {
        "raw_prompt": "Find papers about LoRa.",
        "search_keywords": ["LoRa"],
    }
    values.update(changes)
    return UserSearchPrompt(**values)  # type: ignore[arg-type]


def test_validation_normalizes_text_and_removes_duplicates():
    prompt = make_prompt(
        raw_prompt="  Find   papers about LoRa.  ",
        search_keywords=[" LoRa ", "lora", "IoT"],
        exclusions=[" medical applications ", "Medical Applications"],
    )

    validated = validate_search_prompt(prompt)

    assert validated.raw_prompt == "Find papers about LoRa."
    assert validated.search_keywords == ["LoRa", "IoT"]
    assert validated.exclusions == ["medical applications"]


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"raw_prompt": "   "}, "Prompt must not be empty."),
        ({"search_keywords": ["  "]}, "Search keywords must not be empty."),
        ({"target_count": 0}, "Target count must be between 1 and 50."),
        ({"target_count": 51}, "Target count must be between 1 and 50."),
        ({"year_from": 2025, "year_to": 2024}, "year_from cannot be later than year_to."),
        ({"year_from": 1899}, "year_from must be after 1900"),
        ({"year_to": date.today().year + 1}, "year_to must be between 1900 and next year from today"),
        ({"inclusions": ["LoRa"], "exclusions": ["lora"]}, "A term cannot be both included and excluded."),
    ],
)
def test_validation_rejects_invalid_values(changes: dict[str, object], message: str):
    with pytest.raises(SearchValidationError, match=message):
        validate_search_prompt(make_prompt(**changes))
