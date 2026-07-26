"""
Project Phoenix
Milestone M9 - Risk Management Engine

Module:
    risk_logger.py

Purpose:
    Logs risk management decisions.
"""

from __future__ import annotations

from risk.risk_models import RiskDecision


class RiskLogger:
    """
    Logs risk decisions.
    """

    def log(
        self,
        decision: RiskDecision,
    ) -> None:
        """
        Log the supplied risk decision.
        """

        if decision is None:
            raise ValueError("RiskDecision cannot be None.")

        print("===== Risk Decision =====")
        print(f"Decision         : {decision.decision.value}")
        print(f"Approved         : {decision.approved}")
        print(f"Reason           : {decision.reason}")
        print(f"Position Size    : {decision.position.quantity}")
        print(f"Capital          : {decision.position.capital_allocated}")
        print(f"Risk %           : {decision.position.risk_percent}")
        print(f"Stop Loss        : {decision.stop_loss.price}")
        print(f"Take Profit      : {decision.take_profit.price}")
        print(
            f"Risk : Reward    : 1 : "
            f"{decision.take_profit.risk_reward_ratio}"
        )