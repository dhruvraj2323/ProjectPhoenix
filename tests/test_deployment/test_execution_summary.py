"""
=================================================
Project Phoenix
Execution Summary Tests
M61.3
=================================================
"""

from deployment.execution_summary import (
    CycleExecutionStatus,
    CycleExecutionSummary,
    SymbolExecutionResult,
    SymbolExecutionStatus,
)


def test_all_symbols_executed():

    summary = CycleExecutionSummary()

    summary.add_result(
        SymbolExecutionResult(
            symbol="XAUUSDm",
            status=SymbolExecutionStatus.EXECUTED,
            trade_id="XAU-001",
        )
    )

    summary.add_result(
        SymbolExecutionResult(
            symbol="BTCUSDm",
            status=SymbolExecutionStatus.EXECUTED,
            trade_id="BTC-001",
        )
    )

    assert summary.total_symbols == 2

    assert summary.executed_symbols == 2

    assert summary.no_trade_symbols == 0

    assert summary.failed_symbols == 0

    assert (
        summary.status
        == CycleExecutionStatus.ALL_EXECUTED
    )


def test_partial_success():

    summary = CycleExecutionSummary()

    summary.add_result(
        SymbolExecutionResult(
            symbol="XAUUSDm",
            status=SymbolExecutionStatus.FAILED,
            error="Simulated failure",
        )
    )

    summary.add_result(
        SymbolExecutionResult(
            symbol="BTCUSDm",
            status=SymbolExecutionStatus.EXECUTED,
            trade_id="BTC-001",
        )
    )

    assert summary.total_symbols == 2

    assert summary.executed_symbols == 1

    assert summary.no_trade_symbols == 0

    assert summary.failed_symbols == 1

    assert (
        summary.status
        == CycleExecutionStatus.PARTIAL_SUCCESS
    )


def test_no_trades():

    summary = CycleExecutionSummary()

    summary.add_result(
        SymbolExecutionResult(
            symbol="XAUUSDm",
            status=SymbolExecutionStatus.NO_TRADE,
        )
    )

    summary.add_result(
        SymbolExecutionResult(
            symbol="BTCUSDm",
            status=SymbolExecutionStatus.NO_TRADE,
        )
    )

    assert summary.total_symbols == 2

    assert summary.executed_symbols == 0

    assert summary.no_trade_symbols == 2

    assert summary.failed_symbols == 0

    assert (
        summary.status
        == CycleExecutionStatus.NO_TRADES
    )


def test_all_failed():

    summary = CycleExecutionSummary()

    summary.add_result(
        SymbolExecutionResult(
            symbol="XAUUSDm",
            status=SymbolExecutionStatus.FAILED,
            error="XAU failure",
        )
    )

    summary.add_result(
        SymbolExecutionResult(
            symbol="BTCUSDm",
            status=SymbolExecutionStatus.FAILED,
            error="BTC failure",
        )
    )

    assert summary.total_symbols == 2

    assert summary.executed_symbols == 0

    assert summary.no_trade_symbols == 0

    assert summary.failed_symbols == 2

    assert (
        summary.status
        == CycleExecutionStatus.ALL_FAILED
    )


def test_empty_summary():

    summary = CycleExecutionSummary()

    assert summary.total_symbols == 0

    assert summary.executed_symbols == 0

    assert summary.no_trade_symbols == 0

    assert summary.failed_symbols == 0

    assert (
        summary.status
        == CycleExecutionStatus.NO_TRADES
    )