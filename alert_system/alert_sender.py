"""
=================================================
Project Phoenix
Alert Sender
M62.1.5 - Telegram-only AlertSender Integration
=================================================

Sends Project Phoenix alerts through Telegram.

Telegram is the only supported alert channel.
"""

from __future__ import annotations

from alert_system.alert_models import (
    AlertMessage,
)

from alert_system.telegram_sender import (
    TelegramSender,
)

from config.telegram_config_loader import (
    TelegramConfigurationLoader,
)


class AlertSender:
    """
    Sends alert notifications through Telegram only.
    """

    TELEGRAM_CHANNEL = "Telegram"

    def __init__(
        self,
        telegram_sender: TelegramSender | None = None,
    ):
        """
        Initialize the Telegram-only alert sender.

        A TelegramSender can optionally be injected
        for testing and controlled integration.
        """

        if telegram_sender is not None:

            self.telegram_sender = (
                telegram_sender
            )

        else:

            configuration = (
                TelegramConfigurationLoader()
                .load()
            )

            self.telegram_sender = (
                TelegramSender(
                    configuration=configuration,
                )
            )

    def send(
        self,
        alert: AlertMessage,
    ) -> list[str]:
        """
        Send an alert through Telegram.

        Returns
        -------
        list[str]
            Names of channels that successfully
            delivered the alert.
        """

        delivered = []

        if self.telegram_sender.send(
            alert
        ):
            delivered.append(
                self.TELEGRAM_CHANNEL
            )

        return delivered