"""
=================================================
Project Phoenix
Order Executor Test
M55
=================================================
"""

from live_trading.order_executor import (
    OrderExecutor,
)


def test_order_executor():

    executor = OrderExecutor()

    result = executor.execute()

    assert result.success

    assert result.retcode == 0

    assert result.broker_ticket != ""