"""
=================================================
Project Phoenix
MT5 Connector Test
M55
=================================================
"""

from live_trading.mt5_connector import (
    MT5Connector,
)


def test_mt5_connector():

    connector = MT5Connector()

    assert connector.connect()

    result = connector.send_order()

    assert result.success

    assert result.retcode == 0

    connector.disconnect()