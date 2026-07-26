"""
Project Phoenix
Milestone M9 - Risk Management Engine

Module:
    risk_validator.py

Purpose:
    Validates whether a calculated risk decision
    satisfies the minimum trading requirements.
"""

from __future__ import annotations

from risk.risk_models import RiskDecision


class RiskValidator:
    """
    Performs validation of risk decisions.
    """

    def validate(
        self,
        decision: RiskDecision,
    ) -> bool:
        """
        Validate the supplied risk decision.

        Returns:
            bool
        """

        if not decision.approved:
            return False

        if decision.position.quantity <= 0:
            return False

        if decision.position.capital_allocated <= 0:
            return False

        if decision.stop_loss.price <= 0:
            return False

        if decision.take_profit.price <= 0:
            return False

        if decision.take_profit.price <= decision.stop_loss.price:
            return False

        return True