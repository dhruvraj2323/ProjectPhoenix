"""
=================================================
Project Phoenix
Test Position Modifier
M59.3.6
=================================================
"""

from unittest.mock import patch

from live_execution.position_modifier import (
    PositionModifier,
)


class DummyResult:

    retcode = 10009


@patch(
    "MetaTrader5.order_send",
)
def test_position_modifier(
    mock_order_send,
):

    mock_order_send.return_value = (
        DummyResult()
    )

    modifier = PositionModifier()

    result = modifier.modify(

        ticket=12345,

        symbol="EURUSD",

        stop_loss=1.0950,

        take_profit=1.1100,

    )

    assert result.retcode == 10009