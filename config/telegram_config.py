"""
=================================================
Project Phoenix
Telegram Configuration
M62.1.1 - Telegram Notification Configuration
=================================================

Defines the configuration model used by the
Telegram notification subsystem.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TelegramConfiguration:
    """
    Stores Telegram notification configuration.

    Secrets are supplied at runtime and are never
    hard-coded in source code.
    """

    bot_token: str

    chat_id: str

    enabled: bool = True

    def is_configured(self) -> bool:
        """
        Return True when required Telegram
        configuration values are available.
        """

        return bool(
            self.bot_token.strip()
            and self.chat_id.strip()
        )