"""
=================================================
Project Phoenix
Account Sync Test
M55
=================================================
"""

from live_trading.account_sync import AccountSync
from live_trading.live_context import LiveContext


def test_account_sync():

    context = LiveContext(
        live_id="LIVE-001",
        account_id="ACC-001",
        symbol="EURUSD",
        timeframe="M1",
    )

    context.account.balance = 100000.0

    context.account.equity = 100250.0
    
    context.account.leverage = 100

    sync = AccountSync()

    sync.sync(context)

    assert context.account.balance == 100000.0

    assert context.account.equity == 100250.0

    assert context.account.leverage == 100.0