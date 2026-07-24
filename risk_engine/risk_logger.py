"""
=================================================
Project Phoenix
Risk Logger
M36
=================================================
"""

from __future__ import annotations

from risk_engine.risk_context import RiskContext


class RiskLogger:
    """
    Logs Risk Engine activity.
    """

    def log_start(
        self,
        context: RiskContext,
    ) -> None:
        """
        Log engine start.
        """

        context.metadata["started"] = True

    def log_finish(
        self,
        context: RiskContext,
    ) -> None:
        """
        Log successful completion.
        """

        context.metadata["completed"] = True

    def log_failure(
        self,
        context: RiskContext,
    ) -> None:
        """
        Log failure.
        """

        context.metadata["failed"] = True

        context.metadata["reason"] = (
            context.reason
        )