"""
Project Phoenix - Environment Configuration Audit Tests
M62.2.2.3
"""

from config.environment_audit import EnvironmentAudit


def _valid_environment() -> dict[str, str]:
    return {
        "MT5_LOGIN": "12345678",
        "MT5_PASSWORD": "test-password",
        "MT5_SERVER": "TestBroker-Demo",
        "MT5_PATH": r"C:\Program Files\MetaTrader 5\terminal64.exe",
        "TELEGRAM_BOT_TOKEN": "123456789:TEST_TOKEN",
        "TELEGRAM_CHAT_ID": "123456789",
        "TELEGRAM_ENABLED": "true",
    }


def test_valid_environment_is_approved():
    result = EnvironmentAudit(
        _valid_environment()
    ).audit()

    assert result.approved is True
    assert result.errors == ()
    assert result.warnings == ()


def test_empty_environment_is_rejected():
    result = EnvironmentAudit({}).audit()

    assert result.approved is False
    assert len(result.errors) == 5
    assert len(result.warnings) == 1


def test_missing_mt5_login_is_rejected():
    environment = _valid_environment()
    environment.pop("MT5_LOGIN")

    result = EnvironmentAudit(environment).audit()

    assert result.approved is False
    assert "MT5_LOGIN is missing." in result.errors


def test_non_numeric_mt5_login_is_rejected():
    environment = _valid_environment()
    environment["MT5_LOGIN"] = "ABC123"

    result = EnvironmentAudit(environment).audit()

    assert result.approved is False
    assert "MT5_LOGIN must be numeric." in result.errors


def test_non_positive_mt5_login_is_rejected():
    environment = _valid_environment()
    environment["MT5_LOGIN"] = "0"

    result = EnvironmentAudit(environment).audit()

    assert result.approved is False
    assert "MT5_LOGIN must be positive." in result.errors


def test_missing_mt5_password_is_rejected():
    environment = _valid_environment()
    environment.pop("MT5_PASSWORD")

    result = EnvironmentAudit(environment).audit()

    assert result.approved is False
    assert "MT5_PASSWORD is missing." in result.errors


def test_missing_mt5_server_is_rejected():
    environment = _valid_environment()
    environment.pop("MT5_SERVER")

    result = EnvironmentAudit(environment).audit()

    assert result.approved is False
    assert "MT5_SERVER is missing." in result.errors


def test_missing_mt5_path_is_rejected():
    environment = _valid_environment()
    environment.pop("MT5_PATH")

    result = EnvironmentAudit(environment).audit()

    assert result.approved is False
    assert "MT5_PATH is missing." in result.errors


def test_telegram_disabled_does_not_require_telegram_credentials():
    environment = _valid_environment()

    environment["TELEGRAM_ENABLED"] = "false"
    environment.pop("TELEGRAM_BOT_TOKEN")
    environment.pop("TELEGRAM_CHAT_ID")

    result = EnvironmentAudit(environment).audit()

    assert result.approved is True
    assert result.errors == ()
    assert (
        "Telegram alerting is disabled."
        in result.warnings
    )


def test_telegram_enabled_requires_bot_token():
    environment = _valid_environment()
    environment.pop("TELEGRAM_BOT_TOKEN")

    result = EnvironmentAudit(environment).audit()

    assert result.approved is False
    assert (
        "TELEGRAM_BOT_TOKEN is missing."
        in result.errors
    )


def test_telegram_enabled_requires_chat_id():
    environment = _valid_environment()
    environment.pop("TELEGRAM_CHAT_ID")

    result = EnvironmentAudit(environment).audit()

    assert result.approved is False
    assert (
        "TELEGRAM_CHAT_ID is missing."
        in result.errors
    )


def test_invalid_telegram_enabled_value_is_rejected():
    environment = _valid_environment()
    environment["TELEGRAM_ENABLED"] = "yes"

    result = EnvironmentAudit(environment).audit()

    assert result.approved is False
    assert (
        "TELEGRAM_ENABLED must be either 'true' or 'false'."
        in result.errors
    )


def test_telegram_configuration_is_validated():
    environment = _valid_environment()
    environment["TELEGRAM_CHAT_ID"] = "invalid-chat-id"

    result = EnvironmentAudit(environment).audit()

    assert result.approved is False
    assert (
        "Telegram configuration failed validation."
        in result.errors
    )


def test_sensitive_checks_do_not_expose_secret_values():
    environment = _valid_environment()

    result = EnvironmentAudit(environment).audit()

    sensitive_checks = [
        check
        for check in result.checks
        if check.sensitive
    ]

    assert sensitive_checks

    for check in sensitive_checks:
        assert environment["MT5_PASSWORD"] not in check.message
        assert (
            environment["TELEGRAM_BOT_TOKEN"]
            not in check.message
        )


def test_audit_result_counts_are_consistent():
    result = EnvironmentAudit(
        _valid_environment()
    ).audit()

    assert result.passed_checks == len(result.checks)
    assert result.failed_checks == 0


def test_failed_check_counts_are_consistent():
    result = EnvironmentAudit({}).audit()

    assert result.passed_checks == 0
    assert result.failed_checks == len(result.checks)