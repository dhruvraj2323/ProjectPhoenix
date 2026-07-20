"""
=================================================
Project Phoenix
Live Trading Models
=================================================

Standard live trading models.
"""

from dataclasses import dataclass


# -------------------------------------------------
# Live Order
# -------------------------------------------------


@dataclass
class LiveOrder:

    ticket: int
    symbol: str
    direction: str
    volume: float
    entry_price: float


# -------------------------------------------------
# Live Position
# -------------------------------------------------


@dataclass
class LivePosition:

    ticket: int
    symbol: str
    direction: str
    volume: float

    entry_price: float
    current_price: float

    profit: float


# -------------------------------------------------
# Live Portfolio
# -------------------------------------------------


@dataclass
class LivePortfolio:

    balance: float
    equity: float

    floating_profit: float
    closed_profit: float


# -------------------------------------------------
# Live Trading Status
# -------------------------------------------------


@dataclass
class LiveTradingStatus:

    running: bool
    account_balance: float
    total_positions: int


# -------------------------------------------------
# Live Trading Result
# -------------------------------------------------


@dataclass
class LiveTradingResult:

    approved: bool
    reason: str
    status: LiveTradingStatus