"""
=================================================
Project Phoenix
Alert Engine Tests
M62.1.5 - Telegram-only Alert Integration
=================================================
"""

from unittest.mock import MagicMock

from alert_system.alert_engine import (
    AlertEngine,
)


def test_alert_engine():

    sender = MagicMock()

    sender.send.return_value = [
        "Telegram",
    ]

    engine = AlertEngine(
        sender=sender,
    )

    result = (
        engine.initialize()
    )

    assert result.approved is True

    assert (
        result.reason
        == "Alert system initialized successfully."
    )

    assert (
        result.status.running
        is True
    )

    assert (
        result.status.alerts_sent
        == 1
    )

    assert (
        result.status.connected_channels
        == 1
    )

    assert (
        result.delivered_channels
        == [
            "Telegram",
        ]
    )

    sender.send.assert_called_once()


def test_alert_engine_telegram_delivery_failed():

    sender = MagicMock()

    sender.send.return_value = []

    engine = AlertEngine(
        sender=sender,
    )

    result = (
        engine.initialize()
    )

    assert result.approved is True

    assert (
        result.status.running
        is True
    )

    assert (
        result.status.alerts_sent
        == 1
    )

    assert (
        result.status.connected_channels
        == 0
    )

    assert (
        result.delivered_channels
        == []
    )

    sender.send.assert_called_once()


def test_alert_engine_shutdown():

    engine = AlertEngine(
        sender=MagicMock(),
    )

    assert (
        engine.shutdown()
        is True
    )