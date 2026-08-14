"""
=================================================
Project Phoenix
Telegram Configuration Loader
M62.1.2 - Telegram Environment Configuration
=================================================

Loads Telegram notification configuration from
the Project Phoenix environment.

Secrets are never hard-coded in source code.
"""

from __future__ import annotations

import os

from core.config import Config

from config.telegram_config import (
    TelegramConfiguration,
)


class TelegramConfigurationLoader:
    """
    Loads Telegram configuration from environment
    variables.
    """

    BOT_TOKEN_KEY = "TELEGRAM_BOT_TOKEN"

    CHAT_ID_KEY = "TELEGRAM_CHAT_ID"

    ENABLED_KEY = "TELEGRAM_ENABLED"

    def __init__(
        self,
        config: Config | None = None,
    ):
        """
        Initialize Telegram configuration loader.
        """

        self.config = (
            config
            if config is not None
            else Config()
        )

    def load(
        self,
    ) -> TelegramConfiguration:
        """
        Load Telegram configuration from the
        Project Phoenix environment.
        """

        self.config.load_environment()

        bot_token = os.getenv(
            self.BOT_TOKEN_KEY,
            "",
        )

        chat_id = os.getenv(
            self.CHAT_ID_KEY,
            "",
        )

        enabled_value = os.getenv(
            self.ENABLED_KEY,
            "true",
        )

        enabled = (
            enabled_value.strip().lower()
            in {
                "1",
                "true",
                "yes",
                "on",
            }
        )

        return TelegramConfiguration(
            bot_token=bot_token,
            chat_id=chat_id,
            enabled=enabled,
        )