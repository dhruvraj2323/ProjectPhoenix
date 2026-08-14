"""
Project Phoenix - Secret Safety Tests
M62.2.5.3
"""

from config.secret_safety import (
    DEFAULT_MASK,
    is_sensitive_key,
    mask_secret,
)
from config.secret_sanitizer import (
    sanitize_mapping,
    sanitize_text,
)


def test_mask_secret_returns_default_mask():
    secret = "super-secret"

    result = mask_secret(secret)

    assert result == DEFAULT_MASK
    assert secret not in result


def test_mask_secret_does_not_expose_secret():
    secret = "123456789:REAL_TOKEN"

    result = mask_secret(secret)

    assert result == "********"
    assert secret not in result


def test_mask_secret_supports_custom_mask():
    secret = "super-secret"

    result = mask_secret(
        secret,
        mask="[REDACTED]",
    )

    assert result == "[REDACTED]"
    assert secret not in result


def test_none_secret_returns_empty_string():
    assert mask_secret(None) == ""


def test_empty_secret_returns_empty_string():
    assert mask_secret("") == ""


def test_mt5_password_is_sensitive():
    assert (
        is_sensitive_key("MT5_PASSWORD")
        is True
    )


def test_telegram_bot_token_is_sensitive():
    assert (
        is_sensitive_key("TELEGRAM_BOT_TOKEN")
        is True
    )


def test_generic_password_is_sensitive():
    assert (
        is_sensitive_key("PASSWORD")
        is True
    )


def test_generic_token_is_sensitive():
    assert (
        is_sensitive_key("TOKEN")
        is True
    )


def test_non_sensitive_mt5_login():
    assert (
        is_sensitive_key("MT5_LOGIN")
        is False
    )


def test_non_sensitive_mt5_server():
    assert (
        is_sensitive_key("MT5_SERVER")
        is False
    )


def test_non_sensitive_mt5_path():
    assert (
        is_sensitive_key("MT5_PATH")
        is False
    )


def test_sensitive_key_detection_is_case_insensitive():
    assert (
        is_sensitive_key("mt5_password")
        is True
    )

    assert (
        is_sensitive_key("telegram_bot_token")
        is True
    )


def test_sanitize_mapping_masks_mt5_password():
    secret = "real-mt5-password"

    result = sanitize_mapping(
        {
            "MT5_PASSWORD": secret,
        }
    )

    assert result["MT5_PASSWORD"] == DEFAULT_MASK
    assert secret not in str(result)


def test_sanitize_mapping_masks_telegram_token():
    secret = "real-telegram-token"

    result = sanitize_mapping(
        {
            "TELEGRAM_BOT_TOKEN": secret,
        }
    )

    assert (
        result["TELEGRAM_BOT_TOKEN"]
        == DEFAULT_MASK
    )
    assert secret not in str(result)


def test_sanitize_mapping_preserves_non_sensitive_values():
    result = sanitize_mapping(
        {
            "MT5_LOGIN": "12345678",
            "MT5_SERVER": "DemoServer",
            "MT5_PATH": r"C:\MT5\terminal64.exe",
        }
    )

    assert result["MT5_LOGIN"] == "12345678"
    assert result["MT5_SERVER"] == "DemoServer"
    assert (
        result["MT5_PATH"]
        == r"C:\MT5\terminal64.exe"
    )


def test_sanitize_mapping_handles_nested_mapping():
    secret = "nested-secret"

    result = sanitize_mapping(
        {
            "database": {
                "password": secret,
            }
        }
    )

    assert (
        result["database"]["password"]
        == DEFAULT_MASK
    )
    assert secret not in str(result)


def test_sanitize_mapping_handles_nested_list():
    secret = "list-secret"

    result = sanitize_mapping(
        {
            "credentials": [
                {
                    "password": secret,
                }
            ]
        }
    )

    assert (
        result["credentials"][0]["password"]
        == DEFAULT_MASK
    )
    assert secret not in str(result)


def test_sanitize_mapping_handles_nested_tuple():
    secret = "tuple-secret"

    result = sanitize_mapping(
        {
            "credentials": (
                {
                    "token": secret,
                },
            )
        }
    )

    assert (
        result["credentials"][0]["token"]
        == DEFAULT_MASK
    )
    assert secret not in str(result)


def test_sanitize_text_masks_mt5_password():
    secret = "real-mt5-password"

    text = (
        f"MT5_PASSWORD={secret}"
    )

    result = sanitize_text(text)

    assert (
        "MT5_PASSWORD=********"
        in result
    )
    assert secret not in result


def test_sanitize_text_masks_telegram_token():
    secret = "real-telegram-token"

    text = (
        f"TELEGRAM_BOT_TOKEN={secret}"
    )

    result = sanitize_text(text)

    assert (
        "TELEGRAM_BOT_TOKEN=********"
        in result
    )
    assert secret not in result


def test_sanitize_text_masks_multiple_secrets():
    password = "real-password"
    token = "real-token"

    text = (
        f"MT5_PASSWORD={password} "
        f"TELEGRAM_BOT_TOKEN={token}"
    )

    result = sanitize_text(text)

    assert password not in result
    assert token not in result
    assert (
        "MT5_PASSWORD=********"
        in result
    )
    assert (
        "TELEGRAM_BOT_TOKEN=********"
        in result
    )


def test_sanitize_text_preserves_non_sensitive_text():
    text = (
        "MT5_LOGIN=12345678 "
        "MT5_SERVER=DemoServer"
    )

    result = sanitize_text(text)

    assert result == text


def test_sanitize_text_handles_empty_text():
    assert sanitize_text("") == ""


def test_original_mapping_is_not_modified():
    secret = "original-secret"

    source = {
        "MT5_PASSWORD": secret,
    }

    result = sanitize_mapping(source)

    assert (
        source["MT5_PASSWORD"]
        == secret
    )

    assert (
        result["MT5_PASSWORD"]
        == DEFAULT_MASK
    )


def test_secret_values_are_not_present_in_sanitized_output():
    mt5_password = "unique-mt5-secret-123"
    telegram_token = "unique-telegram-secret-456"

    source = {
        "MT5_PASSWORD": mt5_password,
        "TELEGRAM_BOT_TOKEN": telegram_token,
        "nested": {
            "password": mt5_password,
            "token": telegram_token,
        },
    }

    result = sanitize_mapping(source)
    output = str(result)

    assert mt5_password not in output
    assert telegram_token not in output