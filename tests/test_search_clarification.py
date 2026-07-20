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
    assert clarification.question == "Which research topic should I search for?"


def test_conflicting_year_range_requests_clarification():
    clarification = get_clarification(make_prompt(year_from=2025, year_to=2024))

    assert clarification is not None
    assert clarification.reason is ClarificationReason.CONFLICTING_YEAR_RANGE


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
