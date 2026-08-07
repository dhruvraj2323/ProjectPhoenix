"""
=================================================
Project Phoenix
Test Position History
M59.3.7
=================================================
"""

from datetime import datetime
from unittest.mock import patch

from live_execution.position_history import (
    PositionHistory,
)


@patch(
    "MetaTrader5.history_deals_get",
)
def test_position_history(
    mock_history,
):

    mock_history.return_value = [
        object(),
        object(),
    ]

    history = PositionHistory()

    deals = history.get_history(

        datetime(2025, 1, 1),

        datetime(2025, 12, 31),

    )

    assert len(deals) == 2