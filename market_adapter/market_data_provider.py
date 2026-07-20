"""
=================================================
Project Phoenix
Market Data Provider Interface
=================================================

Abstract interface for all market data providers.
"""

from abc import ABC, abstractmethod


class MarketDataProvider(ABC):
    """
    Standard interface that every market data provider
    must implement.
    """

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def symbols(self):
        pass

    @abstractmethod
    def latest_tick(self):
        pass

    @abstractmethod
    def latest_price(self):
        pass

    @abstractmethod
    def historical_data(self):
        pass

    @abstractmethod
    def current_candle(self):
        pass

    @abstractmethod
    def market_status(self):
        pass

    @abstractmethod
    def is_connected(self):
        pass