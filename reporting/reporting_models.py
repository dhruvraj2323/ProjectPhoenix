"""
=================================================
Project Phoenix
Reporting Models
=================================================

Defines reporting and analytics models.
"""

from dataclasses import dataclass


# -------------------------------------------------
# Report Summary
# -------------------------------------------------


@dataclass(slots=True)
class ReportSummary:

    report_name: str

    generated_at: str

    total_records: int


# -------------------------------------------------
# Trade Statistics
# -------------------------------------------------


@dataclass(slots=True)
class TradeStatistics:

    total_trades: int

    winning_trades: int

    losing_trades: int

    win_rate: float

    loss_rate: float


# -------------------------------------------------
# Performance Analytics
# -------------------------------------------------


@dataclass(slots=True)
class PerformanceAnalytics:

    net_profit: float

    gross_profit: float

    gross_loss: float

    profit_factor: float

    expectancy: float

    drawdown: float


# -------------------------------------------------
# Equity Curve
# -------------------------------------------------


@dataclass(slots=True)
class EquityCurve:

    starting_balance: float

    current_balance: float

    highest_balance: float


# -------------------------------------------------
# Monthly Statistics
# -------------------------------------------------


@dataclass(slots=True)
class MonthlyStatistics:

    month: str

    trades: int

    profit: float

    win_rate: float


# -------------------------------------------------
# Reporting Status
# -------------------------------------------------


@dataclass(slots=True)
class ReportingStatus:

    generated: bool

    analytics_completed: bool

    report_name: str


# -------------------------------------------------
# Reporting Result
# -------------------------------------------------


@dataclass(slots=True)
class ReportingResult:

    approved: bool

    reason: str

    status: ReportingStatus