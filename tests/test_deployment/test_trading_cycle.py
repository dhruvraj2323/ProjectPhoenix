"""
Project Phoenix
Trading Cycle Tests
M61.2 - Multi-Symbol Execution Validation
"""

from datetime import UTC, datetime
from unittest.mock import MagicMock

from deployment.trading_cycle import TradingCycle

from execution_engine.execution_models import (
    ExecutionResult,
    ExecutionStatus,
)

from reporting.reporting_models import (
    DailyReport,
    TradeRecord,
)


# =========================================================
# Dummy MT5 Trade Response
# =========================================================

class DummyTradeResponse:

    ticket = 2372901969

    executed_price = 4381.838

    executed_volume = 0.01

    execution_time = datetime(
        2026,
        8,
        11,
        16,
        51,
        4,
        tzinfo=UTC,
    )


# =========================================================
# Helpers
# =========================================================

def _create_success_context(
    symbol: str,
    ticket: str,
    price: float,
) -> MagicMock:

    context = MagicMock()

    context.symbol = symbol

    context.execution_result = (
        ExecutionResult(
            accepted=True,
            status=ExecutionStatus.ACCEPTED,
            order_id=ticket,
            executed_price=price,
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

    signal.entry_price = price - 2.838

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
            stop_loss=price - 10.0,
            take_profit=price + 20.0,
            position_size=0.01,
        )
    )

    # --------------------------------------------------
    # Pipeline Validation
    # --------------------------------------------------

    context.candles = [1]

    context.indicators = {
        "ema": 1,
    }

    context.patterns = [
        "pattern",
    ]

    context.signals = [
        signal,
    ]

    context.ai_result = object()

    context.portfolio_result = object()

    context.approved = True

    context.decision = (
        "PIPELINE_COMPLETED"
    )

    context.reason = (
        "Pipeline executed successfully."
    )

    return context


def _create_trade_record(
    symbol: str,
    ticket: str,
    price: float,
) -> TradeRecord:

    execution_time = (
        DummyTradeResponse.execution_time
    )

    return TradeRecord(

        trade_id=ticket,

        symbol=symbol,

        direction="BUY",

        strategy="S01_EMA_TREND",

        pattern="",

        entry_price=price,

        exit_price=0.0,

        stop_loss=price - 10.0,

        take_profit=price + 20.0,

        volume=0.01,

        profit_loss=0.0,

        status="OPEN",

        opened_at=execution_time,

        closed_at=execution_time,
    )


# =========================================================
# Existing Reporting Integration Test
# =========================================================

