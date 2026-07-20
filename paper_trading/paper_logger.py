"""
=================================================
Project Phoenix
Paper Trading Logger
=================================================

Logs paper trading operations.
"""

from paper_trading.paper_models import PaperTradingResult


class PaperLogger:
    """
    Logs paper trading events.
    """

    @staticmethod
    def log(result: PaperTradingResult):

        print("===== Paper Trading =====")

        print(f"Approved          : {result.approved}")
        print(f"Reason            : {result.reason}")
        print()

        print(f"Running           : {result.status.running}")
        print(f"Virtual Balance   : {result.status.virtual_balance}")
        print(f"Open Positions    : {result.status.total_positions}")