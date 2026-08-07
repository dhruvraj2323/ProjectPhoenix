"""
=================================================
Project Phoenix
Test Price Validator
M59.4.4
=================================================
"""

from unittest.mock import patch

from live_execution.price_validator import (
    PriceValidator,
)


@patch(
    "live_execution.symbol_info.SymbolInfo.digits",
)
def test_price_validator(
    mock_digits,
):

    mock_digits.return_value = 5

    validator = PriceValidator()

    assert (
        validator.validate(

            "EURUSD",

            1.10000,

            1.09500,

            1.11000,

        )
        is True
    )