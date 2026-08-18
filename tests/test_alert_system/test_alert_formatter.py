"""
=================================================
Project Phoenix
Alert Formatter Tests
=================================================
"""

from alert_system.alert_formatter import (
    AlertFormatter,
)


def test_alert_formatter():

    trade = AlertFormatter.trade_alert(
        symbol="EURUSD",
        direction="BUY",
        price=1.1065,
    )

    risk = AlertFormatter.risk_alert(
        "Maximum daily loss reached."
    )

    system = AlertFormatter.system_alert(
        "Dashboard initialized."
    )

    assert trade.title == "BUY Signal"

    assert (
        trade.message
        == "EURUSD BUY @ 1.1065"
    )

    assert (
        trade.alert_type
        == "TRADE"
    )

    assert (
        risk.title
        == "Risk Alert"
    )

    assert (
        risk.alert_type
        == "RISK"
    )

    assert (
        system.title
        == "System Alert"
    )

    assert (
        system.alert_type
        == "SYSTEM"
    )