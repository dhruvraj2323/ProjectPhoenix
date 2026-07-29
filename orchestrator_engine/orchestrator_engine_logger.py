"""
=================================================
Project Phoenix
Orchestrator Engine Logger
M39
=================================================
"""

from __future__ import annotations

from orchestrator_engine.orchestrator_engine_models import (
    OrchestratorResult,
)


class OrchestratorEngineLogger:
    """
    Logs Orchestrator Engine events.
    """

    def log_start(self) -> None:

        print()

        print("========================================")
        print("Project Phoenix")
        print("Orchestrator Engine Started")
        print("========================================")

    def log_stage(
        self,
        stage_name: str,
    ) -> None:

        print(f"[PIPELINE] {stage_name}")

    def log_result(
        self,
        result: OrchestratorResult,
    ) -> None:

        print()

        print("----------- RESULT -----------")

        print(f"Approved : {result.approved}")

        print(f"Status   : {result.status}")

        print(f"Reason   : {result.reason}")

    def log_finish(self) -> None:

        print()

        print("========================================")
        print("Orchestrator Engine Finished")
        print("========================================")