"""
=================================================
Project Phoenix
Test Connection Health Checker
M59.4.5
=================================================
"""

from unittest.mock import patch

from live_execution.connection_health_checker import (
    ConnectionHealthChecker,
)


class DummyTerminal:

    connected = True


@patch(
    "MetaTrader5.terminal_info",
)
def test_connection_health_checker(
    mock_terminal,
):

    mock_terminal.return_value = (
        DummyTerminal()
    )

    checker = (
        ConnectionHealthChecker()
    )

    assert checker.validate() is True