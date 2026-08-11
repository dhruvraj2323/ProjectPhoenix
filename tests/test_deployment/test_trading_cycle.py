"""
=================================================
Project Phoenix
Trading Cycle Reporting Integration Test
M60.3.2
=================================================
"""

from datetime import UTC, datetime
from unittest.mock import MagicMock

from deployment.trading_cycle import (
    TradingCycle,
)

from execution_engine.execution_models import (
    ExecutionResult,
    ExecutionStatus,
)

from reporting.reporting_models import (
    DailyReport,
    TradeRecord,
)


class DummyTradeResponse:

    ticket = 2372901969

    executed_price = 4381.838

    executed_volume = 0.01

    broker_message = "ok"

    execution_time = datetime(
        2026,
        8,
        11,
        16,
        51,
        4,
        tzinfo=UTC,
    )

    retcode = 10009


def test_trading_cycle_execution_reporting():

    # --------------------------------------------------
    # Trading Cycle
    # --------------------------------------------------

    cycle = TradingCycle()

    # --------------------------------------------------
    # Mock Pipeline Context
    # --------------------------------------------------

    context = MagicMock()

    context.symbol = "XAUUSDm"

    context.execution_result = (
        ExecutionResult(
            accepted=True,
            status=ExecutionStatus.ACCEPTED,
            order_id="2372901969",
            executed_price=4381.838,
        )
    )

    context.metadata = {
        "trade_response": (
            DummyTradeResponse()
        )
    }

    context.completed = True

    context.failed = False

    # --------------------------------------------------
    # Strategy
    # --------------------------------------------------

    context.strategy_result = MagicMock()

    signal = MagicMock()

    signal.direction.value = "BUY"

    signal.strategy_name.value = (
        "S01_EMA_TREND"
    )

    signal.entry_price = 4379.000

    signal.metadata = {}

    context.strategy_result.signals = [
        signal,
    ]

    # --------------------------------------------------
    # Risk
    # --------------------------------------------------

    context.risk_result = MagicMock()

    context.risk_result.metrics = (
        MagicMock(
            stop_loss=4370.000,
            take_profit=4400.000,
            position_size=0.01,
        )
    )

    # --------------------------------------------------
    # Pipeline Context
    # --------------------------------------------------

    cycle.pipeline_context = (
        context
    )

    # --------------------------------------------------
    # Mock Reporting Boundary
    # --------------------------------------------------

    trade_record = TradeRecord(
        trade_id="2372901969",
        symbol="XAUUSDm",
        direction="BUY",
        strategy="S01_EMA_TREND",
        pattern="",
        entry_price=4381.838,
        exit_price=0.0,
        stop_loss=4370.000,
        take_profit=4400.000,
        volume=0.01,
        profit_loss=0.0,
        status="OPEN",
        opened_at=(
            DummyTradeResponse.execution_time
        ),
        closed_at=(
            DummyTradeResponse.execution_time
        ),
    )

    cycle.trade_record_mapper = (
        MagicMock()
    )

    cycle.trade_record_mapper.map.return_value = (
        trade_record
    )

    report = DailyReport()

    report.output_file = (
        "reports/Daily/2026-08-11_Trading_Report.xlsx"
    )

    cycle.reporting_engine = (
        MagicMock()
    )

    cycle.reporting_engine.run.return_value = (
        report
    )

    # --------------------------------------------------
    # Execute Reporting Integration
    # --------------------------------------------------

    cycle._collect_execution_record()

    assert len(
        cycle.trade_records
    ) == 1

    assert (
        cycle.trade_records[0]
        == trade_record
    )

    cycle._generate_consolidated_report()

    assert (
        cycle.daily_report
        == report
    )

    cycle.reporting_engine.run.assert_called_once_with(
        [trade_record],
    )

    # --------------------------------------------------
    # Mapper Verification
    # --------------------------------------------------

    cycle.trade_record_mapper.map.assert_called_once_with(
        context,
    )

    # --------------------------------------------------
    # Reporting Engine Verification
    # --------------------------------------------------

    cycle.reporting_engine.run.assert_called_once_with(
        [trade_record],
    )

    # --------------------------------------------------
    # Stored Report
    # --------------------------------------------------

    assert (
        cycle.daily_report
        is report
    )

    assert (
        cycle.daily_report.output_file
        == "reports/Daily/2026-08-11_Trading_Report.xlsx"
    )

    # --------------------------------------------------
    # Trade Record Verification
    # --------------------------------------------------

    assert (
        trade_record.trade_id
        == "2372901969"
    )

    assert (
        trade_record.symbol
        == "XAUUSDm"
    )

    assert (
        trade_record.direction
        == "BUY"
    )

    assert (
        trade_record.entry_price
        == 4381.838
    )

    assert (
        trade_record.volume
        == 0.01
    )

    print()

    print(
        "===== Trading Cycle Reporting ====="
    )

    print(
        "Trade ID    :",
        trade_record.trade_id,
    )

    print(
        "Symbol      :",
        trade_record.symbol,
    )

    print(
        "Entry Price :",
        trade_record.entry_price,
    )

    print(
        "Volume      :",
        trade_record.volume,
    )

    print(
        "Status      :",
        trade_record.status,
    )

    print(
        "Report File :",
        report.output_file,
    )

    print()

    print(
        "Trading Cycle Reporting Test Passed"
    )