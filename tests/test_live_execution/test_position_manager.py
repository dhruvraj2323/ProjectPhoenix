"""
=================================================
Project Phoenix
Test Position Manager
M59.3.3
=================================================
"""

from unittest.mock import patch

from live_execution.position_manager import (
    PositionManager,
)


@patch(
    "MetaTrader5.positions_get",
)
def test_position_manager(
    mock_positions,
):

    mock_positions.return_value = [
        object(),
        object(),
        object(),
    ]

    manager = PositionManager()

    assert manager.total_positions() == 3

    assert (
        manager.total_positions(
            "EURUSD",
        )
        == 3
    )