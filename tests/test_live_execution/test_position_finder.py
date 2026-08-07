"""
=================================================
Project Phoenix
Test Position Finder
M59.3.4
=================================================
"""

from unittest.mock import patch

from live_execution.position_finder import (
    PositionFinder,
)


class DummyPosition:

    def __init__(
        self,
        ticket: int,
    ):

        self.ticket = ticket


@patch(
    "MetaTrader5.positions_get",
)
def test_position_finder(
    mock_positions,
):

    mock_positions.return_value = [

        DummyPosition(101),

        DummyPosition(202),

        DummyPosition(303),

    ]

    finder = PositionFinder()

    position = finder.by_ticket(
        202,
    )

    assert position is not None

    assert position.ticket == 202

    assert (
        finder.by_ticket(
            999,
        )
        is None
    )