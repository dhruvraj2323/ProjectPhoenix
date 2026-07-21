"""
=================================================
Project Phoenix
Market Pipeline Router
M31
=================================================
"""

from __future__ import annotations

from typing import Dict, Optional

from .pipeline_models import PipelineStage


class PipelineRouter:
    """
    Defines the execution order of the
    Project Phoenix Market Pipeline.
    """

    def __init__(self) -> None:

        self._routes: Dict[PipelineStage, PipelineStage] = {

            PipelineStage.INITIALIZED: PipelineStage.MARKET_DATA,

            PipelineStage.MARKET_DATA: PipelineStage.INDICATORS,

            PipelineStage.INDICATORS: PipelineStage.PATTERNS,

            PipelineStage.PATTERNS: PipelineStage.SIGNAL,

            PipelineStage.SIGNAL: PipelineStage.RISK,

            PipelineStage.RISK: PipelineStage.PORTFOLIO,

            PipelineStage.PORTFOLIO: PipelineStage.AI,

            PipelineStage.AI: PipelineStage.EXECUTION,

            PipelineStage.EXECUTION: PipelineStage.COMPLETED,

        }

    # ---------------------------------------------------------

    def get_next_stage(
        self,
        current_stage: PipelineStage,
    ) -> Optional[PipelineStage]:
        """
        Return the next pipeline stage.
        """

        return self._routes.get(current_stage)

    # ---------------------------------------------------------

    def has_next_stage(
        self,
        current_stage: PipelineStage,
    ) -> bool:
        """
        Check whether a next stage exists.
        """

        return current_stage in self._routes

    # ---------------------------------------------------------

    def is_final_stage(
        self,
        current_stage: PipelineStage,
    ) -> bool:
        """
        True if pipeline reached COMPLETED stage.
        """

        return current_stage == PipelineStage.COMPLETED

    # ---------------------------------------------------------

    def reset(self) -> PipelineStage:
        """
        Reset pipeline to initial stage.
        """

        return PipelineStage.INITIALIZED

    # ---------------------------------------------------------

    @property
    def routes(self) -> Dict[PipelineStage, PipelineStage]:
        """
        Return pipeline routing table.
        """

        return self._routes.copy()