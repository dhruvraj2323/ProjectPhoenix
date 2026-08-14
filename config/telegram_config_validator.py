"""
=================================================
Project Phoenix
Telegram Configuration Validator
M62.1.3 - Telegram Configuration Validation
=================================================

Validates Telegram notification configuration
before the Telegram sender is allowed to use it.
"""

from __future__ import annotations

from config.telegram_config import (
    TelegramConfiguration,
)


class TelegramConfigurationValidator:
    """
    Validates TelegramConfiguration instances.
    """

    @staticmethod
    def validate(
        configuration: TelegramConfiguration,
    ) -> bool:
        """
        Return True when the Telegram configuration
        contains valid required values.

        A disabled Telegram configuration is treated
        as valid because delivery has intentionally
        been disabled.
        """

        if not configuration.enabled:
            return True

        if not configuration.bot_token.strip():
            return False

        if not configuration.chat_id.strip():
            return False

        if not (
            TelegramConfigurationValidator
            ._valid_chat_id(
                configuration.chat_id
            )
        ):
            return False

        return True

    @staticmethod
    def _valid_chat_id(
        chat_id: str,
    ) -> bool:
        """
        Validate Telegram chat ID format.

        Telegram chat IDs are numeric. Negative IDs
        are allowed for group/supergroup chats.
        """

        value = chat_id.strip()

        if not value:
            return False

        if value.startswith("-"):
            value = value[1:]

        return (
            value.isdigit()
            and len(value) > 0
        )