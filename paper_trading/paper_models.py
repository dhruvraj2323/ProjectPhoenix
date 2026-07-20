"""
=================================================
Project Phoenix
Paper Trading Models
=================================================

Standard paper trading models.
"""

from dataclasses import dataclass


# -------------------------------------------------
# Paper Order
# -------------------------------------------------


@dataclass
class PaperOrder:

    ticket: int
    symbol: str
    direction: str
    volume: float
    entry_price: float


# -------------------------------------------------
# Paper Position
# -------------------------------------------------


@dataclass
class PaperPosition:

    ticket: int
    symbol: str
    direction: str
    volume: float

    entry_price: float
    current_price: float

    profit: float


# -------------------------------------------------
# Paper Portfolio
# -------------------------------------------------


@dataclass
class PaperPortfolio:

    balance: float
    equity: float

    floating_profit: float
    closed_profit: float


# -------------------------------------------------
# Paper Trading Status
# -------------------------------------------------


@dataclass
class PaperTradingStatus:

    running: bool
    virtual_balance: float
    total_positions: int


# -------------------------------------------------
# Paper Trading Result
# -------------------------------------------------


@dataclass
class PaperTradingResult:

    approved: bool
    reason: str
    status: PaperTradingStatus