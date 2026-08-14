"""
=================================================
Project Phoenix
Telegram Configuration Loader Tests
M62.1.2 - Telegram Environment Configuration
=================================================
"""

from config.telegram_config_loader import (
    TelegramConfigurationLoader,
)


class FakeConfig:
    """
    Minimal configuration stub used to verify
    that the loader requests environment loading.
    """

    def __init__(self):
        self.load_environment_called = False

    def load_environment(self):
        self.load_environment_called = True


def test_telegram_configuration_loader(
    monkeypatch,
):

    monkeypatch.setenv(
        "TELEGRAM_BOT_TOKEN",
        "test-bot-token",
    )

    monkeypatch.setenv(
        "TELEGRAM_CHAT_ID",
        "123456789",
    )

    monkeypatch.setenv(
        "TELEGRAM_ENABLED",
        "true",
    )

    config = FakeConfig()

    loader = TelegramConfigurationLoader(
        config=config,
    )

    result = loader.load()

    assert (
        config.load_environment_called
        is True
    )

    assert (
        result.bot_token
        == "test-bot-token"
    )

    assert (
        result.chat_id
        == "123456789"
    )

    assert result.enabled is True

    assert (
        result.is_configured()
        is True
    )


def test_telegram_configuration_loader_disabled(
    monkeypatch,
):

    monkeypatch.setenv(
        "TELEGRAM_BOT_TOKEN",
        "test-bot-token",
    )

    monkeypatch.setenv(
        "TELEGRAM_CHAT_ID",
        "123456789",
    )

    monkeypatch.setenv(
        "TELEGRAM_ENABLED",
        "false",
    )

    loader = TelegramConfigurationLoader(
        config=FakeConfig(),
    )

    result = loader.load()

    assert result.enabled is False

    assert (
        result.is_configured()
        is True
    )


def test_telegram_configuration_loader_default_enabled(
    monkeypatch,
):

    monkeypatch.setenv(
        "TELEGRAM_BOT_TOKEN",
        "test-bot-token",
    )

    monkeypatch.setenv(
        "TELEGRAM_CHAT_ID",
        "123456789",
    )

    monkeypatch.delenv(
        "TELEGRAM_ENABLED",
        raising=False,
    )

    loader = TelegramConfigurationLoader(
        config=FakeConfig(),
    )

    result = loader.load()

    assert result.enabled is True


def test_telegram_configuration_loader_missing_values(
    monkeypatch,
):

    monkeypatch.delenv(
        "TELEGRAM_BOT_TOKEN",
        raising=False,
    )

    monkeypatch.delenv(
        "TELEGRAM_CHAT_ID",
        raising=False,
    )

    monkeypatch.delenv(
        "TELEGRAM_ENABLED",
        raising=False,
    )

    loader = TelegramConfigurationLoader(
        config=FakeConfig(),
    )

    result = loader.load()

    assert result.bot_token == ""

    assert result.chat_id == ""

    assert result.enabled is True

    assert (
        result.is_configured()
        is False
    )