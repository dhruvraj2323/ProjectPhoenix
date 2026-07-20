"""
=================================================
Project Phoenix
Market Adapter Factory
=================================================

Creates market data provider instances.
"""

from market_adapter.market_data_provider import MarketDataProvider


class MT5Provider(MarketDataProvider):
    """
    Dummy MT5 market data provider.
    """

    def connect(self):
        return True

    def disconnect(self):
        return True

    def symbols(self):
        return ["EURUSD", "GBPUSD"]

    def latest_tick(self):
        return {"bid": 1.1064, "ask": 1.1066}

    def latest_price(self):
        return 1.1065

    def historical_data(self):
        return []

    def current_candle(self):
        return {}

    def market_status(self):
        return "OPEN"

    def is_connected(self):
        return True


class MarketAdapterFactory:
    """
    Creates market data provider implementations.
    """

    @staticmethod
    def create(provider_name: str) -> MarketDataProvider:

        provider_name = provider_name.upper()

        if provider_name == "MT5":
            return MT5Provider()

        raise ValueError(
            f"Unsupported market data provider: {provider_name}"
        )