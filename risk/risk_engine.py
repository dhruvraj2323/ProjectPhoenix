"""
Project Phoenix
Milestone M9 - Risk Management Engine

Module:
    risk_engine.py

Purpose:
    Coordinates the complete Risk Management Engine workflow.
"""

from __future__ import annotations

from risk.risk_logger import RiskLogger
from risk.risk_models import (
    RiskContext,
    RiskDecision,
    TradeDecision,
)
from risk.risk_position import PositionSizer
from risk.risk_stoploss import StopLossCalculator
from risk.risk_takeprofit import TakeProfitCalculator
from risk.risk_validator import RiskValidator


class RiskEngine:
    """
    Main coordinator for the Risk Management Engine.
    """

    def __init__(self) -> None:
        self.position_sizer = PositionSizer()
        self.stoploss = StopLossCalculator()
        self.takeprofit = TakeProfitCalculator()
        self.validator = RiskValidator()
        self.logger = RiskLogger()

    def evaluate(self, context: RiskContext) -> RiskDecision:
        """
        Execute the complete risk workflow.

        Returns:
            RiskDecision
        """

        if context.account_balance <= 0:
            raise ValueError("Account balance must be greater than zero.")

        if not context.symbol.strip():
            raise ValueError("Symbol cannot be empty.")

        entry_price = context.signal.metadata.get("entry_price")

        if entry_price is None:
            raise ValueError("Entry price missing from signal metadata.")

        position = self.position_sizer.calculate(
            account_balance=context.account_balance,
            risk_percent=1.0,
        )

        stop_loss = self.stoploss.calculate(
            entry_price=entry_price,
            stop_loss_percent=2.0,
        )

        take_profit = self.takeprofit.calculate(
            entry_price=entry_price,
            stop_loss_price=stop_loss.price,
            risk_reward_ratio=2.0,
        )

        decision = RiskDecision(
            decision=TradeDecision.APPROVE,
            position=position,
            stop_loss=stop_loss,
            take_profit=take_profit,
            approved=True,
            reason="Risk evaluation completed successfully.",
        )

        if not self.validator.validate(decision):
            raise ValueError("Risk validation failed.")

        self.logger.log(decision)

        return decision