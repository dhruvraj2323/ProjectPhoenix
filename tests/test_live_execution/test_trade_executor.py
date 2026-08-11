"""
=================================================
Project Phoenix
Test Trade Executor
M59.1.8
=================================================
"""

from unittest.mock import patch

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_executor import (
    TradeExecutor,
)

from live_execution.trade_models import (
    ExecutionStatus,
    ExecutionType,
    OrderSide,
    TradeRequest,
)


class DummyCheckResult:
    retcode = 0
    comment = "Done"


class DummyFailedCheckResult:
    retcode = 10014
    comment = "Invalid volume"


class DummyResult:
    retcode = 10009
    order = 123456
    price = 1.1000
    volume = 0.10
    comment = "Executed"


class DummySymbolInfo:
    name = "XAUUSDm"
    visible = True
    trade_mode = 0
    trade_exemode = 0
    filling_mode = 1
    trade_stops_level = 0
    trade_freeze_level = 0


def create_trade_context() -> TradeContext:

    context = TradeContext(
        execution_id="EXEC-001",
        symbol="XAUUSDm",
        timeframe="M15",
    )

    context.trade_request = TradeRequest(
        symbol="XAUUSDm",
        volume=0.10,
        side=OrderSide.BUY,
        execution_type=ExecutionType.MARKET,
        price=1.1000,
        stop_loss=1.0950,
        take_profit=1.1100,
    )

    return context


# ==================================================
# TEST 1
# order_check PASS → order_send allowed
# ==================================================

@patch(
    "MetaTrader5.symbol_info",
)
@patch(
    "MetaTrader5.order_check",
)
@patch(
    "MetaTrader5.order_send",
)
def test_trade_executor_order_check_pass(
    mock_order_send,
    mock_order_check,
    mock_symbol_info,
):

    mock_symbol_info.return_value = (
        DummySymbolInfo()
    )

    mock_order_check.return_value = (
        DummyCheckResult()
    )

    mock_order_send.return_value = (
        DummyResult()
    )

    context = create_trade_context()

    executor = TradeExecutor()

    response = executor.execute(
        context,
    )

    # --------------------------------------------------
    # Execution Result
    # --------------------------------------------------

    assert (
        response.status
        == ExecutionStatus.EXECUTED
    )

    assert (
        response.ticket
        == 123456
    )

    # --------------------------------------------------
    # order_check MUST happen
    # --------------------------------------------------

    mock_order_check.assert_called_once()

    # --------------------------------------------------
    # order_send MUST happen only after
    # successful order_check
    # --------------------------------------------------

    mock_order_send.assert_called_once()

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    assert (
        context.metadata[
            "mt5_order_check_retcode"
        ]
        == 0
    )

    assert (
        context.metadata[
            "mt5_order_check_comment"
        ]
        == "Done"
    )


# ==================================================
# TEST 2
# order_check FAIL → order_send BLOCKED
# ==================================================

@patch(
    "MetaTrader5.symbol_info",
)
@patch(
    "MetaTrader5.order_check",
)
@patch(
    "MetaTrader5.order_send",
)
def test_trade_executor_order_check_fail(
    mock_order_send,
    mock_order_check,
    mock_symbol_info,
):

    mock_symbol_info.return_value = (
        DummySymbolInfo()
    )

    mock_order_check.return_value = (
        DummyFailedCheckResult()
    )

    context = create_trade_context()

    executor = TradeExecutor()

    response = executor.execute(
        context,
    )

    # --------------------------------------------------
    # Trade MUST be rejected
    # --------------------------------------------------

    assert (
        response.status
        == ExecutionStatus.FAILED
    )

    assert (
        context.failed
        is True
    )

    # --------------------------------------------------
    # order_check MUST happen
    # --------------------------------------------------

    mock_order_check.assert_called_once()

    # --------------------------------------------------
    # CRITICAL SAFETY ASSERTION
    #
    # Failed pre-check MUST prevent
    # actual order_send().
    # --------------------------------------------------

    mock_order_send.assert_not_called()

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    assert (
        context.metadata[
            "mt5_order_check_retcode"
        ]
        == 10014
    )

    assert (
        context.metadata[
            "mt5_order_check_comment"
        ]
        == "Invalid volume"
    )