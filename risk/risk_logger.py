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

    Current implementation prints the
    decision to the console.
    """

    def log(
        self,
        decision: RiskDecision,
    ) -> None:
        """
        Log the supplied risk decision.
        """

        print("===== Risk Decision =====")
        print(f"Decision   : {decision.decision.value}")
        print(f"Approved   : {decision.approved}")
        print(f"Reason     : {decision.reason}")
        print(f"Position   : {decision.position.quantity}")
        print(f"Stop Loss  : {decision.stop_loss.price}")
        print(f"Take Profit: {decision.take_profit.price}")