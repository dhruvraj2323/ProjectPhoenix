"""
Project Phoenix
Trading Cycle Tests
M61.3 - Multi-Symbol Execution Summary Validation
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

    signal.entry_price = (
        price - 2.838
    )

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

    cycle = TradingCycle()

    context = _create_success_context(
        symbol="XAUUSDm",
        ticket="2372901969",
        price=4381.838,
    )

    cycle.pipeline_context = context

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

    cycle._collect_execution_record()

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

    cycle.config = MagicMock()

    cycle.config.symbols = [
        "XAUUSDm",
        "BTCUSDm",
    ]

    cycle.config.timeframe = "M15"

    cycle.config.bars = 500

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

    result = cycle.execute()

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

    cycle.config = MagicMock()

    cycle.config.symbols = [
        "XAUUSDm",
        "BTCUSDm",
    ]

    cycle.config.timeframe = "M15"

    cycle.config.bars = 500

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

    result = cycle.execute()

    assert result is True

    assert (
        cycle.current_symbol
        == "BTCUSDm"
    )

    assert (
        cycle._load_market_data.call_count
        == 2
    )

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

    cycle._finish.assert_called_once()


# =========================================================
# M61.3
# Test C
# All Symbols Executed
# =========================================================

def test_trading_cycle_summary_all_executed():

    cycle = TradingCycle()

    cycle.config = MagicMock()

    cycle.config.symbols = [
        "XAUUSDm",
        "BTCUSDm",
    ]

    cycle.config.timeframe = "M15"

    cycle.config.bars = 500

    contexts = {
        "XAUUSDm": _create_success_context(
            symbol="XAUUSDm",
            ticket="XAU-003",
            price=4381.838,
        ),
        "BTCUSDm": _create_success_context(
            symbol="BTCUSDm",
            ticket="BTC-003",
            price=63505.370,
        ),
    }

    def mock_run_market_pipeline():

        cycle.pipeline_context = (
            contexts[
                cycle.current_symbol
            ]
        )

    cycle._run_market_pipeline = (
        mock_run_market_pipeline
    )

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

    records = {
        "XAUUSDm": _create_trade_record(
            symbol="XAUUSDm",
            ticket="XAU-003",
            price=4381.838,
        ),
        "BTCUSDm": _create_trade_record(
            symbol="BTCUSDm",
            ticket="BTC-003",
            price=63505.370,
        ),
    }

    def mock_collect_execution_record():

        cycle.trade_records.append(
            records[
                cycle.current_symbol
            ]
        )

        return True

    cycle._collect_execution_record = (
        mock_collect_execution_record
    )

    result = cycle.execute()

    assert result is True

    assert (
        cycle.execution_summary.total_symbols
        == 2
    )

    assert (
        cycle.execution_summary.executed_symbols
        == 2
    )

    assert (
        cycle.execution_summary.no_trade_symbols
        == 0
    )

    assert (
        cycle.execution_summary.failed_symbols
        == 0
    )

    assert (
        cycle.execution_summary.status.value
        == "ALL_EXECUTED"
    )

    assert len(
        cycle.execution_summary.symbol_results
    ) == 2

    assert {
        result.symbol
        for result
        in cycle.execution_summary.symbol_results
    } == {
        "XAUUSDm",
        "BTCUSDm",
    }

    cycle._finish.assert_called_once()


# =========================================================
# M61.3
# Test D
# Partial Success
# =========================================================

def test_trading_cycle_summary_partial_success():

    cycle = TradingCycle()

    cycle.config = MagicMock()

    cycle.config.symbols = [
        "XAUUSDm",
        "BTCUSDm",
    ]

    cycle.config.timeframe = "M15"

    cycle.config.bars = 500

    def mock_run_market_pipeline():

        if cycle.current_symbol == "XAUUSDm":

            raise RuntimeError(
                "Simulated XAUUSDm failure."
            )

        cycle.pipeline_context = (
            _create_success_context(
                symbol="BTCUSDm",
                ticket="BTC-004",
                price=63505.370,
            )
        )

    cycle._run_market_pipeline = (
        mock_run_market_pipeline
    )

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

    btc_record = _create_trade_record(
        symbol="BTCUSDm",
        ticket="BTC-004",
        price=63505.370,
    )

    def mock_collect_execution_record():

        if cycle.current_symbol == "BTCUSDm":

            cycle.trade_records.append(
                btc_record
            )

            return True

        return False

    cycle._collect_execution_record = (
        mock_collect_execution_record
    )

    result = cycle.execute()

    assert result is True

    assert (
        cycle.execution_summary.total_symbols
        == 2
    )

    assert (
        cycle.execution_summary.executed_symbols
        == 1
    )

    assert (
        cycle.execution_summary.no_trade_symbols
        == 0
    )

    assert (
        cycle.execution_summary.failed_symbols
        == 1
    )

    assert (
        cycle.execution_summary.status.value
        == "PARTIAL_SUCCESS"
    )

    failed_results = [
        result
        for result
        in cycle.execution_summary.symbol_results
        if result.symbol == "XAUUSDm"
    ]

    assert len(
        failed_results
    ) == 1

    assert (
        failed_results[0].status.value
        == "FAILED"
    )

    assert (
        "Simulated XAUUSDm failure"
        in failed_results[0].error
    )

    executed_results = [
        result
        for result
        in cycle.execution_summary.symbol_results
        if result.symbol == "BTCUSDm"
    ]

    assert len(
        executed_results
    ) == 1

    assert (
        executed_results[0].status.value
        == "EXECUTED"
    )

    assert (
        executed_results[0].trade_id
        == "BTC-004"
    )

    cycle._finish.assert_called_once()


# =========================================================
# M61.3
# Test E
# All Symbols No Trade
# =========================================================

def test_trading_cycle_summary_no_trades():

    cycle = TradingCycle()

    cycle.config = MagicMock()

    cycle.config.symbols = [
        "XAUUSDm",
        "BTCUSDm",
    ]

    cycle.config.timeframe = "M15"

    cycle.config.bars = 500

    contexts = {
        "XAUUSDm": _create_success_context(
            symbol="XAUUSDm",
            ticket="",
            price=4381.838,
        ),
        "BTCUSDm": _create_success_context(
            symbol="BTCUSDm",
            ticket="",
            price=63505.370,
        ),
    }

    def mock_run_market_pipeline():

        cycle.pipeline_context = (
            contexts[
                cycle.current_symbol
            ]
        )

    cycle._run_market_pipeline = (
        mock_run_market_pipeline
    )

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

    def mock_collect_execution_record():

        return False

    cycle._collect_execution_record = (
        mock_collect_execution_record
    )

    result = cycle.execute()

    assert result is True

    assert (
        cycle.execution_summary.total_symbols
        == 2
    )

    assert (
        cycle.execution_summary.executed_symbols
        == 0
    )

    assert (
        cycle.execution_summary.no_trade_symbols
        == 2
    )

    assert (
        cycle.execution_summary.failed_symbols
        == 0
    )

    assert (
        cycle.execution_summary.status.value
        == "NO_TRADES"
    )

    assert len(
        cycle.execution_summary.symbol_results
    ) == 2

    assert all(
        result.status.value == "NO_TRADE"
        for result
        in cycle.execution_summary.symbol_results
    )

    cycle._finish.assert_called_once()


# =========================================================
# M61.3
# Test F
# All Symbols Failed
# =========================================================

def test_trading_cycle_summary_all_failed():

    cycle = TradingCycle()

    cycle.config = MagicMock()

    cycle.config.symbols = [
        "XAUUSDm",
        "BTCUSDm",
    ]

    cycle.config.timeframe = "M15"

    cycle.config.bars = 500

    def mock_run_market_pipeline():

        raise RuntimeError(
            f"Simulated {cycle.current_symbol} failure."
        )

    cycle._run_market_pipeline = (
        mock_run_market_pipeline
    )

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

    result = cycle.execute()

    assert result is True

    assert (
        cycle.execution_summary.total_symbols
        == 2
    )

    assert (
        cycle.execution_summary.executed_symbols
        == 0
    )

    assert (
        cycle.execution_summary.no_trade_symbols
        == 0
    )

    assert (
        cycle.execution_summary.failed_symbols
        == 2
    )

    assert (
        cycle.execution_summary.status.value
        == "ALL_FAILED"
    )

    assert len(
        cycle.execution_summary.symbol_results
    ) == 2

    assert all(
        result.status.value == "FAILED"
        for result
        in cycle.execution_summary.symbol_results
    )

    cycle._finish.assert_called_once()


# =========================================================
# M61.3
# Test G
# Summary Must Reset Between Cycles
# =========================================================

def test_trading_cycle_summary_resets_between_cycles():

    cycle = TradingCycle()

    cycle.config = MagicMock()

    cycle.config.symbols = [
        "XAUUSDm",
    ]

    cycle.config.timeframe = "M15"

    cycle.config.bars = 500

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

    context = _create_success_context(
        symbol="XAUUSDm",
        ticket="RESET-001",
        price=4381.838,
    )

    def mock_run_market_pipeline():

        cycle.pipeline_context = context

    cycle._run_market_pipeline = (
        mock_run_market_pipeline
    )

    def mock_collect_execution_record():

        cycle.trade_records.append(
            _create_trade_record(
                symbol="XAUUSDm",
                ticket="RESET-001",
                price=4381.838,
            )
        )

        return True

    cycle._collect_execution_record = (
        mock_collect_execution_record
    )

    assert cycle.execute() is True

    assert (
        cycle.execution_summary.total_symbols
        == 1
    )

    assert (
        cycle.execution_summary.executed_symbols
        == 1
    )

    assert (
        cycle.execution_summary.status.value
        == "ALL_EXECUTED"
    )

    def mock_collect_no_trade():

        return False

    cycle._collect_execution_record = (
        mock_collect_no_trade
    )

    assert cycle.execute() is True

    assert (
        cycle.execution_summary.total_symbols
        == 1
    )

    assert (
        cycle.execution_summary.executed_symbols
        == 0
    )

    assert (
        cycle.execution_summary.no_trade_symbols
        == 1
    )

    assert (
        cycle.execution_summary.failed_symbols
        == 0
    )

    assert (
        cycle.execution_summary.status.value
        == "NO_TRADES"
    )

    assert len(
        cycle.execution_summary.symbol_results
    ) == 1