import pytest

from app.cli import run_query_generation


# pytestmark = pytest.mark.xfail(reason="target behavior for the next query-generation pass")


@pytest.mark.parametrize(
    ("prompt", "expected"),
    [
        (
            "I want 10 research papers about IoT with 2.4 GHz LoRa.",
            ["iot 2.4 ghz lora", "2.4 ghz lora iot", "lora iot"],
        ),
        (
            "Give me academic work on LoRa 2.4 GHz ranging.",
            ["lora 2.4 ghz ranging", "2.4 ghz lora ranging", "lora ranging"],
        ),
        (
            "I’m researching indoor localization using LoRa; collect relevant papers.",
            ["indoor localization lora", "lora indoor localization", "lora localization"],
        ),
        (
            "Search for studies about LPWAN technologies in IoT systems.",
            ["lpwan technologies iot systems", "lpwan iot", "iot lpwan technologies"],
        ),
        (
            "I need sources on wireless sensor networks for underground mines.",
            [
                "wireless sensor networks underground mines",
                "underground mines wireless sensor networks",
                "wireless sensor networks mines",
            ],
        ),
        (
            "Can you pull papers about IoT-based localization systems?",
            ["iot-based localization systems", "iot localization systems", "localization systems iot"],
        ),
        (
            "Gather academic articles involving ESP32 and LoRa communication.",
            ["esp32 lora communication", "lora communication esp32", "esp32 lora"],
        ),
        (
            "Show me research on LoRa-based asset tracking.",
            ["lora-based asset tracking", "lora asset tracking", "asset tracking lora"],
        ),
        (
            "Retrieve papers that discuss SX1280 ranging.",
            ["sx1280 ranging"],
        ),
        (
            "Compile studies about drone communication using LoRa.",
            ["drone communication lora", "lora drone communication", "drone lora communication"],
        ),
    ],
)
def test_simple_topic_prompts_generate_target_queries(prompt, expected):
    assert run_query_generation(prompt) == expected
