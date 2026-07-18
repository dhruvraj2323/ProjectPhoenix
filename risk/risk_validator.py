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

        Current placeholder logic:
        A trade is valid if it has been approved.
        """

        return decision.approved