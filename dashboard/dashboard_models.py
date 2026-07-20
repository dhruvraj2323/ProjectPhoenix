"""
=================================================
Project Phoenix
Dashboard Models
=================================================

Standard dashboard models.
"""

from dataclasses import dataclass


# -------------------------------------------------
# Dashboard Account
# -------------------------------------------------


@dataclass
class DashboardAccount:

    balance: float
    equity: float

    floating_profit: float
    closed_profit: float


# -------------------------------------------------
# Dashboard Position
# -------------------------------------------------


@dataclass
class DashboardPosition:

    symbol: str
    direction: str

    volume: float

    entry_price: float
    current_price: float

    profit: float


# -------------------------------------------------
# Dashboard Signal
# -------------------------------------------------


@dataclass
class DashboardSignal:

    symbol: str

    signal: str

    strength: float
    confidence: float


# -------------------------------------------------
# Dashboard Status
# -------------------------------------------------


@dataclass
class DashboardStatus:

    running: bool
    connected: bool

    refresh_rate: int


# -------------------------------------------------
# Dashboard Result
# -------------------------------------------------


@dataclass
class DashboardResult:

    approved: bool
    reason: str

    status: DashboardStatus