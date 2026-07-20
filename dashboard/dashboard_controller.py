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
                symbol="EURUSD",
                direction="BUY",
                volume=0.10,
                entry_price=1.1065,
                current_price=1.1075,
                profit=10.0,
            )
        ]

    def signals(self):

        return [
            DashboardSignal(
                symbol="EURUSD",
                signal="BUY",
                strength=92.5,
                confidence=96.0,
            )
        ]