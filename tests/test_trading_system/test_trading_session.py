"""
=================================================
Project Phoenix
Trading Session Test
=================================================
"""

from trading_system.trading_session import (
    TradingSession,
)


def test_trading_session():

    session = TradingSession(

        session_id="SESSION-001",

    )

    session.record_success(
        profit=150.0,
    )

    session.record_success(
        profit=75.0,
    )

    session.record_failure(
        loss=50.0,
    )

    session.record_skip()

    assert session.total_trades == 3

    assert session.successful_trades == 2

    assert session.failed_trades == 1

    assert session.skipped_trades == 1

    assert session.gross_profit == 225.0

    assert session.gross_loss == 50.0

    assert session.net_profit == 175.0

    session.close()

    assert session.completed is True

    assert session.active is False

    print()

    print("Trading Session Test Passed")


if __name__ == "__main__":

    test_trading_session()