"""
Project Phoenix
Milestone M15 - Trading Orchestrator Engine

Module:
    orchestrator_engine.py

Purpose:
    Coordinates the complete Trading
    Orchestrator workflow.
"""

from __future__ import annotations

from orchestrator.orchestrator_logger import (
    OrchestratorLogger,
)
from orchestrator.orchestrator_models import (
    OrchestratorStatus,
    TradingDecision,
)
from orchestrator.orchestrator_pipeline import (
    OrchestratorPipeline,
)
from orchestrator.orchestrator_validator import (
    OrchestratorValidator,
)


class OrchestratorEngine:
    """
    Coordinates the complete
    Trading Orchestrator Engine.
    """

    def __init__(self) -> None:

        self.pipeline = OrchestratorPipeline()

        self.validator = OrchestratorValidator()

        self.logger = OrchestratorLogger()

    def execute(
        self,
    ) -> TradingDecision:
        """
        Execute complete workflow.
        """

        result = self.pipeline.execute()

        validation = self.validator.validate(
            result
        )

        decision = TradingDecision(

            status=(

                OrchestratorStatus.APPROVED

                if validation.valid

                else

                OrchestratorStatus.REJECTED

            ),

            approved=validation.valid,

            result=result,

            reason=validation.reason,

        )

        self.logger.log(
            decision
        )

        return decision