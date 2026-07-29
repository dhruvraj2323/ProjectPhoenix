"""
=================================================
Project Phoenix
Orchestrator Engine Validator
M39
=================================================
"""

from __future__ import annotations

from orchestrator_engine.orchestrator_engine_models import (
    OrchestratorResult,
)


class OrchestratorEngineValidator:
    """
    Validates the Orchestrator Engine before
    pipeline execution.
    """

    def validate(
        self,
        result: OrchestratorResult,
    ) -> bool:
        """
        Validate orchestrator state.
        """

        if result is None:

            return False

        return True