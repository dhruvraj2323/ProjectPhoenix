"""
Project Phoenix - Configuration Readiness Gate
M62.2.6.2
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from config.configuration_readiness_models import (
    ConfigurationReadinessCheck,
    ConfigurationReadinessResult,
)
from config.environment_audit import EnvironmentAudit
from config.mt5_configuration_audit import (
    MT5ConfigurationAudit,
)
from config.trading_runtime_config import (
    TradingRuntimeConfiguration,
)
from config.trading_runtime_config_validator import (
    TradingRuntimeConfigurationValidator,
)


class ConfigurationReadinessGate:
    """
    Aggregate configuration readiness checks.

    This gate evaluates configuration readiness only.

    It does not:
        - connect to MT5
        - authenticate an MT5 account
        - approve live trading
        - execute trades
    """

    def __init__(
        self,
        environment: Mapping[str, str] | None = None,
        credential_file: str | None = None,
        runtime_configuration: (
            TradingRuntimeConfiguration | None
        ) = None,
        secrets_safe: bool = True,
    ) -> None:
        """
        Initialize the configuration readiness gate.

        A custom environment and credential file can be
        supplied for deterministic testing.

        runtime_configuration is supplied as an already
        loaded configuration object. The gate validates
        it but does not load or mutate it.
        """
        self._environment = (
            None
            if environment is None
            else dict(environment)
        )

        self._credential_file = credential_file

        self._runtime_configuration = (
            runtime_configuration
        )

        self._secrets_safe = secrets_safe

    def evaluate(self) -> ConfigurationReadinessResult:
        """
        Evaluate complete configuration readiness.
        """
        checks: list[
            ConfigurationReadinessCheck
        ] = []

        errors: list[str] = []
        warnings: list[str] = []

        environment_result = (
            EnvironmentAudit(
                self._environment
            ).audit()
        )

        environment_ready = (
            environment_result.approved
        )

        checks.append(
            ConfigurationReadinessCheck(
                name="ENVIRONMENT",
                passed=environment_ready,
                required=True,
                message=(
                    "Environment configuration "
                    "is ready."
                    if environment_ready
                    else
                    "Environment configuration "
                    "is not ready."
                ),
            )
        )

        errors.extend(
            environment_result.errors
        )
        warnings.extend(
            environment_result.warnings
        )

        mt5_result = (
            MT5ConfigurationAudit(
                environment=self._environment,
                credential_file=(
                    self._credential_file
                ),
            ).audit()
        )

        mt5_ready = mt5_result.approved

        checks.append(
            ConfigurationReadinessCheck(
                name="MT5",
                passed=mt5_ready,
                required=True,
                message=(
                    "MT5 configuration is ready."
                    if mt5_ready
                    else
                    "MT5 configuration is not ready."
                ),
            )
        )

        errors.extend(
            mt5_result.errors
        )
        warnings.extend(
            mt5_result.warnings
        )

        runtime_ready = (
            self._runtime_configuration
            is not None
            and TradingRuntimeConfigurationValidator.validate(
                self._runtime_configuration
            )
        )

        checks.append(
            ConfigurationReadinessCheck(
                name="TRADING_RUNTIME",
                passed=runtime_ready,
                required=True,
                message=(
                    "Trading runtime configuration "
                    "is ready."
                    if runtime_ready
                    else
                    "Trading runtime configuration "
                    "is not ready."
                ),
            )
        )

        if not runtime_ready:
            errors.append(
                "Trading runtime configuration "
                "is not valid."
            )

        checks.append(
            ConfigurationReadinessCheck(
                name="SECRET_SAFETY",
                passed=self._secrets_safe,
                required=True,
                message=(
                    "Configuration secrets are safe."
                    if self._secrets_safe
                    else
                    "Configuration secret safety "
                    "check failed."
                ),
            )
        )

        if not self._secrets_safe:
            errors.append(
                "Configuration secret safety "
                "check failed."
            )

        ready = (
            environment_ready
            and mt5_ready
            and runtime_ready
            and self._secrets_safe
        )

        return ConfigurationReadinessResult(
            ready=ready,
            environment_ready=environment_ready,
            mt5_ready=mt5_ready,
            runtime_ready=runtime_ready,
            secrets_safe=self._secrets_safe,
            checks=tuple(checks),
            errors=tuple(errors),
            warnings=tuple(warnings),
        )