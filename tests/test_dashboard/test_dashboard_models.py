"""
=================================================
Project Phoenix
Dashboard Models Test
=================================================
"""

from dashboard.dashboard_models import (
    DashboardAccount,
    DashboardPosition,
    DashboardSignal,
    DashboardStatus,
    DashboardResult,
)


def run_test():

    account = DashboardAccount(
        balance=10000.0,
        equity=10050.0,
        floating_profit=50.0,
        closed_profit=250.0,
    )

    position = DashboardPosition(
        symbol="EURUSD",
        direction="BUY",
        volume=0.10,
        entry_price=1.1065,
        current_price=1.1075,
        profit=10.0,
    )

    signal = DashboardSignal(
        symbol="EURUSD",
        signal="BUY",
        strength=92.5,
        confidence=96.0,
    )

    status = DashboardStatus(
        running=True,
        connected=True,
        refresh_rate=5,
    )

    result = DashboardResult(
        approved=True,
        reason="Dashboard initialized successfully.",
        status=status,
    )

    print("===== Dashboard Models =====")

    print(f"Balance        : {account.balance}")
    print(f"Equity         : {account.equity}")
    print(f"Signal         : {signal.signal}")
    print(f"Confidence     : {signal.confidence}")
    print(f"Refresh Rate   : {status.refresh_rate}")

    assert result.approved

    print()
    print("Dashboard Models Test Passed")


if __name__ == "__main__":

    run_test()