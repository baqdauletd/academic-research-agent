from app.search.models import (
    PaperType,
    SearchQueries,
    SortPreference,
    SourceName,
    UserSearchPrompt,
)
from datetime import date


def test_user_search_prompt_stores_required_fields():
    prompt = UserSearchPrompt(
        raw_prompt="Give me 10 papers about LoRa after 2021.",
        search_keywords=["LoRa"],
    )

    assert prompt.raw_prompt == "Give me 10 papers about LoRa after 2021."
    assert prompt.search_keywords == ["LoRa"]


def test_user_search_prompt_has_safe_defaults():
    prompt = UserSearchPrompt(
        raw_prompt="Find papers about LoRa.",
        search_keywords=["LoRa"],
    )

    assert prompt.target_count == 5
    assert prompt.year_from is None
    assert prompt.year_to == date.today().year
    assert prompt.paper_types == []
    assert prompt.exclusions == []
    assert prompt.inclusions == []
    assert prompt.sources == []
    assert prompt.venues == []
    assert prompt.authors == []
    assert prompt.sort is SortPreference.RELEVANCE
    assert prompt.language is None


def test_user_search_prompt_stores_all_explicit_values():
    prompt = UserSearchPrompt(
        raw_prompt="Find 5 recent review papers about RAG, excluding medical applications.",
        search_keywords=["RAG", "retrieval-augmented generation"],
        target_count=5,
        year_from=2022,
        year_to=2026,
        paper_types=[PaperType.REVIEW, PaperType.CONFERENCE_PAPER],
        exclusions=["medical applications"],
        inclusions=["citations"],
        sources=[SourceName.OPENALEX, SourceName.ARXIV],
        venues=["NeurIPS"],
        authors=["Jane Doe"],
        sort=SortPreference.NEWEST,
        language="en",
    )

    assert prompt.search_keywords == ["RAG", "retrieval-augmented generation"]
    assert prompt.target_count == 5
    assert prompt.year_from == 2022
    assert prompt.year_to == 2026
    assert prompt.paper_types == [PaperType.REVIEW, PaperType.CONFERENCE_PAPER]
    assert prompt.exclusions == ["medical applications"]
    assert prompt.inclusions == ["citations"]
    assert prompt.sources == [SourceName.OPENALEX, SourceName.ARXIV]
    assert prompt.venues == ["NeurIPS"]
    assert prompt.authors == ["Jane Doe"]
    assert prompt.sort is SortPreference.NEWEST
    assert prompt.language == "en"


def test_user_search_prompt_default_lists_are_independent():
    first = UserSearchPrompt(raw_prompt="Find papers about LoRa.", search_keywords=["LoRa"])
    second = UserSearchPrompt(raw_prompt="Find papers about RAG.", search_keywords=["RAG"])

    first.exclusions.append("medical applications")

    assert first.exclusions == ["medical applications"]
    assert second.exclusions == []


def test_enum_values_are_stable():
    assert PaperType.REVIEW.value == "review"
    assert PaperType.SURVEY.value == "survey"
    assert SourceName.OPENALEX.value == "openalex"
    assert SourceName.SEMANTIC_SCHOLAR.value == "semantic_scholar"
    assert SourceName.ARXIV.value == "arxiv"
    assert SortPreference.RELEVANCE.value == "relevance"
    assert SortPreference.NEWEST.value == "newest"
    assert SortPreference.OLDEST.value == "oldest"
    assert SortPreference.CITED_BY.value == "cited_by"


def test_search_queries_stores_one_query_for_its_prompt():
    prompt = UserSearchPrompt(
        raw_prompt="Find papers about LoRa.",
        search_keywords=["LoRa"],
    )
    queries = SearchQueries(prompt=prompt, textual_queries=["SX1280 ranging"])

    assert queries.prompt is prompt
    assert queries.textual_queries == ["SX1280 ranging"]


def test_search_queries_stores_multiple_queries_in_order():
    prompt = UserSearchPrompt(
        raw_prompt="Find papers about LoRa in indoor localization.",
        search_keywords=["LoRa", "indoor localization"],
    )
    textual_queries = [
        "LoRa indoor localization",
        '"LoRa" "indoor localization"',
        "LoRa localization indoor",
    ]

    queries = SearchQueries(prompt=prompt, textual_queries=textual_queries)

    assert queries.textual_queries == textual_queries


def test_search_queries_can_represent_no_queries_yet():
    prompt = UserSearchPrompt(
        raw_prompt="Find papers about LoRa.",
        search_keywords=["LoRa"],
    )

    queries = SearchQueries(prompt=prompt, textual_queries=[])

    assert queries.textual_queries == []
