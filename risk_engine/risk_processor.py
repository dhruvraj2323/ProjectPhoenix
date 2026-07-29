"""
=================================================
Project Phoenix
Risk Processor
M36
=================================================
"""

from __future__ import annotations

from risk_engine.risk_context import RiskContext
from risk_engine.risk_models import (
    RiskDecision,
)


class RiskProcessor:
    """
    Performs risk calculations.
    """

    def process(
        self,
        context: RiskContext,
    ) -> RiskContext:
        """
        Calculate risk metrics.
        """

        metrics = context.risk_result.metrics

        # ---------------------------------------------
        # Risk %
        # ---------------------------------------------

        if context.balance > 0:

            metrics.risk_percent = (
                (context.balance - context.free_margin)
                / context.balance
            ) * 100.0

        else:

            metrics.risk_percent = 0.0

        # ---------------------------------------------
        # Position Size
        # ---------------------------------------------

        metrics.position_size = 0.10

        # ---------------------------------------------
        # Exposure
        # ---------------------------------------------

        metrics.exposure = (
            context.balance
            - context.free_margin
        )

        # ---------------------------------------------
        # Margin Required
        # ---------------------------------------------

        metrics.margin_required = (
            context.balance * 0.01
        )

        # ---------------------------------------------
        # Drawdown
        # ---------------------------------------------

        if context.balance > 0:

            metrics.drawdown = max(
                0.0,
                (
                    (context.balance - context.equity)
                    / context.balance
                )
                * 100.0,
            )

        else:

            metrics.drawdown = 0.0

        # ---------------------------------------------
        # Final Decision
        # ---------------------------------------------

        context.risk_result.decision = (
            RiskDecision.APPROVED
        )

        context.risk_result.reason = (
            "Risk Calculated"
        )

        return context