"""
=================================================
Project Phoenix
Test Market Status Validator
M59.4.2
=================================================
"""

from unittest.mock import patch

from live_execution.market_status_validator import (
    MarketStatusValidator,
)


class DummySymbol:

    visible = True

    trade_mode = 1


@patch(
    "MetaTrader5.symbol_info",
)
def test_market_status_validator(
    mock_symbol_info,
):

    mock_symbol_info.return_value = (
        DummySymbol()
    )

    validator = (
        MarketStatusValidator()
    )

    assert (
        validator.validate(
            "EURUSD",
        )
        is True
    )