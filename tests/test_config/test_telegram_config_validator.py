"""
=================================================
Project Phoenix
Telegram Configuration Validator Tests
M62.1.3 - Telegram Configuration Validation
=================================================
"""

from config.telegram_config import (
    TelegramConfiguration,
)

from config.telegram_config_validator import (
    TelegramConfigurationValidator,
)


def test_valid_telegram_configuration():

    configuration = TelegramConfiguration(
        bot_token="test-bot-token",
        chat_id="123456789",
        enabled=True,
    )

    assert (
        TelegramConfigurationValidator.validate(
            configuration
        )
        is True
    )


def test_missing_bot_token():

    configuration = TelegramConfiguration(
        bot_token="",
        chat_id="123456789",
        enabled=True,
    )

    assert (
        TelegramConfigurationValidator.validate(
            configuration
        )
        is False
    )


def test_missing_chat_id():

    configuration = TelegramConfiguration(
        bot_token="test-bot-token",
        chat_id="",
        enabled=True,
    )

    assert (
        TelegramConfigurationValidator.validate(
            configuration
        )
        is False
    )


def test_whitespace_bot_token():

    configuration = TelegramConfiguration(
        bot_token="   ",
        chat_id="123456789",
        enabled=True,
    )

    assert (
        TelegramConfigurationValidator.validate(
            configuration
        )
        is False
    )


def test_whitespace_chat_id():

    configuration = TelegramConfiguration(
        bot_token="test-bot-token",
        chat_id="   ",
        enabled=True,
    )

    assert (
        TelegramConfigurationValidator.validate(
            configuration
        )
        is False
    )


def test_invalid_chat_id():

    configuration = TelegramConfiguration(
        bot_token="test-bot-token",
        chat_id="not-a-chat-id",
        enabled=True,
    )

    assert (
        TelegramConfigurationValidator.validate(
            configuration
        )
        is False
    )


def test_negative_chat_id():

    configuration = TelegramConfiguration(
        bot_token="test-bot-token",
        chat_id="-1001234567890",
        enabled=True,
    )

    assert (
        TelegramConfigurationValidator.validate(
            configuration
        )
        is True
    )


def test_disabled_telegram_configuration():

    configuration = TelegramConfiguration(
        bot_token="",
        chat_id="",
        enabled=False,
    )

    assert (
        TelegramConfigurationValidator.validate(
            configuration
        )
        is True
    )