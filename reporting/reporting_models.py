"""
=================================================
Project Phoenix
Reporting Models
M57
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


# --------------------------------------------------
# Trade Record
# --------------------------------------------------


@dataclass(slots=True)
class TradeRecord:
    """
    Individual trade information.
    """

    trade_id: str = ""

    symbol: str = ""

    direction: str = ""

    strategy: str = ""

    pattern: str = ""

    entry_price: float = 0.0

    exit_price: float = 0.0

    stop_loss: float = 0.0

    take_profit: float = 0.0

    volume: float = 0.0

    profit_loss: float = 0.0

    status: str = ""

    opened_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    closed_at: datetime = field(
        default_factory=datetime.utcnow,
    )


# --------------------------------------------------
# Performance Summary
# --------------------------------------------------


@dataclass(slots=True)
class PerformanceSummary:
    """
    Daily trading statistics.
    """

    total_trades: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    win_rate: float = 0.0

    gross_profit: float = 0.0

    gross_loss: float = 0.0

    net_profit: float = 0.0

    average_profit: float = 0.0

    average_loss: float = 0.0

    profit_factor: float = 0.0


# --------------------------------------------------
# Daily Report
# --------------------------------------------------


@dataclass(slots=True)
class DailyReport:
    """
    Complete daily trading report.
    """

    report_date: datetime = field(
        default_factory=datetime.utcnow,
    )

    generated_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    trades: list[TradeRecord] = field(
        default_factory=list,
    )

    summary: PerformanceSummary = field(
        default_factory=PerformanceSummary,
    )

    report_name: str = ""

    output_file: str = ""