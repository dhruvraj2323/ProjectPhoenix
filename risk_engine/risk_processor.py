"""
=================================================
Project Phoenix
Risk Processor
M36
=================================================
"""

from __future__ import annotations

from risk_engine.risk_context import RiskContext
from risk_engine.risk_models import RiskDecision


class RiskProcessor:
    """
    Performs basic risk calculations.
    """

    def process(
        self,
        context: RiskContext,
    ) -> RiskContext:

        metrics = context.risk_result.metrics

        if context.balance > 0:

            metrics.risk_percent = (
                (context.balance - context.free_margin)
                / context.balance
            ) * 100.0

        metrics.position_size = 0.10

        metrics.exposure = (
            context.balance
            - context.free_margin
        )

        metrics.margin_required = (
            context.balance * 0.01
        )

        metrics.drawdown = max(
            0.0,
            (
                (context.balance - context.equity)
                / context.balance
            )
            * 100.0,
        )

        context.risk_result.decision = (
            RiskDecision.APPROVED
        )

        context.risk_result.reason = (
            "Risk Calculated"
        )

        return context