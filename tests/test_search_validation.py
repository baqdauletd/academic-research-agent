from datetime import date

import pytest

from app.search.models import PaperType, SortPreference, SourceName, UserSearchPrompt
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
        inclusions=[" citations ", "CITATIONS"],
        exclusions=[" medical applications ", "Medical Applications"],
        venues=[" NeurIPS ", "neurips"],
        authors=[" Jane Doe ", "jane doe"],
        language=" EN ",
    )

    validated = validate_search_prompt(prompt)

    assert validated.raw_prompt == "Find papers about LoRa."
    assert validated.search_keywords == ["LoRa", "IoT"]
    assert validated.inclusions == ["citations"]
    assert validated.exclusions == ["medical applications"]
    assert validated.venues == ["NeurIPS"]
    assert validated.authors == ["Jane Doe"]
    assert validated.language == "en"


def test_validation_preserves_valid_constraints_and_returns_a_new_prompt():
    prompt = make_prompt(
        target_count=50,
        year_from=1900,
        year_to=date.today().year,
        paper_types=[PaperType.REVIEW],
        sources=[SourceName.OPENALEX, SourceName.ARXIV],
        sort=SortPreference.NEWEST,
    )

    validated = validate_search_prompt(prompt)

    assert validated is not prompt
    assert validated.target_count == 50
    assert validated.year_from == 1900
    assert validated.year_to == date.today().year
    assert validated.paper_types == [PaperType.REVIEW]
    assert validated.sources == [SourceName.OPENALEX, SourceName.ARXIV]
    assert validated.sort is SortPreference.NEWEST


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"raw_prompt": "   "}, "Prompt must not be empty."),
        ({"raw_prompt": None}, "Prompt must be text."),
        ({"search_keywords": []}, "Search topic must not be empty."),
        ({"search_keywords": ["  "]}, "Search topic must not be empty."),
        ({"search_keywords": "LoRa"}, "search_keywords must be a list of string values."),
        ({"search_keywords": ["LoRa", 123]}, "search_keywords must contain only string values."),
        ({"target_count": 0}, "Target count must be between 1 and 50."),
        ({"target_count": 51}, "Target count must be between 1 and 50."),
        ({"target_count": "five"}, "Target count must be a whole number."),
        ({"target_count": 5.5}, "Target count must be a whole number."),
        ({"target_count": True}, "Target count must be a whole number."),
        ({"year_from": 2025, "year_to": 2024}, "year_from cannot be later than year_to."),
        ({"year_from": 1899}, "year_from must be between 1900 and"),
        ({"year_from": "2021"}, "year_from must be a whole year."),
        ({"year_from": True}, "year_from must be a whole year."),
        ({"year_to": date.today().year + 1}, "year_to must be between 1900 and"),
        ({"inclusions": ["LoRa"], "exclusions": ["lora"]}, "A term cannot be both included and excluded."),
        ({"inclusions": ["LoRa", None]}, "inclusions must contain only text values."),
        ({"paper_types": ["thesis"]}, "paper_types contains an unsupported value."),
        ({"sources": ["google_scholar"]}, "sources contains an unsupported value."),
        ({"sort": "best"}, "sort is unsupported."),
        ({"language": "english"}, "language must be a two-letter code."),
        ({"language": 123}, "language must be a two-letter code."),
    ],
)
def test_validation_rejects_invalid_values(changes: dict[str, object], message: str):
    with pytest.raises(SearchValidationError, match=message):
        validate_search_prompt(make_prompt(**changes))
