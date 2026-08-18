"""
=================================================
Project Phoenix
Reporting Models
M63.7 - Demo Reporting & Analytics
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


# --------------------------------------------------
# Trade Record
# --------------------------------------------------


@dataclass(slots=True)
class TradeRecord:
    """
    Individual trade information.

    M63.7 extends the existing M57/M61.4 trade
    record with optional DEMO observation fields.

    IMPORTANT:
    These fields observe information already available
    from upstream Phoenix execution/context contracts.

    They do not execute trades, calculate risk, or
    perform reconciliation.
    """

    # --------------------------------------------------
    # Existing M57 trade fields
    # --------------------------------------------------

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
        default_factory=lambda: datetime.now(UTC),
    )

    closed_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    # --------------------------------------------------
    # M63.7 Demo Observation
    # --------------------------------------------------

    strategy_decision: str = ""

    risk_decision: str = ""

    execution_status: str = ""

    execution_message: str = ""

    execution_retcode: int | None = None

    requested_price: float | None = None

    executed_price: float | None = None

    requested_volume: float | None = None

    executed_volume: float | None = None

    order_check_retcode: int | None = None

    order_check_message: str = ""

    # --------------------------------------------------
    # Runtime Observation
    # --------------------------------------------------

    runtime_state: str = ""

    trading_protection_state: str = ""

    # --------------------------------------------------
    # M63.6 Governance Observation
    #
    # These remain optional because the current
    # repository does not yet have a production caller
    # propagating RiskExposureGovernanceResult into
    # the reporting context.
    # --------------------------------------------------

    governance_state: str = ""

    governance_reason: str = ""

    balance: float | None = None

    equity: float | None = None

    free_margin: float | None = None

    open_positions: int | None = None

    symbol_exposure: float | None = None

    gross_exposure: float | None = None

    net_exposure: float | None = None

    portfolio_heat: float | None = None

    risk_percent: float | None = None

    drawdown: float | None = None

    # --------------------------------------------------
    # Optional Market / Execution Analytics
    #
    # M63.7 does not invent these values.
    # They are populated only when an upstream context
    # explicitly provides them.
    # --------------------------------------------------

    spread: float | None = None

    slippage: float | None = None

    mfe: float | None = None

    mae: float | None = None

    # --------------------------------------------------
    # Observation Error
    # --------------------------------------------------

    observation_error: str = ""


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

    M61.4:
    Carries the existing cycle-level execution summary.

    M63.7:
    TradeRecord now contains optional DEMO observation
    fields while the existing report structure remains
    unchanged.
    """

    report_date: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    generated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    trades: list[TradeRecord] = field(
        default_factory=list,
    )

    summary: PerformanceSummary = field(
        default_factory=PerformanceSummary,
    )

    # --------------------------------------------------
    # M61.4 Cycle Execution Summary
    # --------------------------------------------------

    execution_summary: Any = None

    # --------------------------------------------------
    # Report Metadata
    # --------------------------------------------------

    report_name: str = ""

    output_file: str = ""