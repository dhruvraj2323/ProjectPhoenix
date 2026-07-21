"""
Project Phoenix
Milestone M15 - Trading Orchestrator Engine

Module:
    orchestrator_logger.py

Purpose:
    Logs Trading Orchestrator pipeline
    execution.
"""

from __future__ import annotations

from orchestrator.orchestrator_models import (
    TradingDecision,
)


class OrchestratorLogger:
    """
    Logs Trading Orchestrator results.
    """

    def log(
        self,
        decision: TradingDecision,
    ) -> None:
        """
        Log pipeline execution.
        """

        print("===== Trading Pipeline =====")

        for stage in decision.result.stages:

            print(
                f"{stage.name:<12}: "
                f"{'PASS' if stage.completed else 'FAIL'}"
            )

        print()

        print(
            f"Result           : "
            f"{decision.status.value}"
        )

        print(
            f"Approved         : "
            f"{decision.approved}"
        )

        print(
            f"Completed Stages : "
            f"{decision.result.metadata.completed_stages}"
        )

        print(
            f"Execution Time   : "
            f"{decision.result.metadata.execution_time_ms:.2f} ms"
        )

        print(
            f"Reason           : "
            f"{decision.reason}"
        )