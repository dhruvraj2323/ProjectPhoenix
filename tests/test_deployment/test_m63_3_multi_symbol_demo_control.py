"""
=================================================
Project Phoenix
M63.3 - Multi-Symbol Demo Trading Control
=================================================

Purpose
-------
Validate the existing M61.3 TradingCycle multi-symbol
isolation boundary for the controlled DEMO symbol set:

    EURUSDm
    XAUUSDm
    BTCUSDm

M63.3 does NOT create a new multi-symbol controller.

The existing TradingCycle is the production boundary
under test.

Required guarantees
-------------------
1. Each configured symbol is processed independently.
2. One symbol failure does not stop remaining symbols.
3. Failed symbols retain their own failure state.
4. Successful symbols retain their own execution state.
5. Consolidated execution summary remains correct.
6. Symbol execution identifiers remain isolated.
7. All-symbol failure is represented correctly.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from deployment.execution_summary import (
    CycleExecutionStatus,
    SymbolExecutionStatus,
)

from deployment.trading_cycle import (
    TradingCycle,
)


# =========================================================
# M63.3 Controlled DEMO Symbol Set
# =========================================================

M63_3_SYMBOLS = (
    "EURUSDm",
    "XAUUSDm",
    "BTCUSDm",
)


# =========================================================
# Helpers
# =========================================================

def _build_cycle(
    symbols=M63_3_SYMBOLS,
):
    """
    Build the real TradingCycle using its existing
    production constructor.

    RuntimeConfig exposes symbols as a read-only
    property. Therefore the test modifies the
    underlying configuration data rather than
    assigning to the property.
    """

    cycle = TradingCycle()

    cycle.config.data["market"]["symbols"] = list(
        symbols
    )

    return cycle


def _prepare_cycle(
    cycle,
    failures=None,
):
    """
    Isolate the existing TradingCycle orchestration
    from external MT5 / pipeline services.

    The production multi-symbol loop remains under test.
    """

    failures = failures or {}

    # -----------------------------------------------------
    # MT5 connection is already tested elsewhere.
    # -----------------------------------------------------

    cycle._connect_mt5 = MagicMock()

    # -----------------------------------------------------
    # Avoid external report generation.
    # -----------------------------------------------------

    cycle._generate_trading_report = MagicMock()

    cycle._generate_consolidated_report = MagicMock()

    cycle._finish = MagicMock()

    # -----------------------------------------------------
    # Simulate successful execution record collection.
    #
    # The trade ID is generated from the CURRENT symbol,
    # proving symbol state remains isolated.
    # -----------------------------------------------------

    def collect_execution_record():

        symbol = cycle.current_symbol

        trade_record = MagicMock()

        trade_record.trade_id = (
            f"EXEC-{symbol}"
        )

        trade_record.symbol = symbol

        cycle.trade_records.append(
            trade_record
        )

        return True

    cycle._collect_execution_record = (
        collect_execution_record
    )

    # -----------------------------------------------------
    # Simulate the symbol processing pipeline.
    #
    # Failure is injected only for the requested symbol.
    # -----------------------------------------------------

    def load_market_data():

        symbol = cycle.current_symbol

        if symbol in failures:

            raise failures[symbol]

        cycle.market_data = {
            "M15": []
        }

        cycle.candles = [object()]

    cycle._load_market_data = (
        load_market_data
    )

    cycle._run_market_pipeline = MagicMock()

    cycle._validate_pipeline_result = MagicMock()

    return cycle


# =========================================================
# Test 1
# =========================================================

def test_m63_3_all_three_demo_symbols_are_processed():

    cycle = _build_cycle()

    _prepare_cycle(cycle)

    assert cycle.execute() is True

    assert (
        cycle.execution_summary.total_symbols
        == 3
    )

    assert (
        cycle.execution_summary.executed_symbols
        == 3
    )

    assert (
        cycle.execution_summary.failed_symbols
        == 0
    )

    assert (
        cycle.execution_summary.status
        == CycleExecutionStatus.ALL_EXECUTED
    )

    assert {
        result.symbol
        for result in cycle.execution_summary.symbol_results
    } == set(M63_3_SYMBOLS)


# =========================================================
# Test 2
# =========================================================

def test_eurusd_failure_does_not_stop_other_symbols():

    cycle = _build_cycle()

    _prepare_cycle(
        cycle,
        failures={
            "EURUSDm": RuntimeError(
                "EURUSDm simulated failure"
            )
        },
    )

    assert cycle.execute() is True

    assert (
        cycle.execution_summary.total_symbols
        == 3
    )

    assert (
        cycle.execution_summary.executed_symbols
        == 2
    )

    assert (
        cycle.execution_summary.failed_symbols
        == 1
    )

    assert (
        cycle.execution_summary.status
        == CycleExecutionStatus.PARTIAL_SUCCESS
    )

    result_by_symbol = {
        result.symbol: result
        for result in cycle.execution_summary.symbol_results
    }

    assert (
        result_by_symbol["EURUSDm"].status
        == SymbolExecutionStatus.FAILED
    )

    assert (
        result_by_symbol["XAUUSDm"].status
        == SymbolExecutionStatus.EXECUTED
    )

    assert (
        result_by_symbol["BTCUSDm"].status
        == SymbolExecutionStatus.EXECUTED
    )


# =========================================================
# Test 3
# =========================================================

def test_xauusd_failure_does_not_stop_other_symbols():

    cycle = _build_cycle()

    _prepare_cycle(
        cycle,
        failures={
            "XAUUSDm": RuntimeError(
                "XAUUSDm simulated failure"
            )
        },
    )

    assert cycle.execute() is True

    result_by_symbol = {
        result.symbol: result
        for result in cycle.execution_summary.symbol_results
    }

    assert (
        result_by_symbol["EURUSDm"].status
        == SymbolExecutionStatus.EXECUTED
    )

    assert (
        result_by_symbol["XAUUSDm"].status
        == SymbolExecutionStatus.FAILED
    )

    assert (
        result_by_symbol["BTCUSDm"].status
        == SymbolExecutionStatus.EXECUTED
    )

    assert (
        cycle.execution_summary.status
        == CycleExecutionStatus.PARTIAL_SUCCESS
    )


# =========================================================
# Test 4
# =========================================================

def test_btcusd_failure_does_not_stop_other_symbols():

    cycle = _build_cycle()

    _prepare_cycle(
        cycle,
        failures={
            "BTCUSDm": RuntimeError(
                "BTCUSDm simulated failure"
            )
        },
    )

    assert cycle.execute() is True

    result_by_symbol = {
        result.symbol: result
        for result in cycle.execution_summary.symbol_results
    }

    assert (
        result_by_symbol["EURUSDm"].status
        == SymbolExecutionStatus.EXECUTED
    )

    assert (
        result_by_symbol["XAUUSDm"].status
        == SymbolExecutionStatus.EXECUTED
    )

    assert (
        result_by_symbol["BTCUSDm"].status
        == SymbolExecutionStatus.FAILED
    )

    assert (
        cycle.execution_summary.status
        == CycleExecutionStatus.PARTIAL_SUCCESS
    )


# =========================================================
# Test 5
# =========================================================

@pytest.mark.parametrize(
    "failed_symbol",
    M63_3_SYMBOLS,
)
def test_any_single_symbol_failure_is_isolated(
    failed_symbol,
):

    cycle = _build_cycle()

    _prepare_cycle(
        cycle,
        failures={
            failed_symbol: RuntimeError(
                f"{failed_symbol} simulated failure"
            )
        },
    )

    assert cycle.execute() is True

    assert (
        cycle.execution_summary.total_symbols
        == 3
    )

    assert (
        cycle.execution_summary.failed_symbols
        == 1
    )

    assert (
        cycle.execution_summary.executed_symbols
        == 2
    )

    result_by_symbol = {
        result.symbol: result
        for result in cycle.execution_summary.symbol_results
    }

    assert (
        result_by_symbol[failed_symbol].status
        == SymbolExecutionStatus.FAILED
    )

    for symbol in M63_3_SYMBOLS:

        if symbol == failed_symbol:
            continue

        assert (
            result_by_symbol[symbol].status
            == SymbolExecutionStatus.EXECUTED
        )


# =========================================================
# Test 6
# =========================================================

def test_two_symbol_failures_do_not_stop_remaining_symbol():

    cycle = _build_cycle()

    _prepare_cycle(
        cycle,
        failures={
            "EURUSDm": RuntimeError(
                "EURUSDm simulated failure"
            ),
            "XAUUSDm": RuntimeError(
                "XAUUSDm simulated failure"
            ),
        },
    )

    assert cycle.execute() is True

    result_by_symbol = {
        result.symbol: result
        for result in cycle.execution_summary.symbol_results
    }

    assert (
        result_by_symbol["EURUSDm"].status
        == SymbolExecutionStatus.FAILED
    )

    assert (
        result_by_symbol["XAUUSDm"].status
        == SymbolExecutionStatus.FAILED
    )

    assert (
        result_by_symbol["BTCUSDm"].status
        == SymbolExecutionStatus.EXECUTED
    )

    assert (
        cycle.execution_summary.executed_symbols
        == 1
    )

    assert (
        cycle.execution_summary.failed_symbols
        == 2
    )

    assert (
        cycle.execution_summary.status
        == CycleExecutionStatus.PARTIAL_SUCCESS
    )


# =========================================================
# Test 7
# =========================================================

def test_all_symbol_failures_are_contained():

    cycle = _build_cycle()

    _prepare_cycle(
        cycle,
        failures={
            "EURUSDm": RuntimeError(
                "EURUSDm simulated failure"
            ),
            "XAUUSDm": RuntimeError(
                "XAUUSDm simulated failure"
            ),
            "BTCUSDm": RuntimeError(
                "BTCUSDm simulated failure"
            ),
        },
    )

    assert cycle.execute() is True

    assert (
        cycle.execution_summary.total_symbols
        == 3
    )

    assert (
        cycle.execution_summary.executed_symbols
        == 0
    )

    assert (
        cycle.execution_summary.failed_symbols
        == 3
    )

    assert (
        cycle.execution_summary.status
        == CycleExecutionStatus.ALL_FAILED
    )


# =========================================================
# Test 8
# =========================================================

def test_symbol_execution_ids_remain_isolated():

    cycle = _build_cycle()

    _prepare_cycle(cycle)

    assert cycle.execute() is True

    result_by_symbol = {
        result.symbol: result
        for result in cycle.execution_summary.symbol_results
    }

    assert (
        result_by_symbol["EURUSDm"].trade_id
        == "EXEC-EURUSDm"
    )

    assert (
        result_by_symbol["XAUUSDm"].trade_id
        == "EXEC-XAUUSDm"
    )

    assert (
        result_by_symbol["BTCUSDm"].trade_id
        == "EXEC-BTCUSDm"
    )


# =========================================================
# Test 9
# =========================================================

def test_failed_symbol_retains_its_own_error():

    cycle = _build_cycle()

    failure_message = (
        "BTCUSDm isolated demo failure"
    )

    _prepare_cycle(
        cycle,
        failures={
            "BTCUSDm": RuntimeError(
                failure_message
            )
        },
    )

    assert cycle.execute() is True

    result_by_symbol = {
        result.symbol: result
        for result in cycle.execution_summary.symbol_results
    }

    assert (
        result_by_symbol["BTCUSDm"].status
        == SymbolExecutionStatus.FAILED
    )

    assert (
        result_by_symbol["BTCUSDm"].error
        == failure_message
    )

    assert (
        result_by_symbol["EURUSDm"].error
        == ""
    )

    assert (
        result_by_symbol["XAUUSDm"].error
        == ""
    )


# =========================================================
# Test 10
# =========================================================

def test_summary_contains_exact_target_symbols():

    cycle = _build_cycle()

    _prepare_cycle(cycle)

    assert cycle.execute() is True

    symbols = [
        result.symbol
        for result in (
            cycle.execution_summary.symbol_results
        )
    ]

    assert symbols == list(
        M63_3_SYMBOLS
    )


# =========================================================
# Test 11
# =========================================================

def test_symbol_processing_order_is_preserved():

    cycle = _build_cycle()

    _prepare_cycle(cycle)

    assert cycle.execute() is True

    symbols = [
        result.symbol
        for result in (
            cycle.execution_summary.symbol_results
        )
    ]

    assert symbols == [
        "EURUSDm",
        "XAUUSDm",
        "BTCUSDm",
    ]


# =========================================================
# Test 12
# =========================================================

def test_failure_in_middle_symbol_does_not_corrupt_later_symbol():

    cycle = _build_cycle()

    _prepare_cycle(
        cycle,
        failures={
            "XAUUSDm": RuntimeError(
                "XAUUSDm middle-symbol failure"
            )
        },
    )

    assert cycle.execute() is True

    results = (
        cycle.execution_summary.symbol_results
    )

    assert len(results) == 3

    assert results[0].symbol == "EURUSDm"
    assert (
        results[0].status
        == SymbolExecutionStatus.EXECUTED
    )

    assert results[1].symbol == "XAUUSDm"
    assert (
        results[1].status
        == SymbolExecutionStatus.FAILED
    )

    assert results[2].symbol == "BTCUSDm"
    assert (
        results[2].status
        == SymbolExecutionStatus.EXECUTED
    )

    assert (
        results[2].trade_id
        == "EXEC-BTCUSDm"
    )