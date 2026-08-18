"""
=================================================
Project Phoenix
Alert Models Tests
=================================================
"""

from alert_system.alert_models import (
    AlertMessage,
    AlertChannel,
    AlertStatus,
    AlertResult,
)


def test_alert_models():

    message = AlertMessage(
        title="BUY Signal",
        message="EURUSD BUY @ 1.1065",
        alert_type="TRADE",
        timestamp="2026-07-20 10:30:00",
    )

    channel = AlertChannel(
        name="Telegram",
        enabled=True,
        connected=True,
    )

    status = AlertStatus(
        running=True,
        alerts_sent=5,
        connected_channels=2,
    )

    result = AlertResult(
        approved=True,
        reason=(
            "Alert system initialized successfully."
        ),
        status=status,
        delivered_channels=[
            "Telegram",
            "Email",
        ],
    )

    assert (
        message.title
        == "BUY Signal"
    )

    assert (
        message.alert_type
        == "TRADE"
    )

    assert (
        channel.name
        == "Telegram"
    )

    assert channel.enabled is True

    assert channel.connected is True

    assert (
        status.alerts_sent
        == 5
    )

    assert (
        status.connected_channels
        == 2
    )

    assert result.approved is True

    assert (
        result.delivered_channels
        == [
            "Telegram",
            "Email",
        ]
    )