from live_trading.mt5_connector import (
    MT5Connector,
)


def test_mt5_connector():

    connector = MT5Connector()

    assert connector.login is not None

    assert connector.server != ""

    assert connector.connect() is True

    account = connector.get_account_info()

    assert account is not None

    connector.disconnect()