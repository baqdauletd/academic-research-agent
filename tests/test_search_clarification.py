import pytest

from app.search.clarification import ClarificationReason, get_clarification
from app.search.models import UserSearchPrompt


def make_prompt(**changes: object) -> UserSearchPrompt:
    values: dict[str, object] = {
        "raw_prompt": "Find papers about LoRa.",
        "search_keywords": ["LoRa"],
    }
    values.update(changes)
    return UserSearchPrompt(**values)  # type: ignore[arg-type]


def test_missing_topic_requests_clarification():
    clarification = get_clarification(
        make_prompt(raw_prompt="Find papers for me.", search_keywords=[])
    )

    assert clarification is not None
    assert clarification.reason is ClarificationReason.MISSING_TOPIC
    assert clarification.question == (
        "Can you give more details about the research topic you want to search for?"
    )


@pytest.mark.parametrize("keywords", [["   "], [" ", "   "]])
def test_blank_only_topics_request_clarification(keywords: list[str]):
    clarification = get_clarification(make_prompt(search_keywords=keywords))

    assert clarification is not None
    assert clarification.reason is ClarificationReason.MISSING_TOPIC


def test_usable_topic_among_blank_items_does_not_require_clarification():
    clarification = get_clarification(make_prompt(search_keywords=[" ", "LoRa"]))

    assert clarification is None


def test_conflicting_year_range_requests_clarification():
    clarification = get_clarification(make_prompt(year_from=2025, year_to=2024))

    assert clarification is not None
    assert clarification.reason is ClarificationReason.CONFLICTING_YEAR_RANGE
    assert clarification.question == (
        "Your date range ends before it begins. Which publication years do you want?"
    )


def test_same_start_and_end_year_does_not_require_clarification():
    clarification = get_clarification(make_prompt(year_from=2024, year_to=2024))

    assert clarification is None


def test_missing_topic_has_priority_over_conflicting_years():
    clarification = get_clarification(
        make_prompt(search_keywords=[], year_from=2025, year_to=2024)
    )

    assert clarification is not None
    assert clarification.reason is ClarificationReason.MISSING_TOPIC


def test_broad_but_valid_topic_uses_defaults_without_clarification():
    clarification = get_clarification(
        make_prompt(
            raw_prompt="I am interested in LoRa research; show relevant academic sources.",
            search_keywords=["LoRa"],
        )
    )

    assert clarification is None


def test_valid_multilingual_topic_does_not_require_clarification():
    clarification = get_clarification(
        make_prompt(
            raw_prompt="Найди 10 научных статей про LoRa 2.4 GHz для IoT.",
            search_keywords=["LoRa", "2.4 GHz", "IoT"],
        )
    )

    assert clarification is None


def test_request_with_default_count_source_and_paper_type_does_not_require_clarification():
    clarification = get_clarification(make_prompt(search_keywords=["LoRa"]))

    assert clarification is None
