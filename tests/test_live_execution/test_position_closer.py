"""
=================================================
Project Phoenix
Test Position Closer
M59.3.5
=================================================
"""

from unittest.mock import patch

from live_execution.position_closer import (
    PositionCloser,
)


class DummyResult:

    retcode = 10009


@patch(
    "MetaTrader5.order_send",
)
def test_position_closer(
    mock_order_send,
):

    mock_order_send.return_value = (
        DummyResult()
    )

    closer = PositionCloser()

    result = closer.close(

        ticket=12345,

        symbol="EURUSD",

        volume=0.10,

        order_type=1,

        price=1.1000,

    )

    assert result.retcode == 10009