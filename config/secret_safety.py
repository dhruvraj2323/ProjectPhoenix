"""
Project Phoenix - Secret Safety Utilities
M62.2.5.1
"""

from __future__ import annotations


DEFAULT_MASK = "********"


def mask_secret(
    value: object,
    mask: str = DEFAULT_MASK,
) -> str:
    """
    Return a safe masked representation of a secret.

    Secret values are never returned by this function.
    """

    if value is None:
        return ""

    if value == "":
        return ""

    return mask


def is_sensitive_key(
    key: object,
) -> bool:
    """
    Return True when a configuration key represents
    sensitive credential data.
    """

    if not isinstance(key, str):
        return False

    normalized = key.strip().upper()

    return normalized in {
        "MT5_PASSWORD",
        "TELEGRAM_BOT_TOKEN",
        "PASSWORD",
        "TOKEN",
    }