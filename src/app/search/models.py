"""Data shared between search intent parsing, planning, and source adapters."""

from dataclasses import dataclass, field
from enum import Enum


class PaperType(str, Enum):
    ARTICLE = "article"
    REVIEW = "review"
    SURVEY = "survey"
    CONFERENCE_PAPER = "conference_paper"
    PREPRINT = "preprint"


class SourceName(str, Enum):
    OPENALEX = "openalex"
    SEMANTIC_SCHOLAR = "semantic_scholar"
    ARXIV = "arxiv"


class SortPreference(str, Enum):
    RELEVANCE = "relevance"
    NEWEST = "newest"
    OLDEST = "oldest"
    CITED_BY = "cited_by"


@dataclass
class UserSearchPrompt:
    raw_prompt: str
    search_keywords: list[str]
    target_count: int = 10
    year_from: int | None = None
    year_to: int | None = None
    paper_types: list[PaperType] = field(default_factory=list)
    exclusions: list[str] = field(default_factory=list)
    inclusions: list[str] = field(default_factory=list)
    sources: list[SourceName] = field(default_factory=list)
    venues: list[str] = field(default_factory=list)
    authors: list[str] = field(default_factory=list)
    sort: SortPreference = SortPreference.RELEVANCE
    language: str | None = None


@dataclass
class SearchQueries:
    prompt: UserSearchPrompt
    textual_queries: list[str]
