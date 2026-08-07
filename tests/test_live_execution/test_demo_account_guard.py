"""
=================================================
Project Phoenix
Test Demo Account Guard
M59.4.1
=================================================
"""

from unittest.mock import patch

from live_execution.demo_account_guard import (
    DemoAccountGuard,
)


class DummyDemoAccount:

    trade_mode = 0


@patch(
    "MetaTrader5.account_info",
)
def test_demo_account_guard(
    mock_account,
):

    mock_account.return_value = (
        DummyDemoAccount()
    )

    guard = DemoAccountGuard()

    assert guard.validate() is True