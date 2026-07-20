"""
=================================================
Project Phoenix
Live Trading Logger Test
=================================================
"""

from live_trading.live_logger import LiveLogger
from live_trading.live_models import (
    LiveTradingStatus,
    LiveTradingResult,
)


def run_test():

    status = LiveTradingStatus(
        running=True,
        account_balance=10000.0,
        total_positions=2,
    )

    result = LiveTradingResult(
        approved=True,
        reason="Live trading initialized successfully.",
        status=status,
    )

    LiveLogger.log(result)

    assert result.approved

    print()
    print("Live Trading Logger Test Passed")


if __name__ == "__main__":

    run_test()