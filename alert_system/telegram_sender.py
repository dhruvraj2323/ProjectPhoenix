"""
=================================================
Project Phoenix
Telegram Sender
M62.1.4 - Telegram Notification Sender
=================================================

Provides Telegram Bot API delivery for Project
Phoenix alert messages.

Security:
- Bot token is supplied through configuration.
- Token is never logged.
- Chat ID is never logged.
- Network failures are handled safely.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from alert_system.alert_models import (
    AlertMessage,
)

from config.telegram_config import (
    TelegramConfiguration,
)

from config.telegram_config_validator import (
    TelegramConfigurationValidator,
)


class TelegramSender:
    """
    Sends AlertMessage objects through the Telegram
    Bot API.
    """

    API_BASE_URL = (
        "https://api.telegram.org/bot"
    )

    SEND_MESSAGE_METHOD = (
        "/sendMessage"
    )

    DEFAULT_TIMEOUT = 10

    def __init__(
        self,
        configuration: TelegramConfiguration,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """
        Initialize Telegram sender.

        Parameters
        ----------
        configuration:
            Telegram notification configuration.

        timeout:
            Network request timeout in seconds.
        """

        self.configuration = configuration

        self.timeout = timeout

    # --------------------------------------------------
    # Configuration
    # --------------------------------------------------

    def is_available(self) -> bool:
        """
        Return True when Telegram delivery is
        enabled and configuration is valid.
        """

        if not self.configuration.enabled:
            return False

        return (
            TelegramConfigurationValidator.validate(
                self.configuration
            )
        )

    # --------------------------------------------------
    # API URL
    # --------------------------------------------------

    def _api_url(self) -> str:
        """
        Build the Telegram sendMessage API URL.

        The token is used internally and is never
        returned through logs or public status data.
        """

        return (
            self.API_BASE_URL
            + self.configuration.bot_token
            + self.SEND_MESSAGE_METHOD
        )

    # --------------------------------------------------
    # Message Payload
    # --------------------------------------------------

    def _payload(
        self,
        alert: AlertMessage,
    ) -> bytes:
        """
        Build the JSON payload for Telegram.
        """

        message_text = (
            f"{alert.title}\n"
            f"{alert.message}"
        )

        payload = {
            "chat_id": (
                self.configuration.chat_id
            ),
            "text": message_text,
        }

        return json.dumps(
            payload
        ).encode("utf-8")

    # --------------------------------------------------
    # Send
    # --------------------------------------------------

    def send(
        self,
        alert: AlertMessage,
    ) -> bool:
        """
        Send an alert through Telegram.

        Returns
        -------
        bool
            True when Telegram confirms successful
            delivery request, otherwise False.
        """

        if not self.is_available():
            return False

        request = urllib.request.Request(
            self._api_url(),
            data=self._payload(alert),
            headers={
                "Content-Type": (
                    "application/json"
                ),
            },
            method="POST",
        )

        try:

            with urllib.request.urlopen(
                request,
                timeout=self.timeout,
            ) as response:

                response_body = (
                    response.read()
                    .decode("utf-8")
                )

            result = json.loads(
                response_body
            )

            return (
                result.get("ok")
                is True
            )

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            OSError,
            json.JSONDecodeError,
        ):

            return False