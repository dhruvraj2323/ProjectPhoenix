"""
Project Phoenix
Milestone M15 - Trading Orchestrator Engine

Module:
    orchestrator_validator.py

Purpose:
    Validates Trading Orchestrator
    pipeline execution.
"""

from __future__ import annotations

from dataclasses import dataclass

from orchestrator.orchestrator_models import (
    TradingResult,
)


@dataclass
class OrchestratorValidationResult:
    """
    Validation result returned by the
    Trading Orchestrator Validator.
    """

    valid: bool

    reason: str


class OrchestratorValidator:
    """
    Validates pipeline execution.
    """

    def validate(
        self,
        result: TradingResult,
    ) -> OrchestratorValidationResult:
        """
        Validate pipeline result.
        """

        if len(result.stages) == 0:

            return OrchestratorValidationResult(

                valid=False,

                reason="Pipeline contains no stages.",

            )

        for stage in result.stages:

            if not stage.completed:

                return OrchestratorValidationResult(

                    valid=False,

                    reason=f"{stage.name} stage failed.",

                )

        return OrchestratorValidationResult(

            valid=True,

            reason="Pipeline validation passed.",

        )