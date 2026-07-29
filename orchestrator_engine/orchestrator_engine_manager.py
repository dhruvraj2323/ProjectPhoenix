"""
=================================================
Project Phoenix
Orchestrator Engine Manager
M39
=================================================
"""

from __future__ import annotations

from orchestrator_engine.orchestrator_engine import (
    OrchestratorEngine,
)
from orchestrator_engine.orchestrator_engine_models import (
    OrchestratorResult,
)


class OrchestratorEngineManager:
    """
    Public entry point for the Orchestrator Engine.
    """

    def __init__(self) -> None:

        self.engine = OrchestratorEngine()

    def execute(
        self,
    ) -> OrchestratorResult:
        """
        Execute the complete Project Phoenix pipeline.
        """

        return self.engine.run()