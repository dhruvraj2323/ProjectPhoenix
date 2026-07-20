"""
=================================================
Project Phoenix
Live Trading Logger
=================================================

Logs live trading operations.
"""

from live_trading.live_models import LiveTradingResult


class LiveLogger:
    """
    Logs live trading events.
    """

    @staticmethod
    def log(result: LiveTradingResult):

        print("===== Live Trading =====")

        print(f"Approved          : {result.approved}")
        print(f"Reason            : {result.reason}")
        print()

        print(f"Running           : {result.status.running}")
        print(f"Account Balance   : {result.status.account_balance}")
        print(f"Open Positions    : {result.status.total_positions}")