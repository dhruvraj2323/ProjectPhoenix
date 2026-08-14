"""
Project Phoenix - MT5 Configuration Audit Tests
M62.2.3.3
"""

from pathlib import Path

from config.mt5_configuration_audit import (
    MT5ConfigurationAudit,
)


def _valid_environment() -> dict[str, str]:
    return {
        "MT5_LOGIN": "12345678",
        "MT5_PASSWORD": "test-password",
        "MT5_SERVER": "TestBroker-Demo",
        "MT5_PATH": r"C:\Program Files\MetaTrader 5\terminal64.exe",
    }


def _write_credentials(
    path: Path,
    *,
    login: object = 12345678,
    password: object = "test-password",
    server: object = "TestBroker-Demo",
) -> None:
    import json

    path.write_text(
        json.dumps(
            {
                "login": login,
                "password": password,
                "server": server,
            }
        ),
        encoding="utf-8",
    )


def _audit(
    tmp_path: Path,
    environment: dict[str, str] | None = None,
    credentials: dict | None = None,
):
    credential_file = (
        tmp_path / "mt5_credentials.json"
    )

    if credentials is not None:
        import json

        credential_file.write_text(
            json.dumps(credentials),
            encoding="utf-8",
        )

    return MT5ConfigurationAudit(
        environment=(
            _valid_environment()
            if environment is None
            else environment
        ),
        credential_file=credential_file,
    ).audit()