def test_trading_cycle_execution_reporting():

    # --------------------------------------------------
    # Trading Cycle
    # --------------------------------------------------

    cycle = TradingCycle()

    # --------------------------------------------------
    # Mock Pipeline Context
    # --------------------------------------------------

    context = _create_success_context(
        symbol="XAUUSDm",
        ticket="2372901969",
        price=4381.838,
    )

    cycle.pipeline_context = context

    # --------------------------------------------------
    # Reporting Boundary
    # --------------------------------------------------

    trade_record = _create_trade_record(
        symbol="XAUUSDm",
        ticket="2372901969",
        price=4381.838,
    )

    cycle.trade_record_mapper = (
        MagicMock()
    )

    cycle.trade_record_mapper.map.return_value = (
        trade_record
    )

    report = DailyReport()

    report.output_file = (
        "reports/Daily/"
        "2026-08-11_Trading_Report.xlsx"
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

    # --------------------------------------------------
    # Assertions
    # --------------------------------------------------

    assert len(
        cycle.trade_records
    ) == 1

    assert (
        cycle.trade_records[0].symbol
        == "XAUUSDm"
    )

    assert (
        cycle.trade_records[0].trade_id
        == "2372901969"
    )


# =========================================================
# M61.2
# Test A
# Multi-Symbol Independent Records
# =========================================================

def test_trading_cycle_multi_symbol_records():

    cycle = TradingCycle()

    # --------------------------------------------------
    # Configure Two Symbols
    # --------------------------------------------------

    cycle.config = MagicMock()

    cycle.config.symbols = [
        "XAUUSDm",
        "BTCUSDm",
    ]

    cycle.config.timeframe = "M15"
    cycle.config.bars = 500

    # --------------------------------------------------
    # Prepare Independent Contexts
    # --------------------------------------------------

    xau_context = _create_success_context(
        symbol="XAUUSDm",
        ticket="XAU-001",
        price=4381.838,
    )

    btc_context = _create_success_context(
        symbol="BTCUSDm",
        ticket="BTC-001",
        price=63505.370,
    )

    contexts = {
        "XAUUSDm": xau_context,
        "BTCUSDm": btc_context,
    }

    # --------------------------------------------------
    # Mock Pipeline
    # --------------------------------------------------

    def mock_run_market_pipeline():

        cycle.pipeline_context = (
            contexts[
                cycle.current_symbol
            ]
        )

        cycle.pipeline_completed = True

        cycle.execution_completed = True

        cycle.paper_trading_completed = True

    cycle._run_market_pipeline = (
        mock_run_market_pipeline
    )

    # --------------------------------------------------
    # Mock Other Cycle Boundaries
    # --------------------------------------------------

    cycle._load_market_data = (
        MagicMock()
    )

    cycle._validate_pipeline_result = (
        MagicMock()
    )

    cycle._generate_trading_report = (
        MagicMock()
    )

    cycle._finish = (
        MagicMock()
    )

    # --------------------------------------------------
    # Trade Records
    # --------------------------------------------------

    xau_record = _create_trade_record(
        symbol="XAUUSDm",
        ticket="XAU-001",
        price=4381.838,
    )

    btc_record = _create_trade_record(
        symbol="BTCUSDm",
        ticket="BTC-001",
        price=63505.370,
    )

    def mock_collect_execution_record():

        record = (
            xau_record
            if cycle.current_symbol
            == "XAUUSDm"
            else btc_record
        )

        cycle.trade_records.append(
            record
        )

    cycle._collect_execution_record = (
        mock_collect_execution_record
    )

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    result = cycle.execute()

    # --------------------------------------------------
    # Assertions
    # --------------------------------------------------

    assert result is True

    assert len(
        cycle.trade_records
    ) == 2

    assert {
        record.symbol
        for record in cycle.trade_records
    } == {
        "XAUUSDm",
        "BTCUSDm",
    }

    assert {
        record.trade_id
        for record in cycle.trade_records
    } == {
        "XAU-001",
        "BTC-001",
    }

    # --------------------------------------------------
    # Both Symbols Processed
    # --------------------------------------------------

    assert (
        cycle._load_market_data.call_count
        == 2
    )

    assert (
        cycle._validate_pipeline_result.call_count
        == 2
    )

    assert (
        cycle._generate_trading_report.call_count
        == 2
    )

    cycle._finish.assert_called_once()


# =========================================================
# M61.2
# Test B
# One Symbol Failure Must Not Block Another
# =========================================================

def test_trading_cycle_symbol_failure_isolated():

    cycle = TradingCycle()

    # --------------------------------------------------
    # Configure Two Symbols
    # --------------------------------------------------

    cycle.config = MagicMock()

    cycle.config.symbols = [
        "XAUUSDm",
        "BTCUSDm",
    ]

    cycle.config.timeframe = "M15"
    cycle.config.bars = 500

    # --------------------------------------------------
    # XAUUSDm Failure
    # BTCUSDm Success
    # --------------------------------------------------

    def mock_run_market_pipeline():

        if cycle.current_symbol == "XAUUSDm":

            raise RuntimeError(
                "Simulated XAUUSDm failure."
            )

        cycle.pipeline_context = (
            _create_success_context(
                symbol="BTCUSDm",
                ticket="BTC-002",
                price=63505.370,
            )
        )

        cycle.pipeline_completed = True

        cycle.execution_completed = True

        cycle.paper_trading_completed = True

    cycle._run_market_pipeline = (
        mock_run_market_pipeline
    )

    # --------------------------------------------------
    # Mock Market Loading
    # --------------------------------------------------

    cycle._load_market_data = (
        MagicMock()
    )

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    cycle._validate_pipeline_result = (
        MagicMock()
    )

    # --------------------------------------------------
    # Reporting
    # --------------------------------------------------

    cycle._generate_trading_report = (
        MagicMock()
    )

    # --------------------------------------------------
    # Finish
    # --------------------------------------------------

    cycle._finish = (
        MagicMock()
    )

    # --------------------------------------------------
    # BTC Trade Record
    # --------------------------------------------------

    btc_record = _create_trade_record(
        symbol="BTCUSDm",
        ticket="BTC-002",
        price=63505.370,
    )

    def mock_collect_execution_record():

        if cycle.current_symbol == "BTCUSDm":

            cycle.trade_records.append(
                btc_record
            )

    cycle._collect_execution_record = (
        mock_collect_execution_record
    )

    # --------------------------------------------------
    # Execute
    #
    # M61.2 requirement:
    # XAU failure must not abort BTC.
    # --------------------------------------------------

    result = cycle.execute()

    # --------------------------------------------------
    # Assertions
    # --------------------------------------------------

    assert result is True

    # --------------------------------------------------
    # BTCUSDm Must Have Been Processed
    # --------------------------------------------------

    assert (
        cycle.current_symbol
        == "BTCUSDm"
    )

    assert (
        cycle._load_market_data.call_count
        == 2
    )

    # --------------------------------------------------
    # Only Successful Trade Recorded
    # --------------------------------------------------

    assert len(
        cycle.trade_records
    ) == 1

    assert (
        cycle.trade_records[0].symbol
        == "BTCUSDm"
    )

    assert (
        cycle.trade_records[0].trade_id
        == "BTC-002"
    )

    # --------------------------------------------------
    # Cycle Must Finish
    # --------------------------------------------------

    cycle._finish.assert_called_once()