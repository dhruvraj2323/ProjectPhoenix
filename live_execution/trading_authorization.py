"""
=================================================
Project Phoenix
Trading Authorization
M63.1 - Demo Trading Authorization Boundary
=================================================
"""

from __future__ import annotations

from enum import Enum

from deployment.trading_protection import (
    TradingProtection,
)

from live_execution.demo_account_guard import (
    DemoAccountGuard,
)


class TradingAuthorizationState(Enum):
    """
    Final trading authorization state.
    """

    AUTHORIZED = "AUTHORIZED"
    BLOCKED = "BLOCKED"


class TradingAuthorization:
    """
    Final permission boundary before trading execution.

    Trading is authorized only when:

        TradingProtection is ACTIVE
        AND
        DemoAccountGuard validates the account.

    This component does not execute trades.
    """

    def __init__(
        self,
        protection: TradingProtection | None = None,
        demo_guard: DemoAccountGuard | None = None,
    ) -> None:

        self.protection = (
            protection
            if protection is not None
            else TradingProtection()
        )

        self.demo_guard = (
            demo_guard
            if demo_guard is not None
            else DemoAccountGuard()
        )

        self.state = (
            TradingAuthorizationState.BLOCKED
        )

    # --------------------------------------------------
    # Authorization
    # --------------------------------------------------

    def authorize(self) -> bool:
        """
        Evaluate the final trading authorization boundary.

        Returns:
            True  -> trading authorized
            False -> trading blocked

        Any failed demo-account validation results
        in trading being blocked.
        """

        # ----------------------------------------------
        # Protection Boundary
        # ----------------------------------------------

        if not self.protection.can_trade():

            self.state = (
                TradingAuthorizationState.BLOCKED
            )

            return False

        # ----------------------------------------------
        # Demo Account Boundary
        # ----------------------------------------------

        try:

            self.demo_guard.validate()

        except Exception:

            self.state = (
                TradingAuthorizationState.BLOCKED
            )

            return False

        # ----------------------------------------------
        # Final Authorization
        # ----------------------------------------------

        self.state = (
            TradingAuthorizationState.AUTHORIZED
        )

        return True

    # --------------------------------------------------
    # Permission
    # --------------------------------------------------

    def can_trade(self) -> bool:
        """
        Return True only when the final authorization
        state allows trading.
        """

        return (
            self.state
            == TradingAuthorizationState.AUTHORIZED
        )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def is_blocked(self) -> bool:
        """
        Return True when trading is blocked.
        """

        return (
            self.state
            == TradingAuthorizationState.BLOCKED
        )