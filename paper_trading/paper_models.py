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


@dataclass(slots=True)
class PaperOrder:

    ticket: int
    symbol: str
    direction: str
    volume: float
    entry_price: float


# -------------------------------------------------
# Paper Position
# -------------------------------------------------


@dataclass(slots=True)
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


@dataclass(slots=True)
class PaperPortfolio:

    balance: float
    equity: float

    floating_profit: float
    closed_profit: float


# -------------------------------------------------
# Paper Trading Status
# -------------------------------------------------


@dataclass(slots=True)
class PaperTradingStatus:

    running: bool
    virtual_balance: float
    total_positions: int


# -------------------------------------------------
# Paper Trading Result
# -------------------------------------------------


@dataclass(slots=True)
class PaperTradingResult:

    approved: bool
    reason: str
    status: PaperTradingStatus