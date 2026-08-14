"""
=================================================
Project Phoenix
Alert Sender Tests
M62.1.5 - Telegram-only AlertSender Integration
=================================================
"""

from unittest.mock import MagicMock

from alert_system.alert_formatter import (
    AlertFormatter,
)

from alert_system.alert_sender import (
    AlertSender,
)


def _create_alert():

    return AlertFormatter.trade_alert(
        symbol="EURUSD",
        direction="BUY",
        price=1.1065,
    )


def test_alert_sender_telegram_delivery():

    telegram_sender = MagicMock()

    telegram_sender.send.return_value = True

    sender = AlertSender(
        telegram_sender=telegram_sender,
    )

    alert = _create_alert()

    delivered = sender.send(
        alert
    )

    telegram_sender.send.assert_called_once_with(
        alert
    )

    assert (
        delivered
        == ["Telegram"]
    )


def test_alert_sender_telegram_delivery_failed():

    telegram_sender = MagicMock()

    telegram_sender.send.return_value = False

    sender = AlertSender(
        telegram_sender=telegram_sender,
    )

    alert = _create_alert()

    delivered = sender.send(
        alert
    )

    telegram_sender.send.assert_called_once_with(
        alert
    )

    assert delivered == []


def test_alert_sender_has_only_telegram_channel():

    telegram_sender = MagicMock()

    sender = AlertSender(
        telegram_sender=telegram_sender,
    )

    assert (
        sender.TELEGRAM_CHANNEL
        == "Telegram"
    )

    assert not hasattr(
        sender,
        "email_sender",
    )


def test_alert_sender_does_not_send_email():

    telegram_sender = MagicMock()

    telegram_sender.send.return_value = True

    sender = AlertSender(
        telegram_sender=telegram_sender,
    )

    alert = _create_alert()

    delivered = sender.send(
        alert
    )

    assert (
        delivered
        == ["Telegram"]
    )

    telegram_sender.send.assert_called_once_with(
        alert
    )