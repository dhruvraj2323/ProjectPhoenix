"""
Project Phoenix - Configuration Readiness Gate Tests
M62.2.6.3
"""

import json
from pathlib import Path

from config.configuration_readiness_gate import (
    ConfigurationReadinessGate,
)
from config.trading_runtime_config import (
    TradingRuntimeConfiguration,
)


def _valid_environment(
    mt5_path: str,
) -> dict[str, str]:
    return {
        "MT5_LOGIN": "12345678",
        "MT5_PASSWORD": "test-password",
        "MT5_SERVER": "TestBroker-Demo",
        "MT5_PATH": mt5_path,
        "TELEGRAM_ENABLED": "false",
    }


def _write_credentials(
    path: Path,
    *,
    login: int = 12345678,
    password: str = "test-password",
    server: str = "TestBroker-Demo",
) -> None:
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


def _create_ready_inputs(
    tmp_path: Path,
) -> tuple[dict[str, str], Path]:
    terminal_path = (
        tmp_path / "terminal64.exe"
    )
    terminal_path.write_text(
        "test-terminal",
        encoding="utf-8",
    )

    credential_file = (
        tmp_path / "mt5_credentials.json"
    )

    _write_credentials(
        credential_file
    )

    return (
        _valid_environment(
            str(terminal_path)
        ),
        credential_file,
    )


def test_valid_demo_configuration_is_ready(
    tmp_path,
):
    environment, credential_file = (
        _create_ready_inputs(tmp_path)
    )

    runtime = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="DEMO",
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            credential_file
        ),
        runtime_configuration=runtime,
    ).evaluate()

    assert result.ready is True
    assert result.environment_ready is True
    assert result.mt5_ready is True
    assert result.runtime_ready is True
    assert result.secrets_safe is True
    assert result.errors == ()


def test_valid_live_configuration_is_ready(
    tmp_path,
):
    environment, credential_file = (
        _create_ready_inputs(tmp_path)
    )

    runtime = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="LIVE",
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            credential_file
        ),
        runtime_configuration=runtime,
    ).evaluate()

    assert result.ready is True
    assert result.environment_ready is True
    assert result.mt5_ready is True
    assert result.runtime_ready is True


def test_live_configuration_does_not_mean_live_approval(
    tmp_path,
):
    environment, credential_file = (
        _create_ready_inputs(tmp_path)
    )

    runtime = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="LIVE",
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            credential_file
        ),
        runtime_configuration=runtime,
    ).evaluate()

    assert result.ready is True

    assert not hasattr(
        result,
        "live_approved",
    )


def test_environment_failure_makes_gate_not_ready(
    tmp_path,
):
    environment, credential_file = (
        _create_ready_inputs(tmp_path)
    )

    environment.pop("MT5_LOGIN")

    runtime = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="DEMO",
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            credential_file
        ),
        runtime_configuration=runtime,
    ).evaluate()

    assert result.ready is False
    assert result.environment_ready is False
    assert result.mt5_ready is False
    assert result.runtime_ready is True


def test_mt5_failure_makes_gate_not_ready(
    tmp_path,
):
    environment, credential_file = (
        _create_ready_inputs(tmp_path)
    )

    environment["MT5_SERVER"] = (
        "DifferentBroker-Demo"
    )

    runtime = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="DEMO",
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            credential_file
        ),
        runtime_configuration=runtime,
    ).evaluate()

    assert result.ready is False
    assert result.mt5_ready is False


def test_missing_credential_file_makes_gate_not_ready(
    tmp_path,
):
    environment, _ = (
        _create_ready_inputs(tmp_path)
    )

    missing_file = (
        tmp_path
        / "missing_credentials.json"
    )

    runtime = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="DEMO",
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            missing_file
        ),
        runtime_configuration=runtime,
    ).evaluate()

    assert result.ready is False
    assert result.mt5_ready is False


def test_runtime_failure_makes_gate_not_ready(
    tmp_path,
):
    environment, credential_file = (
        _create_ready_inputs(tmp_path)
    )

    runtime = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="PAPER",
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            credential_file
        ),
        runtime_configuration=runtime,
    ).evaluate()

    assert result.ready is False
    assert result.environment_ready is True
    assert result.mt5_ready is True
    assert result.runtime_ready is False
    assert (
        "Trading runtime configuration "
        "is not valid."
        in result.errors
    )


