"""
=================================================
Project Phoenix
Live Trading Models Test
M55
=================================================
"""

from live_trading.live_models import (
    BrokerType,
    LiveAccount,
    LiveExecutionResult,
    LiveOrder,
    LivePosition,
    LiveResult,
    LiveStatistics,
    LiveTrade,
    OrderStatus,
    OrderType,
    PositionDirection,
)


def test_live_models():

    order = LiveOrder(
        order_id="ORD-001",
        broker_order_id="MT5-1001",
        symbol="EURUSD",
        order_type=OrderType.BUY,
        volume=0.10,
        price=1.1050,
        status=OrderStatus.SUBMITTED,
    )

    position = LivePosition(
        position_id="POS-001",
        broker_position_id="MT5-2001",
        symbol="EURUSD",
        direction=PositionDirection.LONG,
    )

    trade = LiveTrade(
        trade_id="TRD-001",
        broker_ticket="3001",
        symbol="EURUSD",
    )

    account = LiveAccount(
        account_id="ACC-001",
        broker=BrokerType.MT5,
    )

    execution = LiveExecutionResult(
        success=True,
        broker_ticket="3001",
    )

    statistics = LiveStatistics()

    result = LiveResult(
        success=True,
        execution_result=execution,
        statistics=statistics,
    )

    assert order.symbol == "EURUSD"
    assert position.symbol == "EURUSD"
    assert trade.symbol == "EURUSD"
    assert account.broker == BrokerType.MT5
    assert result.success