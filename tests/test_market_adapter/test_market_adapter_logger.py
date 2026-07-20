"""
=================================================
Project Phoenix
Market Adapter Logger Test
=================================================
"""

from market_adapter.market_adapter_logger import MarketAdapterLogger
from market_adapter.market_adapter_models import (
    MarketStatus,
    MarketDataResult,
)


def run_test():

    status = MarketStatus(
        connected=True,
        market_open=True,
        provider_name="MT5",
    )

    result = MarketDataResult(
        approved=True,
        reason="Market adapter initialized successfully.",
        status=status,
    )

    MarketAdapterLogger.log(result)

    assert result.approved

    print()
    print("Market Adapter Logger Test Passed")


if __name__ == "__main__":
    run_test()