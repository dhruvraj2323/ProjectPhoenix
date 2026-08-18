"""
=================================================
Project Phoenix
Pre-Trade Governance
M63.2
=================================================
"""

from __future__ import annotations

from live_execution.account_info import (
    AccountInfo,
)

from live_execution.pre_trade_safety_manager import (
    PreTradeSafetyManager,
)

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_validator import (
    TradeValidator,
)

from live_execution.trading_authorization import (
    TradingAuthorization,
)


class PreTradeGovernance:
    """
    Final pre-trade governance boundary.

    Existing M59 safety components are reused.

    Governance chain:

        Trading Authorization
                ↓
        Pre-Trade Safety
                ↓
        Account Validation
                ↓
        Trade Validation
                ↓
        Execution Allowed
    """

    def __init__(
        self,
        trading_authorization=None,
        safety_manager=None,
        account_info=None,
        trade_validator=None,
    ) -> None:

        self.trading_authorization = (
            trading_authorization
            if trading_authorization is not None
            else TradingAuthorization()
        )

        self.safety_manager = (
            safety_manager
            if safety_manager is not None
            else PreTradeSafetyManager()
        )

        self.account_info = (
            account_info
            if account_info is not None
            else AccountInfo()
        )

        self.trade_validator = (
            trade_validator
            if trade_validator is not None
            else TradeValidator()
        )

    def validate(
        self,
        context: TradeContext,
        volume: float,
        price: float,
        stop_loss: float,
        take_profit: float,
    ) -> bool:
        """
        Execute the complete pre-trade governance chain.

        Returns True only when every required
        governance boundary passes.
        """

        # --------------------------------------------------
        # Gate 1 - Trading Authorization
        # --------------------------------------------------

        if not self.trading_authorization.authorize():

            return False

        # --------------------------------------------------
        # Gate 2 - Existing M59 Pre-Trade Safety
        # --------------------------------------------------

        try:

            safety_result = self.safety_manager.validate(
                context.symbol,
                volume,
                price,
                stop_loss,
                take_profit,
            )

        except Exception:

            return False

        if safety_result is not True:

            return False

        # --------------------------------------------------
        # Gate 3 - Account Availability
        # --------------------------------------------------

        try:

            account = self.account_info.get()

        except Exception:

            return False

        if account is None:

            return False

        # --------------------------------------------------
        # Gate 4 - Account State
        # --------------------------------------------------

        try:

            if self.account_info.balance() <= 0:

                return False

            if self.account_info.equity() <= 0:

                return False

            if self.account_info.free_margin() <= 0:

                return False

        except Exception:

            return False

        # --------------------------------------------------
        # Gate 5 - Trade Context Validation
        # --------------------------------------------------

        try:

            trade_result = self.trade_validator.validate(
                context
            )

        except Exception:

            return False

        if trade_result is not True:

            return False

        # --------------------------------------------------
        # Final Governance Approval
        # --------------------------------------------------

        return True