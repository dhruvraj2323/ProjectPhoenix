"""
=================================================
Project Phoenix
Test Order Sender
M59.3.1
=================================================
"""

from unittest.mock import patch

from live_execution.order_sender import (
    OrderSender,
)


class DummyResult:

    retcode = 10009


@patch(
    "MetaTrader5.order_send",
)
def test_order_sender(
    mock_order_send,
):

    mock_order_send.return_value = (
        DummyResult()
    )

    sender = OrderSender()

    result = sender.send(
        {},
    )

    assert result.retcode == 10009