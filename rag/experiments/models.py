from __future__ import annotations

from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class StageResult(BaseModel):
    """Common result shape for one RAG stage execution."""

    stage_name: str = Field(..., description="RAG stage name, such as chunking.")
    strategy_name: str = Field(..., description="Strategy used for this stage.")
    input_summary: str = Field(default="", description="Short summary of stage input.")
    output_summary: str = Field(default="", description="Short summary of stage output.")
    artifacts: dict[str, Any] = Field(
        default_factory=dict,
        description="Stage outputs or samples used for inspection.",
    )
    metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Quantitative values produced by the stage.",
    )
    observations: list[str] = Field(
        default_factory=list,
        description="Human-readable observations from the stage result.",
    )
    explanation: str = Field(
        default="",
        description="Learning-oriented explanation of the result.",
    )


class ExperimentConfig(BaseModel):
    """Configuration snapshot for a RAG experiment run."""

    experiment_name: str = Field(
        default="untitled",
        description="Human-readable experiment name.",
    )
    description: str = Field(default="", description="Purpose of this experiment.")
    document_path: str | None = Field(
        default=None,
        description="Primary document path used by the experiment.",
    )
    stage_configs: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Per-stage strategy settings.",
    )


class ExperimentResult(BaseModel):
    """Complete result shape for one experiment run."""

    experiment_id: str = Field(
        default_factory=lambda: uuid4().hex,
        description="Unique identifier for this experiment result.",
    )
    config: ExperimentConfig = Field(
        default_factory=ExperimentConfig,
        description="Configuration used for this experiment.",
    )
    stage_results: list[StageResult] = Field(
        default_factory=list,
        description="Ordered results from each executed stage.",
    )
    final_metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Experiment-level metrics.",
    )
    recommendation: str = Field(
        default="",
        description="Final recommendation derived from the experiment.",
    )