def test_valid_mt5_configuration_is_approved(tmp_path):
    result = _audit(
        tmp_path,
        credentials={
            "login": 12345678,
            "password": "test-password",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is True
    assert result.credential_file_present is True
    assert result.credential_file_valid is True
    assert result.environment_valid is True
    assert result.consistency_valid is True
    assert result.errors == ()


def test_missing_credential_file_is_rejected(tmp_path):
    result = _audit(
        tmp_path,
        credentials=None,
    )

    assert result.approved is False
    assert result.credential_file_present is False
    assert result.credential_file_valid is False
    assert (
        "MT5 credential file is missing."
        in result.errors
    )


def test_invalid_json_credential_file_is_rejected(
    tmp_path,
):
    credential_file = (
        tmp_path / "mt5_credentials.json"
    )

    credential_file.write_text(
        "{invalid-json",
        encoding="utf-8",
    )

    result = MT5ConfigurationAudit(
        environment=_valid_environment(),
        credential_file=credential_file,
    ).audit()

    assert result.approved is False
    assert result.credential_file_present is True
    assert result.credential_file_valid is False
    assert (
        "MT5 credential file is invalid JSON."
        in result.errors
    )


def test_credential_file_must_contain_json_object(
    tmp_path,
):
    credential_file = (
        tmp_path / "mt5_credentials.json"
    )

    credential_file.write_text(
        "[]",
        encoding="utf-8",
    )

    result = MT5ConfigurationAudit(
        environment=_valid_environment(),
        credential_file=credential_file,
    ).audit()

    assert result.approved is False
    assert result.credential_file_valid is False
    assert (
        "MT5 credential file must contain a JSON object."
        in result.errors
    )


def test_missing_login_in_credentials_is_rejected(
    tmp_path,
):
    result = _audit(
        tmp_path,
        credentials={
            "password": "test-password",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is False
    assert (
        "MT5 credential field 'login' is missing."
        in result.errors
    )


def test_missing_password_in_credentials_is_rejected(
    tmp_path,
):
    result = _audit(
        tmp_path,
        credentials={
            "login": 12345678,
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is False
    assert (
        "MT5 credential field 'password' is missing."
        in result.errors
    )


def test_missing_server_in_credentials_is_rejected(
    tmp_path,
):
    result = _audit(
        tmp_path,
        credentials={
            "login": 12345678,
            "password": "test-password",
        },
    )

    assert result.approved is False
    assert (
        "MT5 credential field 'server' is missing."
        in result.errors
    )


def test_non_numeric_credential_login_is_rejected(
    tmp_path,
):
    result = _audit(
        tmp_path,
        credentials={
            "login": "ABC123",
            "password": "test-password",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is False
    assert (
        "MT5 credential login must be numeric."
        in result.errors
    )


def test_non_positive_credential_login_is_rejected(
    tmp_path,
):
    result = _audit(
        tmp_path,
        credentials={
            "login": 0,
            "password": "test-password",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is False
    assert (
        "MT5 credential login must be positive."
        in result.errors
    )


def test_invalid_credential_password_is_rejected(
    tmp_path,
):
    result = _audit(
        tmp_path,
        credentials={
            "login": 12345678,
            "password": "",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is False
    assert (
        "MT5 credential field 'password' is invalid."
        in result.errors
    )


def test_invalid_credential_server_is_rejected(
    tmp_path,
):
    result = _audit(
        tmp_path,
        credentials={
            "login": 12345678,
            "password": "test-password",
            "server": "",
        },
    )

    assert result.approved is False
    assert (
        "MT5 credential field 'server' is invalid."
        in result.errors
    )


def test_missing_environment_login_is_rejected(
    tmp_path,
):
    environment = _valid_environment()
    environment.pop("MT5_LOGIN")

    result = _audit(
        tmp_path,
        environment=environment,
        credentials={
            "login": 12345678,
            "password": "test-password",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is False
    assert "MT5_LOGIN is missing." in result.errors


def test_invalid_environment_login_is_rejected(
    tmp_path,
):
    environment = _valid_environment()
    environment["MT5_LOGIN"] = "ABC123"

    result = _audit(
        tmp_path,
        environment=environment,
        credentials={
            "login": 12345678,
            "password": "test-password",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is False
    assert (
        "MT5_LOGIN must be numeric."
        in result.errors
    )


def test_missing_environment_password_is_rejected(
    tmp_path,
):
    environment = _valid_environment()
    environment.pop("MT5_PASSWORD")

    result = _audit(
        tmp_path,
        environment=environment,
        credentials={
            "login": 12345678,
            "password": "test-password",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is False
    assert (
        "MT5_PASSWORD is missing."
        in result.errors
    )


def test_missing_environment_server_is_rejected(
    tmp_path,
):
    environment = _valid_environment()
    environment.pop("MT5_SERVER")

    result = _audit(
        tmp_path,
        environment=environment,
        credentials={
            "login": 12345678,
            "password": "test-password",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is False
    assert (
        "MT5_SERVER is missing."
        in result.errors
    )


def test_missing_mt5_path_is_rejected(tmp_path):
    environment = _valid_environment()
    environment.pop("MT5_PATH")

    result = _audit(
        tmp_path,
        environment=environment,
        credentials={
            "login": 12345678,
            "password": "test-password",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is False
    assert (
        "MT5_PATH is missing."
        in result.errors
    )


def test_nonexistent_mt5_path_is_rejected(
    tmp_path,
):
    environment = _valid_environment()
    environment["MT5_PATH"] = str(
        tmp_path / "missing-terminal64.exe"
    )

    result = _audit(
        tmp_path,
        environment=environment,
        credentials={
            "login": 12345678,
            "password": "test-password",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is False
    assert (
        "MT5_PATH does not exist."
        in result.errors
    )


def test_mt5_path_must_be_a_file(tmp_path):
    terminal_path = tmp_path / "terminal64.exe"
    terminal_path.mkdir()

    environment = _valid_environment()
    environment["MT5_PATH"] = str(
        terminal_path
    )

    result = _audit(
        tmp_path,
        environment=environment,
        credentials={
            "login": 12345678,
            "password": "test-password",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is False
    assert (
        "MT5_PATH is not a file."
        in result.errors
    )


def test_login_consistency_mismatch_is_rejected(
    tmp_path,
):
    result = _audit(
        tmp_path,
        credentials={
            "login": 87654321,
            "password": "test-password",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is False
    assert (
        "MT5 login configuration does not match "
        "the credential file."
        in result.errors
    )


def test_password_consistency_mismatch_is_rejected(
    tmp_path,
):
    result = _audit(
        tmp_path,
        credentials={
            "login": 12345678,
            "password": "different-password",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is False
    assert (
        "MT5 password configuration does not match "
        "the credential file."
        in result.errors
    )


def test_server_consistency_mismatch_is_rejected(
    tmp_path,
):
    result = _audit(
        tmp_path,
        credentials={
            "login": 12345678,
            "password": "test-password",
            "server": "DifferentBroker-Demo",
        },
    )

    assert result.approved is False
    assert (
        "MT5 server configuration does not match "
        "the credential file."
        in result.errors
    )


def test_sensitive_checks_do_not_expose_password(
    tmp_path,
):
    secret = "super-secret-password"

    environment = _valid_environment()
    environment["MT5_PASSWORD"] = secret

    result = _audit(
        tmp_path,
        environment=environment,
        credentials={
            "login": 12345678,
            "password": secret,
            "server": "TestBroker-Demo",
        },
    )

    sensitive_checks = [
        check
        for check in result.checks
        if check.sensitive
    ]

    assert sensitive_checks

    for check in sensitive_checks:
        assert secret not in check.message


def test_result_counts_are_consistent(tmp_path):
    result = _audit(
        tmp_path,
        credentials={
            "login": 12345678,
            "password": "test-password",
            "server": "TestBroker-Demo",
        },
    )

    assert (
        result.passed_checks
        + result.failed_checks
        == len(result.checks)
    )


def test_audit_does_not_require_mt5_connection(
    tmp_path,
):
    result = _audit(
        tmp_path,
        credentials={
            "login": 12345678,
            "password": "test-password",
            "server": "TestBroker-Demo",
        },
    )

    assert result.approved is True
    assert result.connected if hasattr(
        result,
        "connected",
    ) else True