from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class EvaluationQuestion(BaseModel):
    """Question item used to evaluate retrieval and generation quality."""

    question: str = Field(..., description="Question to evaluate.")
    expected_answer: str = Field(
        default="",
        description="Reference answer expected for this question.",
    )
    expected_evidence: list[str] = Field(
        default_factory=list,
        description="Evidence snippets expected to appear in retrieved context.",
    )
    source_document: str = Field(
        default="",
        description="Source document name or path for the expected evidence.",
    )
    source_page: int | None = Field(
        default=None,
        description="Source page number when available.",
    )
    source_section: str = Field(
        default="",
        description="Source section or heading when available.",
    )
    difficulty: str = Field(
        default="unknown",
        description="Question difficulty, such as easy, medium, or hard.",
    )
    question_type: str = Field(
        default="unknown",
        description="Question type, such as factual, summary, or reasoning.",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional evaluation metadata.",
    )


class EvaluationDataset(BaseModel):
    """Collection of evaluation questions loaded from a dataset file."""

    name: str = Field(default="untitled", description="Dataset name.")
    description: str = Field(default="", description="Dataset description.")
    questions: list[EvaluationQuestion] = Field(
        default_factory=list,
        description="Questions included in this evaluation dataset.",
    )


def load_evaluation_questions(file_path: str | Path) -> EvaluationDataset:
    """Load evaluation questions from a JSON file.

    Supported JSON shapes:
    - A list of question objects.
    - An object with name, description, and questions fields.
    """
    path = Path(file_path)
    with path.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)

    if isinstance(data, list):
        return EvaluationDataset(
            name=path.stem,
            questions=[EvaluationQuestion(**item) for item in data],
        )

    if isinstance(data, dict):
        questions = data.get("questions", [])
        return EvaluationDataset(
            name=data.get("name", path.stem),
            description=data.get("description", ""),
            questions=[EvaluationQuestion(**item) for item in questions],
        )

    raise ValueError("Evaluation dataset JSON must be a list or an object.")
