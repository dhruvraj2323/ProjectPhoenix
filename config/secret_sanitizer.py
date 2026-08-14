"""
Project Phoenix - Configuration Secret Sanitizer
M62.2.5.2
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from config.secret_safety import (
    DEFAULT_MASK,
    is_sensitive_key,
    mask_secret,
)


def sanitize_mapping(
    value: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Return a sanitized copy of a configuration mapping.

    Sensitive values are replaced with a mask.
    Nested mappings and sequences are sanitized recursively.
    """

    sanitized: dict[str, Any] = {}

    for key, item in value.items():
        if is_sensitive_key(key):
            sanitized[key] = mask_secret(item)
        else:
            sanitized[key] = _sanitize_value(item)

    return sanitized


def sanitize_text(
    value: str,
) -> str:
    """
    Sanitize known sensitive key/value patterns in text.

    This function is intentionally conservative. It replaces
    values associated with known sensitive configuration keys.
    """

    if not value:
        return value

    result = value

    sensitive_keys = (
        "MT5_PASSWORD",
        "TELEGRAM_BOT_TOKEN",
        "PASSWORD",
        "TOKEN",
    )

    for key in sensitive_keys:
        result = _mask_key_value(
            result,
            key,
        )

    return result


def _sanitize_value(
    value: Any,
) -> Any:
    """
    Recursively sanitize nested configuration values.
    """

    if isinstance(value, Mapping):
        return sanitize_mapping(value)

    if isinstance(value, list):
        return [
            _sanitize_value(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return tuple(
            _sanitize_value(item)
            for item in value
        )

    return value


def _mask_key_value(
    text: str,
    key: str,
) -> str:
    """
    Mask a simple key=value or key: value representation.

    Only the value portion is replaced.
    """

    separators = (
        "=",
        ":",
    )

    result = text

    for separator in separators:
        marker = f"{key}{separator}"

        start = result.find(marker)

        while start != -1:
            value_start = (
                start + len(marker)
            )

            value_end = _find_value_end(
                result,
                value_start,
            )

            result = (
                result[:value_start]
                + DEFAULT_MASK
                + result[value_end:]
            )

            start = result.find(
                marker,
                value_start + len(DEFAULT_MASK),
            )

    return result


def _find_value_end(
    text: str,
    start: int,
) -> int:
    """
    Find the end of a simple textual configuration value.
    """

    delimiters = (
        " ",
        "\n",
        "\r",
        "\t",
        ",",
        ";",
        "}",
    )

    positions = [
        text.find(
            delimiter,
            start,
        )
        for delimiter in delimiters
    ]

    valid_positions = [
        position
        for position in positions
        if position != -1
    ]

    if not valid_positions:
        return len(text)

    return min(valid_positions)