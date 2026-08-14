"""
=================================================
Project Phoenix
Telegram Sender Tests
M62.1.4 - Telegram Notification Sender
=================================================
"""

import json

from alert_system.alert_models import (
    AlertMessage,
)

from alert_system.telegram_sender import (
    TelegramSender,
)

from config.telegram_config import (
    TelegramConfiguration,
)


def _configuration():

    return TelegramConfiguration(
        bot_token="test-bot-token",
        chat_id="123456789",
        enabled=True,
    )


def _alert():

    return AlertMessage(
        title="BUY Signal",
        message=(
            "EURUSD BUY @ 1.1065"
        ),
        alert_type="TRADE",
        timestamp="2026-08-13 23:30:00",
    )


def test_telegram_sender_available():

    sender = TelegramSender(
        configuration=_configuration(),
    )

    assert (
        sender.is_available()
        is True
    )


def test_telegram_sender_disabled():

    configuration = TelegramConfiguration(
        bot_token="test-bot-token",
        chat_id="123456789",
        enabled=False,
    )

    sender = TelegramSender(
        configuration=configuration,
    )

    assert (
        sender.is_available()
        is False
    )


def test_telegram_sender_missing_configuration():

    configuration = TelegramConfiguration(
        bot_token="",
        chat_id="",
        enabled=True,
    )

    sender = TelegramSender(
        configuration=configuration,
    )

    assert (
        sender.is_available()
        is False
    )


def test_telegram_sender_payload():

    sender = TelegramSender(
        configuration=_configuration(),
    )

    payload = sender._payload(
        _alert()
    )

    decoded = json.loads(
        payload.decode("utf-8")
    )

    assert (
        decoded["chat_id"]
        == "123456789"
    )

    assert (
        decoded["text"]
        == (
            "BUY Signal\n"
            "EURUSD BUY @ 1.1065"
        )
    )


def test_telegram_sender_api_url():

    sender = TelegramSender(
        configuration=_configuration(),
    )

    url = sender._api_url()

    assert (
        url
        == (
            "https://api.telegram.org/"
            "bottest-bot-token/"
            "sendMessage"
        )
    )


def test_telegram_sender_success(
    monkeypatch,
):

    class FakeResponse:

        def __enter__(self):
            return self

        def __exit__(
            self,
            exc_type,
            exc_value,
            traceback,
        ):
            return False

        def read(self):

            return (
                b'{"ok":true}'
            )

    def fake_urlopen(
        request,
        timeout,
    ):

        assert (
            timeout
            == 10
        )

        assert (
            request.get_method()
            == "POST"
        )

        return FakeResponse()

    monkeypatch.setattr(
        "urllib.request.urlopen",
        fake_urlopen,
    )

    sender = TelegramSender(
        configuration=_configuration(),
    )

    result = sender.send(
        _alert()
    )

    assert result is True


def test_telegram_sender_api_failure(
    monkeypatch,
):

    def fake_urlopen(
        request,
        timeout,
    ):

        raise OSError(
            "Telegram unavailable"
        )

    monkeypatch.setattr(
        "urllib.request.urlopen",
        fake_urlopen,
    )

    sender = TelegramSender(
        configuration=_configuration(),
    )

    result = sender.send(
        _alert()
    )

    assert result is False


def test_telegram_sender_timeout(
    monkeypatch,
):

    def fake_urlopen(
        request,
        timeout,
    ):

        raise TimeoutError(
            "Telegram request timed out"
        )

    monkeypatch.setattr(
        "urllib.request.urlopen",
        fake_urlopen,
    )

    sender = TelegramSender(
        configuration=_configuration(),
    )

    result = sender.send(
        _alert()
    )

    assert result is False