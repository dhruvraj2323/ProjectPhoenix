"""
Project Phoenix
Milestone M10 - Execution Rules Engine

Module:
    execution_rules.py

Purpose:
    Converts a RiskDecision into an OrderRequest.
"""

from __future__ import annotations

from execution.execution_models import (
    OrderRequest,
    OrderSide,
    OrderType,
)
from risk.risk_models import RiskDecision


class ExecutionRules:
    """
    Generates an OrderRequest from a RiskDecision.
    """

    def create_order(self, decision: RiskDecision) -> OrderRequest:
        """
        Create an execution order from an approved risk decision.
        """

        return OrderRequest(
            symbol="XAUUSD",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            volume=decision.position.quantity,
            entry_price=250.0,
            stop_loss=decision.stop_loss.price,
            take_profit=decision.take_profit.price,
            comment="Initial M10 placeholder order.",
        )