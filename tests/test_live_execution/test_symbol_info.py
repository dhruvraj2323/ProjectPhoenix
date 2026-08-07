"""
=================================================
Project Phoenix
Test Symbol Information
M59.3.9
=================================================
"""

from unittest.mock import patch

from live_execution.symbol_info import (
    SymbolInfo,
)


class DummySymbol:

    digits = 5

    point = 0.00001

    spread = 12

    volume_min = 0.01

    volume_max = 100.0

    volume_step = 0.01


@patch(
    "MetaTrader5.symbol_info",
)
def test_symbol_info(
    mock_symbol,
):

    mock_symbol.return_value = (
        DummySymbol()
    )

    info = SymbolInfo()

    assert info.digits(
        "EURUSD",
    ) == 5

    assert info.point(
        "EURUSD",
    ) == 0.00001

    assert info.spread(
        "EURUSD",
    ) == 12

    assert info.volume_min(
        "EURUSD",
    ) == 0.01

    assert info.volume_max(
        "EURUSD",
    ) == 100.0

    assert info.volume_step(
        "EURUSD",
    ) == 0.01