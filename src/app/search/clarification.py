"""Rules for deciding when a search prompt needs a user follow-up."""

from dataclasses import dataclass
from enum import Enum

from app.search.models import UserSearchPrompt


class ClarificationReason(str, Enum):
    MISSING_TOPIC = "missing_topic"
    CONFLICTING_YEAR_RANGE = "conflicting_year_range"


@dataclass(frozen=True)
class Clarification:
    reason: ClarificationReason
    question: str


def get_clarification(prompt: UserSearchPrompt) -> Clarification | None:
    """Return a follow-up only when search intent cannot be safely inferred."""

    if not any(keyword.strip() for keyword in prompt.search_keywords):
        return Clarification(
            reason=ClarificationReason.MISSING_TOPIC,
            question="Can you give more details about the research topic you want to search for?",
        )

    if prompt.year_from is not None and prompt.year_to is not None:
        if prompt.year_from > prompt.year_to:
            return Clarification(
                reason=ClarificationReason.CONFLICTING_YEAR_RANGE,
                question="Your date range ends before it begins. Which publication years do you want?",
            )

    return None
