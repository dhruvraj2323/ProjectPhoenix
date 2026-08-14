"""
=================================================
Project Phoenix
Telegram Configuration Tests
M62.1.1 - Telegram Notification Configuration
=================================================
"""

from config.telegram_config import (
    TelegramConfiguration,
)


def test_telegram_configuration():

    configuration = TelegramConfiguration(
        bot_token="test-bot-token",
        chat_id="123456789",
    )

    assert (
        configuration.bot_token
        == "test-bot-token"
    )

    assert (
        configuration.chat_id
        == "123456789"
    )

    assert configuration.enabled is True

    assert (
        configuration.is_configured()
        is True
    )


def test_telegram_configuration_disabled():

    configuration = TelegramConfiguration(
        bot_token="test-bot-token",
        chat_id="123456789",
        enabled=False,
    )

    assert configuration.enabled is False

    assert (
        configuration.is_configured()
        is True
    )


def test_telegram_configuration_missing_token():

    configuration = TelegramConfiguration(
        bot_token="",
        chat_id="123456789",
    )

    assert (
        configuration.is_configured()
        is False
    )


def test_telegram_configuration_missing_chat_id():

    configuration = TelegramConfiguration(
        bot_token="test-bot-token",
        chat_id="",
    )

    assert (
        configuration.is_configured()
        is False
    )


def test_telegram_configuration_whitespace_values():

    configuration = TelegramConfiguration(
        bot_token="   ",
        chat_id="   ",
    )

    assert (
        configuration.is_configured()
        is False
    )