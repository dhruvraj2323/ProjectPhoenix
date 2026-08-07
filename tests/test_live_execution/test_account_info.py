"""
=================================================
Project Phoenix
Test Account Information
M59.3.8
=================================================
"""

from unittest.mock import patch

from live_execution.account_info import (
    AccountInfo,
)


class DummyAccount:

    balance = 10000.0

    equity = 9985.5

    margin_free = 9500.0

    leverage = 100


@patch(
    "MetaTrader5.account_info",
)
def test_account_info(
    mock_account,
):

    mock_account.return_value = (
        DummyAccount()
    )

    account = AccountInfo()

    assert account.balance() == 10000.0

    assert account.equity() == 9985.5

    assert account.free_margin() == 9500.0

    assert account.leverage() == 100