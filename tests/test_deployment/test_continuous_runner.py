"""
=================================================
Project Phoenix
Continuous Runner Tests
M61.5 - Deployment Runtime Status
=================================================
"""

from unittest.mock import MagicMock

from deployment.continuous_runner import (
    ContinuousRunner,
)

from deployment.execution_summary import (
    CycleExecutionStatus,
)


# =========================================================
# Helpers
# =========================================================

def _create_runner(
    status: CycleExecutionStatus,
    execute_result: bool = True,
) -> ContinuousRunner:
    """
    Create a ContinuousRunner with a mocked
    TradingCycle and execution summary.
    """

    runner = ContinuousRunner(
        interval=0,
    )

    runner.trading_cycle = MagicMock()

    runner.trading_cycle.execute.return_value = (
        execute_result
    )

    runner.trading_cycle.execution_summary = (
        MagicMock()
    )

    runner.trading_cycle.execution_summary.status = (
        status
    )

    return runner


# =========================================================
# Existing M58 Test
# =========================================================

def test_continuous_runner():

    runner = ContinuousRunner(
        interval=0,
    )

    assert runner.running is False

    runner.start(
        cycles=1,
    )

    assert runner.running is False

    assert runner.run_once() is True


# =========================================================
# M61.5
# Test A
# ALL_EXECUTED
# =========================================================

def test_continuous_runner_all_executed():

    runner = _create_runner(
        status=(
            CycleExecutionStatus.ALL_EXECUTED
        ),
        execute_result=True,
    )

    result = runner.run_once()

    assert result is True

    assert (
        runner.trading_cycle.execute.call_count
        == 1
    )


# =========================================================
# M61.5
# Test B
# PARTIAL_SUCCESS
# =========================================================

def test_continuous_runner_partial_success():

    runner = _create_runner(
        status=(
            CycleExecutionStatus.PARTIAL_SUCCESS
        ),
        execute_result=True,
    )

    result = runner.run_once()

    # Partial success must keep the runner
    # operational.

    assert result is True

    assert (
        runner.trading_cycle.execute.call_count
        == 1
    )


# =========================================================
# M61.5
# Test C
# NO_TRADES
# =========================================================

def test_continuous_runner_no_trades():

    runner = _create_runner(
        status=(
            CycleExecutionStatus.NO_TRADES
        ),
        execute_result=True,
    )

    result = runner.run_once()

    # No trade is a valid completed cycle.
    # It is not a runtime failure.

    assert result is True

    assert (
        runner.trading_cycle.execute.call_count
        == 1
    )


# =========================================================
# M61.5
# Test D
# ALL_FAILED
# =========================================================

def test_continuous_runner_all_failed():

    runner = _create_runner(
        status=(
            CycleExecutionStatus.ALL_FAILED
        ),
        execute_result=True,
    )

    result = runner.run_once()

    # TradingCycle may complete its cycle and
    # return True, but ALL_FAILED must be
    # interpreted as a failed deployment cycle.

    assert result is False

    assert (
        runner.trading_cycle.execute.call_count
        == 1
    )


# =========================================================
# M61.5
# Test E
# Runner Continues After Partial Success
# =========================================================

def test_continuous_runner_partial_success_start():

    runner = _create_runner(
        status=(
            CycleExecutionStatus.PARTIAL_SUCCESS
        ),
        execute_result=True,
    )

    runner.start(
        cycles=1,
    )

    assert runner.running is False

    assert (
        runner.trading_cycle.execute.call_count
        == 1
    )


# =========================================================
# M61.5
# Test F
# Runner Handles No Trade Cycle
# =========================================================

def test_continuous_runner_no_trade_start():

    runner = _create_runner(
        status=(
            CycleExecutionStatus.NO_TRADES
        ),
        execute_result=True,
    )

    runner.start(
        cycles=1,
    )

    assert runner.running is False

    assert (
        runner.trading_cycle.execute.call_count
        == 1
    )


# =========================================================
# M61.5
# Test G
# Runner Handles All Failed Cycle
# =========================================================

def test_continuous_runner_all_failed_start():

    runner = _create_runner(
        status=(
            CycleExecutionStatus.ALL_FAILED
        ),
        execute_result=True,
    )

    runner.start(
        cycles=1,
    )

    assert runner.running is False

    assert (
        runner.trading_cycle.execute.call_count
        == 1
    )


# =========================================================
# M61.5
# Test H
# Trading Cycle Exception
# =========================================================

def test_continuous_runner_exception():

    runner = ContinuousRunner(
        interval=0,
    )

    runner.trading_cycle = MagicMock()

    runner.trading_cycle.execute.side_effect = (
        RuntimeError(
            "Simulated trading cycle failure."
        )
    )

    result = runner.run_once()

    assert result is False

    assert (
        runner.trading_cycle.execute.call_count
        == 1
    )

# =========================================================
# M61.5.3
# Test I
# Execution Summary Must Be Read From TradingCycle
# =========================================================

def test_continuous_runner_reads_execution_summary():

    runner = _create_runner(
        status=(
            CycleExecutionStatus.PARTIAL_SUCCESS
        ),
        execute_result=True,
    )

    assert (
        runner.trading_cycle.execution_summary
        is not None
    )

    result = runner.run_once()

    assert result is True

    assert (
        runner.trading_cycle.execution_summary.status
        == CycleExecutionStatus.PARTIAL_SUCCESS
    )


# =========================================================
# M61.5.3
# Test J
# ALL_FAILED Overrides TradingCycle True Result
# =========================================================

def test_continuous_runner_all_failed_overrides_true_result():

    runner = _create_runner(
        status=(
            CycleExecutionStatus.ALL_FAILED
        ),
        execute_result=True,
    )

    # TradingCycle itself returned True.
    assert (
        runner.trading_cycle.execute()
        is True
    )

    # Reset mock call history before the
    # actual runner invocation.
    runner.trading_cycle.execute.reset_mock()

    result = runner.run_once()

    assert result is False

    assert (
        runner.trading_cycle.execute.call_count
        == 1
    )


# =========================================================
# M61.5.3
# Test K
# Partial Success Must Remain Successful
# =========================================================

def test_continuous_runner_partial_success_preserved():

    runner = _create_runner(
        status=(
            CycleExecutionStatus.PARTIAL_SUCCESS
        ),
        execute_result=True,
    )

    result = runner.run_once()

    assert result is True

    assert (
        runner.trading_cycle.execution_summary.status
        == CycleExecutionStatus.PARTIAL_SUCCESS
    )