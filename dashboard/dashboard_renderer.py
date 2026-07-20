"""
=================================================
Project Phoenix
Dashboard Renderer
=================================================

Renders dashboard information.
"""

from dashboard.dashboard_controller import DashboardController


class DashboardRenderer:
    """
    Renders dashboard output.
    """

    def __init__(self):

        self.controller = DashboardController()

    def render(self):

        account = self.controller.account()
        positions = self.controller.positions()
        signals = self.controller.signals()

        print("===== Project Phoenix Dashboard =====")
        print()

        print(f"Balance        : {account.balance}")
        print(f"Equity         : {account.equity}")
        print(f"Floating P/L   : {account.floating_profit}")
        print(f"Closed P/L     : {account.closed_profit}")
        print()

        print(f"Open Positions : {len(positions)}")
        print(f"Signals        : {len(signals)}")

        return True