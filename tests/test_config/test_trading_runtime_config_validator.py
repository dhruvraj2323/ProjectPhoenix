"""
Project Phoenix - Trading Runtime Configuration Validator Tests
M62.2.4.3
"""

from config.trading_runtime_config import (
    TradingRuntimeConfiguration,
)
from config.trading_runtime_config_validator import (
    TradingRuntimeConfigurationValidator,
)


Validator = TradingRuntimeConfigurationValidator


def test_demo_enabled_configuration_is_valid():
    configuration = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="DEMO",
    )

    assert Validator.validate(configuration) is True


def test_demo_disabled_configuration_is_valid():
    configuration = TradingRuntimeConfiguration(
        trading_enabled=False,
        trading_mode="DEMO",
    )

    assert Validator.validate(configuration) is True


def test_live_enabled_configuration_is_valid():
    configuration = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="LIVE",
    )

    assert Validator.validate(configuration) is True


def test_live_disabled_configuration_is_valid():
    configuration = TradingRuntimeConfiguration(
        trading_enabled=False,
        trading_mode="LIVE",
    )

    assert Validator.validate(configuration) is True


def test_demo_mode_is_valid():
    assert Validator.validate_mode("DEMO") is True


def test_live_mode_is_valid():
    assert Validator.validate_mode("LIVE") is True


def test_unknown_mode_is_invalid():
    assert Validator.validate_mode("PAPER") is False


def test_empty_mode_is_invalid():
    assert Validator.validate_mode("") is False


def test_lowercase_mode_is_invalid():
    assert Validator.validate_mode("demo") is False


def test_execution_enabled_for_enabled_demo():
    configuration = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="DEMO",
    )

    assert (
        Validator.is_execution_enabled(configuration)
        is True
    )


def test_execution_disabled_for_disabled_demo():
    configuration = TradingRuntimeConfiguration(
        trading_enabled=False,
        trading_mode="DEMO",
    )

    assert (
        Validator.is_execution_enabled(configuration)
        is False
    )


def test_execution_enabled_for_enabled_live():
    configuration = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="LIVE",
    )

    assert (
        Validator.is_execution_enabled(configuration)
        is True
    )


def test_execution_disabled_for_disabled_live():
    configuration = TradingRuntimeConfiguration(
        trading_enabled=False,
        trading_mode="LIVE",
    )

    assert (
        Validator.is_execution_enabled(configuration)
        is False
    )


def test_live_execution_requested_when_live_and_enabled():
    configuration = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="LIVE",
    )

    assert (
        Validator.is_live_execution_requested(configuration)
        is True
    )


def test_live_execution_not_requested_when_live_disabled():
    configuration = TradingRuntimeConfiguration(
        trading_enabled=False,
        trading_mode="LIVE",
    )

    assert (
        Validator.is_live_execution_requested(configuration)
        is False
    )


def test_live_execution_not_requested_for_demo():
    configuration = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="DEMO",
    )

    assert (
        Validator.is_live_execution_requested(configuration)
        is False
    )


def test_invalid_mode_cannot_enable_execution():
    configuration = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode="PAPER",
    )

    assert Validator.validate(configuration) is False
    assert (
        Validator.is_execution_enabled(configuration)
        is False
    )
    assert (
        Validator.is_live_execution_requested(configuration)
        is False
    )


def test_invalid_trading_enabled_type_is_rejected():
    configuration = TradingRuntimeConfiguration(
        trading_enabled="true",
        trading_mode="DEMO",
    )

    assert Validator.validate(configuration) is False


def test_invalid_trading_mode_type_is_rejected():
    configuration = TradingRuntimeConfiguration(
        trading_enabled=True,
        trading_mode=None,
    )

    assert Validator.validate(configuration) is False


def test_invalid_configuration_cannot_request_live_execution():
    configuration = TradingRuntimeConfiguration(
        trading_enabled="true",
        trading_mode="LIVE",
    )

    assert (
        Validator.is_live_execution_requested(configuration)
        is False
    )