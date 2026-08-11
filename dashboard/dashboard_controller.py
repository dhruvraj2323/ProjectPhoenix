"""
=================================================
Project Phoenix
Dashboard Controller
=================================================

Collects dashboard information from the system.
"""

from dashboard.dashboard_models import (
    DashboardAccount,
    DashboardPosition,
    DashboardSignal,
)


class DashboardController:
    """
    Collects dashboard data.
    """

    def account(self):

        return DashboardAccount(
            balance=10000.0,
            equity=10050.0,
            floating_profit=50.0,
            closed_profit=250.0,
        )

    def positions(self):

        return [
            DashboardPosition(
                symbol="XAUUSDm",
                direction="BUY",
                volume=0.10,
                entry_price=3350.0,
                current_price=3355.0,
                profit=50.0,
            ),
            DashboardPosition(
                symbol="BTCUSDm",
                direction="BUY",
                volume=0.01,
                entry_price=115000.0,
                current_price=115500.0,
                profit=5.0,
            ),
        ]

    def signals(self):

        return [
            DashboardSignal(
                symbol="XAUUSDm",
                signal="BUY",
                strength=92.5,
                confidence=96.0,
            ),
            DashboardSignal(
                symbol="BTCUSDm",
                signal="BUY",
                strength=88.0,
                confidence=91.0,
            ),
        ]