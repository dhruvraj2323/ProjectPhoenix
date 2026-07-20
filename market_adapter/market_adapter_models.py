"""
=================================================
Project Phoenix
Market Adapter Models
=================================================

Standardized market data models.
"""

from dataclasses import dataclass
from datetime import datetime


# -------------------------------------------------
# Market Candle
# -------------------------------------------------


@dataclass
class MarketCandle:
    """
    OHLC candle.
    """

    symbol: str
    timeframe: str
    timestamp: datetime

    open: float
    high: float
    low: float
    close: float

    volume: int


# -------------------------------------------------
# Tick Data
# -------------------------------------------------


@dataclass
class TickData:
    """
    Tick information.
    """

    symbol: str

    bid: float
    ask: float
    last: float

    timestamp: datetime


# -------------------------------------------------
# Symbol Information
# -------------------------------------------------


@dataclass
class SymbolInformation:
    """
    Symbol metadata.
    """

    symbol: str
    digits: int
    spread: int
    trade_allowed: bool


# -------------------------------------------------
# Market Status
# -------------------------------------------------


@dataclass
class MarketStatus:
    """
    Market provider status.
    """

    connected: bool
    market_open: bool
    provider_name: str


# -------------------------------------------------
# Market Data Result
# -------------------------------------------------


@dataclass
class MarketDataResult:
    """
    Final adapter result.
    """

    approved: bool
    reason: str
    status: MarketStatus