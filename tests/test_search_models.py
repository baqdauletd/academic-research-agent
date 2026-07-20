from app.search.models import SearchQueries, SortPreference, UserSearchPrompt


def test_user_prompt_has_safe_defaults():
    prompt = UserSearchPrompt(
        raw_prompt="Find papers about LoRa.",
        search_keywords=["LoRa"],
    )

    assert prompt.target_count == 10
    assert prompt.year_from is None
    assert prompt.sources == []
    assert prompt.sort is SortPreference.RELEVANCE


def test_search_queries_references_its_prompt_and_queries():
    prompt = UserSearchPrompt(
        raw_prompt="Find papers about LoRa.",
        search_keywords=["LoRa"],
    )
    queries = SearchQueries(prompt=prompt, textual_queries=["LoRa"])

    assert queries.prompt is prompt
    assert queries.textual_queries == ["LoRa"]
