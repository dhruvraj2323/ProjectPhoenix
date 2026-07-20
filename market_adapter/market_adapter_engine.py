"""
=================================================
Project Phoenix
Market Adapter Engine
=================================================

Master controller of Market Adapter Layer.
"""

from market_adapter.market_adapter_factory import MarketAdapterFactory
from market_adapter.market_adapter_logger import MarketAdapterLogger
from market_adapter.market_adapter_models import (
    MarketStatus,
    MarketDataResult,
)


class MarketAdapterEngine:
    """
    Master controller for Market Data Adapter.
    """

    def __init__(self, provider_name: str):

        self.provider = MarketAdapterFactory.create(provider_name)

    def initialize(self):

        connected = self.provider.connect()

        status = MarketStatus(
            connected=connected,
            market_open=True,
            provider_name="MT5",
        )

        result = MarketDataResult(
            approved=True,
            reason="Market adapter initialization completed successfully.",
            status=status,
        )

        MarketAdapterLogger.log(result)

        return result