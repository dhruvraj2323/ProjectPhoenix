"""
=================================================
Project Phoenix
Telegram Delivery Integration Test
M62.1.6 - Real Telegram Delivery Test
=================================================

Performs one controlled real Telegram delivery
using the local Project Phoenix environment.

Security:
- Credentials are loaded from .env.
- Credentials are never printed.
- Credentials are never hard-coded.
- The test is skipped unless explicitly enabled.
"""

from __future__ import annotations

import os
from datetime import datetime

import pytest

from alert_system.alert_models import (
    AlertMessage,
)

from alert_system.telegram_sender import (
    TelegramSender,
)

from config.telegram_config_loader import (
    TelegramConfigurationLoader,
)


INTEGRATION_FLAG = (
    "PHOENIX_RUN_TELEGRAM_INTEGRATION"
)


def _integration_enabled() -> bool:
    """
    Return True only when real Telegram integration
    testing has been explicitly enabled.
    """

    value = os.getenv(
        INTEGRATION_FLAG,
        "",
    )

    return (
        value.strip().lower()
        in {
            "1",
            "true",
            "yes",
            "on",
        }
    )


def test_real_telegram_delivery():

    if not _integration_enabled():

        pytest.skip(
            "Real Telegram integration test is "
            "disabled. Set "
            f"{INTEGRATION_FLAG}=true "
            "to run it."
        )

    configuration = (
        TelegramConfigurationLoader()
        .load()
    )

    assert (
        configuration.enabled
        is True
    )

    assert (
        configuration.is_configured()
        is True
    )

    sender = TelegramSender(
        configuration=configuration,
    )

    assert (
        sender.is_available()
        is True
    )

    timestamp = (
        datetime.now()
        .strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    alert = AlertMessage(
        title=(
            "Project Phoenix "
            "Telegram Test"
        ),
        message=(
            "M62.1.6 real Telegram "
            f"delivery test successful.\n"
            f"Time: {timestamp}"
        ),
        alert_type="SYSTEM",
        timestamp=timestamp,
    )

    delivered = sender.send(
        alert
    )

    assert delivered is True