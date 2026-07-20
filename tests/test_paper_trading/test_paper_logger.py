"""
=================================================
Project Phoenix
Paper Trading Logger Test
=================================================
"""

from paper_trading.paper_logger import PaperLogger
from paper_trading.paper_models import (
    PaperTradingStatus,
    PaperTradingResult,
)


def run_test():

    status = PaperTradingStatus(
        running=True,
        virtual_balance=10000.0,
        total_positions=2,
    )

    result = PaperTradingResult(
        approved=True,
        reason="Paper trading initialized successfully.",
        status=status,
    )

    PaperLogger.log(result)

    assert result.approved

    print()
    print("Paper Trading Logger Test Passed")


if __name__ == "__main__":

    run_test()