def test_missing_runtime_configuration_is_not_ready(
    tmp_path,
):
    environment, credential_file = (
        _create_ready_inputs(tmp_path)
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            credential_file
        ),
        runtime_configuration=None,
    ).evaluate()

    assert result.ready is False
    assert result.runtime_ready is False


def test_secret_safety_failure_makes_gate_not_ready(
    tmp_path,
):
    environment, credential_file = (
        _create_ready_inputs(tmp_path)
    )

    runtime = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="DEMO",
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            credential_file
        ),
        runtime_configuration=runtime,
        secrets_safe=False,
    ).evaluate()

    assert result.ready is False
    assert result.environment_ready is True
    assert result.mt5_ready is True
    assert result.runtime_ready is True
    assert result.secrets_safe is False
    assert (
        "Configuration secret safety "
        "check failed."
        in result.errors
    )


def test_multiple_failures_are_aggregated(
    tmp_path,
):
    environment, _ = (
        _create_ready_inputs(tmp_path)
    )

    environment.pop("MT5_LOGIN")

    runtime = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="PAPER",
    )

    missing_file = (
        tmp_path
        / "missing_credentials.json"
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            missing_file
        ),
        runtime_configuration=runtime,
        secrets_safe=False,
    ).evaluate()

    assert result.ready is False
    assert result.environment_ready is False
    assert result.mt5_ready is False
    assert result.runtime_ready is False
    assert result.secrets_safe is False
    assert len(result.errors) >= 4


def test_disabled_demo_runtime_can_be_ready(
    tmp_path,
):
    environment, credential_file = (
        _create_ready_inputs(tmp_path)
    )

    runtime = TradingRuntimeConfiguration(
        trading_enabled=False,
        trading_mode="DEMO",
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            credential_file
        ),
        runtime_configuration=runtime,
    ).evaluate()

    assert result.ready is True
    assert result.runtime_ready is True


def test_disabled_live_runtime_can_be_ready(
    tmp_path,
):
    environment, credential_file = (
        _create_ready_inputs(tmp_path)
    )

    runtime = TradingRuntimeConfiguration(
        trading_enabled=False,
        trading_mode="LIVE",
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            credential_file
        ),
        runtime_configuration=runtime,
    ).evaluate()

    assert result.ready is True
    assert result.runtime_ready is True


def test_readiness_check_summary_is_complete(
    tmp_path,
):
    environment, credential_file = (
        _create_ready_inputs(tmp_path)
    )

    runtime = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="DEMO",
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            credential_file
        ),
        runtime_configuration=runtime,
    ).evaluate()

    check_names = {
        check.name
        for check in result.checks
    }

    assert check_names == {
        "ENVIRONMENT",
        "MT5",
        "TRADING_RUNTIME",
        "SECRET_SAFETY",
    }


def test_passed_and_failed_counts_are_consistent(
    tmp_path,
):
    environment, credential_file = (
        _create_ready_inputs(tmp_path)
    )

    runtime = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="DEMO",
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            credential_file
        ),
        runtime_configuration=runtime,
    ).evaluate()

    assert (
        result.passed_checks
        + result.failed_checks
        == len(result.checks)
    )


def test_gate_does_not_expose_credentials(
    tmp_path,
):
    environment, credential_file = (
        _create_ready_inputs(tmp_path)
    )

    secret_password = "unique-secret-password"

    environment["MT5_PASSWORD"] = (
        secret_password
    )

    runtime = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="DEMO",
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            credential_file
        ),
        runtime_configuration=runtime,
    ).evaluate()

    output = str(result)

    assert secret_password not in output


def test_gate_does_not_require_mt5_connection(
    tmp_path,
):
    environment, credential_file = (
        _create_ready_inputs(tmp_path)
    )

    runtime = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="DEMO",
    )

    result = ConfigurationReadinessGate(
        environment=environment,
        credential_file=str(
            credential_file
        ),
        runtime_configuration=runtime,
    ).evaluate()

    assert result.ready is True

    assert not hasattr(
        result,
        "connected",
    )