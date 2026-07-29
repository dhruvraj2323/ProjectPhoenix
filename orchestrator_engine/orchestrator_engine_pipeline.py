"""
=================================================
Project Phoenix
Orchestrator Engine Pipeline
M39
=================================================
"""

from __future__ import annotations

from orchestrator_engine.orchestrator_engine_models import (
    PipelineStage,
)


class OrchestratorEnginePipeline:
    """
    Defines the execution pipeline
    of Project Phoenix.
    """

    def __init__(self) -> None:

        self._stages = [

            PipelineStage("Market Data"),

            PipelineStage("Signal Engine"),

            PipelineStage("Strategy Engine"),

            PipelineStage("Risk Engine"),

            PipelineStage("Execution Engine"),

            PipelineStage("Paper Trading"),

            PipelineStage("Portfolio Engine"),

            PipelineStage("Performance Engine"),

        ]

    def stages(
        self,
    ) -> list[PipelineStage]:
        """
        Return pipeline stages.
        """

        return self._stages

    def total_stages(
        self,
    ) -> int:
        """
        Total pipeline stages.
        """

        return len(self._stages)