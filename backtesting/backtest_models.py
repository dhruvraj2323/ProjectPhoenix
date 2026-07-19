"""
Project Phoenix
Milestone M16 - Backtesting Engine

Module:
    backtest_models.py

Purpose:
    Defines all core data models used by the
    Backtesting Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class BacktestStatus(Enum):
    """
    Final backtest status.
    """

    APPROVED = "APPROVED"

    REJECTED = "REJECTED"


@dataclass
class BacktestTrade:
    """
    Represents one simulated trade.
    """

    symbol: str

    entry_price: float

    exit_price: float

    volume: float

    profit: float

    win: bool


@dataclass
class BacktestStatistics:
    """
    Summary statistics of the backtest.
    """

    total_trades: int

    win_rate: float

    net_profit: float

    profit_factor: float

    max_drawdown: float

    expectancy: float


@dataclass
class BacktestContext:
    """
    Context supplied to the Backtesting Engine.
    """

    strategy_name: str

    symbol: str

    timeframe: str

    initial_balance: float

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class BacktestDecision:
    """
    Final output of the Backtesting Engine.
    """

    status: BacktestStatus

    statistics: BacktestStatistics

    approved: bool

    reason: Optional[str] = None