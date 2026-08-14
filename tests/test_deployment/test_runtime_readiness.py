"""
Project Phoenix - Runtime Readiness Adapter Tests
M62.3.1
"""

from config.configuration_readiness_models import (
    ConfigurationReadinessCheck,
    ConfigurationReadinessResult,
)
from deployment.runtime_readiness import (
    RuntimeReadinessAdapter,
)


def _ready_result() -> ConfigurationReadinessResult:
    return ConfigurationReadinessResult(
        ready=True,
        environment_ready=True,
        mt5_ready=True,
        runtime_ready=True,
        secrets_safe=True,
        checks=(
            ConfigurationReadinessCheck(
                name="ENVIRONMENT",
                passed=True,
                required=True,
                message="Environment configuration is ready.",
            ),
            ConfigurationReadinessCheck(
                name="MT5",
                passed=True,
                required=True,
                message="MT5 configuration is ready.",
            ),
            ConfigurationReadinessCheck(
                name="TRADING_RUNTIME",
                passed=True,
                required=True,
                message="Trading runtime configuration is ready.",
            ),
            ConfigurationReadinessCheck(
                name="SECRET_SAFETY",
                passed=True,
                required=True,
                message="Configuration secrets are safe.",
            ),
        ),
    )


def _not_ready_result() -> ConfigurationReadinessResult:
    return ConfigurationReadinessResult(
        ready=False,
        environment_ready=False,
        mt5_ready=True,
        runtime_ready=True,
        secrets_safe=True,
        checks=(
            ConfigurationReadinessCheck(
                name="ENVIRONMENT",
                passed=False,
                required=True,
                message="Environment configuration is not ready.",
            ),
        ),
        errors=(
            "Environment configuration is not ready.",
        ),
    )


def test_ready_configuration_is_adapted_to_runtime_ready():
    result = _ready_result()

    readiness = RuntimeReadinessAdapter.evaluate(
        result
    )

    assert readiness.ready is True
    assert readiness.configuration_ready is True
    assert (
        readiness.reason
        == "Runtime configuration is ready."
    )


def test_not_ready_configuration_is_adapted_to_runtime_not_ready():
    result = _not_ready_result()

    readiness = RuntimeReadinessAdapter.evaluate(
        result
    )

    assert readiness.ready is False
    assert readiness.configuration_ready is False
    assert (
        readiness.reason
        == "Runtime configuration is not ready."
    )


def test_adapter_preserves_original_configuration_result():
    result = _ready_result()

    readiness = RuntimeReadinessAdapter.evaluate(
        result
    )

    assert readiness.configuration_result is result


def test_not_ready_adapter_preserves_original_result():
    result = _not_ready_result()

    readiness = RuntimeReadinessAdapter.evaluate(
        result
    )

    assert readiness.configuration_result is result


def test_ready_state_matches_configuration_result():
    result = _ready_result()

    readiness = RuntimeReadinessAdapter.evaluate(
        result
    )

    assert (
        readiness.ready
        == result.ready
    )

    assert (
        readiness.configuration_ready
        == result.ready
    )


def test_not_ready_state_matches_configuration_result():
    result = _not_ready_result()

    readiness = RuntimeReadinessAdapter.evaluate(
        result
    )

    assert (
        readiness.ready
        == result.ready
    )

    assert (
        readiness.configuration_ready
        == result.ready
    )


def test_adapter_does_not_change_configuration_result():
    result = _ready_result()

    original_checks = result.checks
    original_errors = result.errors
    original_warnings = result.warnings

    RuntimeReadinessAdapter.evaluate(
        result
    )

    assert result.checks == original_checks
    assert result.errors == original_errors
    assert result.warnings == original_warnings


def test_adapter_does_not_create_live_approval():
    result = _ready_result()

    readiness = RuntimeReadinessAdapter.evaluate(
        result
    )

    assert not hasattr(
        readiness,
        "live_approved",
    )


def test_adapter_does_not_report_mt5_connection():
    result = _ready_result()

    readiness = RuntimeReadinessAdapter.evaluate(
        result
    )

    assert not hasattr(
        readiness,
        "connected",
    )


def test_adapter_does_not_report_trade_execution():
    result = _ready_result()

    readiness = RuntimeReadinessAdapter.evaluate(
        result
    )

    assert not hasattr(
        readiness,
        "trade_executed",
    )


def test_ready_result_with_warnings_remains_ready():
    result = ConfigurationReadinessResult(
        ready=True,
        environment_ready=True,
        mt5_ready=True,
        runtime_ready=True,
        secrets_safe=True,
        warnings=(
            "Non-critical configuration warning.",
        ),
    )

    readiness = RuntimeReadinessAdapter.evaluate(
        result
    )

    assert readiness.ready is True
    assert readiness.configuration_ready is True


def test_failed_configuration_remains_not_ready_even_with_other_checks_passed():
    result = ConfigurationReadinessResult(
        ready=False,
        environment_ready=True,
        mt5_ready=True,
        runtime_ready=False,
        secrets_safe=True,
        errors=(
            "Trading runtime configuration is not valid.",
        ),
    )

    readiness = RuntimeReadinessAdapter.evaluate(
        result
    )

    assert readiness.ready is False
    assert readiness.configuration_ready is False


def test_adapter_evaluation_is_deterministic():
    result = _ready_result()

    first = RuntimeReadinessAdapter.evaluate(
        result
    )
    second = RuntimeReadinessAdapter.evaluate(
        result
    )

    assert first == second


def test_adapter_does_not_require_external_connection():
    result = _ready_result()

    readiness = RuntimeReadinessAdapter.evaluate(
        result
    )

    assert readiness.ready is True