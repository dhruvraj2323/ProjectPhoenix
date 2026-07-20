"""
=================================================
Project Phoenix
Dashboard Controller Test
=================================================
"""

from dashboard.dashboard_controller import DashboardController


def run_test():

    controller = DashboardController()

    account = controller.account()
    positions = controller.positions()
    signals = controller.signals()

    print("===== Dashboard Controller =====")

    print(f"Balance        : {account.balance}")
    print(f"Equity         : {account.equity}")
    print(f"Positions      : {len(positions)}")
    print(f"Signals        : {len(signals)}")

    assert len(positions) == 1
    assert len(signals) == 1

    print()
    print("Dashboard Controller Test Passed")


if __name__ == "__main__":

    run_test()