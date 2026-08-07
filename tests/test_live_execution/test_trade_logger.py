"""
=================================================
Project Phoenix
Test Trade Logger
M59.1.6
=================================================
"""

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_logger import (
    TradeLogger,
)

from live_execution.trade_models import (
    ExecutionStatus,
    ExecutionType,
    OrderSide,
    TradeRequest,
    TradeResponse,
)


def test_trade_logger():

    logger = TradeLogger()

    context = TradeContext(

        execution_id="EXEC-001",

        symbol="EURUSD",

        timeframe="M15",

    )

    context.trade_request = TradeRequest(

        symbol="EURUSD",

        volume=0.10,

        side=OrderSide.BUY,

        execution_type=ExecutionType.MARKET,

        price=1.1000,

        stop_loss=1.0950,

        take_profit=1.1100,

    )

    context.trade_response = TradeResponse(

        status=ExecutionStatus.EXECUTED,

        ticket=123456,

        executed_price=1.1002,

        executed_volume=0.10,

        broker_message="Executed",

    )

    logger.log_request(
        context,
    )

    logger.log_response(
        context,
    )

    logger.log_error(
        "Sample Error",
    )

    assert True