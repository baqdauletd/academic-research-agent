from app.tools.query import clean_prompt, generate_queries


def test_clean_prompt_removes_request_words_and_filler_words():
    assert clean_prompt("I want research papers about IoT with LoRa") == "iot lora"


def test_clean_prompt_keeps_technical_tokens():
    assert clean_prompt("IOT 2.4 ghz Lora intersections") == "iot 2.4 ghz lora intersections"


def test_generate_queries_returns_deterministic_variants():
    assert generate_queries("IOT 2.4 ghz Lora intersections") == [
        "iot 2.4 ghz lora intersections",
        "intersections lora ghz 2.4 iot",
        "2.4 ghz lora intersections iot",
    ]


def test_generate_queries_respects_max_queries():
    assert generate_queries("IOT 2.4 ghz Lora intersections", max_queries=1) == [
        "iot 2.4 ghz lora intersections",
    ]


def test_generate_queries_returns_empty_for_noise_only_prompt():
    assert generate_queries("I want research papers about") == []
