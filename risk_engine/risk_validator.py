"""
=================================================
Project Phoenix
Risk Validator
M36
=================================================
"""

from __future__ import annotations

from risk_engine.risk_context import RiskContext
from risk_engine.risk_models import RiskDecision


class RiskValidator:
    """
    Validates calculated risk against configured limits.
    """

    MAX_RISK_PERCENT = 2.0

    def validate(
        self,
        context: RiskContext,
    ) -> bool:

        metrics = context.risk_result.metrics

        if metrics.risk_percent > self.MAX_RISK_PERCENT:

            context.fail(
                "Maximum risk exceeded",
            )

            context.risk_result.decision = (
                RiskDecision.REJECTED
            )

            context.risk_result.reason = (
                "Maximum risk exceeded"
            )

            return False

        context.complete()

        context.risk_result.decision = (
            RiskDecision.APPROVED
        )

        context.risk_result.reason = (
            "Risk Accepted"
        )

        return True