"""
=================================================
Project Phoenix
Orchestrator Engine Validator
M56
=================================================
"""

from __future__ import annotations

from orchestrator_engine.orchestrator_engine_models import (
    OrchestratorResult,
)


class OrchestratorEngineValidator:
    """
    Validates Orchestrator Engine
    before pipeline execution.
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

        if result.approved:

            # Fresh execution should never
            # start with an approved result.
            return False

        if result.status != "PENDING":

            return False

        return True