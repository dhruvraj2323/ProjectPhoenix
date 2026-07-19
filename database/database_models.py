"""
=================================================
Project Phoenix
Database Models
=================================================

Defines all database entities used by
the Database Layer.
"""

from dataclasses import dataclass


# -------------------------------------------------
# Trade Record
# -------------------------------------------------


@dataclass(slots=True)
class TradeRecord:

    trade_id: int
    symbol: str
    direction: str

    entry_price: float
    exit_price: float

    stop_loss: float
    take_profit: float

    lot_size: float

    profit: float

    open_time: str
    close_time: str


# -------------------------------------------------
# Signal Record
# -------------------------------------------------


@dataclass(slots=True)
class SignalRecord:

    signal_id: int

    symbol: str

    signal_type: str

    strength: int

    confidence: float

    timestamp: str


# -------------------------------------------------
# Performance Record
# -------------------------------------------------


@dataclass(slots=True)
class PerformanceRecord:

    total_trades: int

    win_rate: float

    net_profit: float

    profit_factor: float

    drawdown: float

    expectancy: float

    timestamp: str


# -------------------------------------------------
# Learning Record
# -------------------------------------------------


@dataclass(slots=True)
class LearningRecord:

    recommendation_type: str

    current_value: float

    suggested_value: float

    confidence: float

    reason: str

    timestamp: str


# -------------------------------------------------
# Configuration Record
# -------------------------------------------------


@dataclass(slots=True)
class ConfigurationRecord:

    name: str

    value: str

    environment: str

    version: str


# -------------------------------------------------
# Database Status
# -------------------------------------------------


@dataclass(slots=True)
class DatabaseStatus:

    connected: bool

    initialized: bool

    database_name: str


# -------------------------------------------------
# Database Result
# -------------------------------------------------


@dataclass(slots=True)
class DatabaseResult:

    approved: bool

    reason: str

    status: DatabaseStatus