"""
Project Phoenix - Trading Runtime Configuration Validator
M62.2.4.3
"""

from __future__ import annotations

from config.trading_runtime_config import (
    TradingRuntimeConfiguration,
)


class TradingRuntimeConfigurationValidator:
    """
    Validates trading runtime configuration.

    This validator checks configuration correctness only.

    It does not:
        - connect to MT5
        - authenticate an account
        - approve live trading
        - execute trades
    """

    VALID_MODES = frozenset(
        {
            "DEMO",
            "LIVE",
        }
    )

    @classmethod
    def validate(
        cls,
        configuration: TradingRuntimeConfiguration,
    ) -> bool:
        """
        Return True when the runtime configuration is valid.
        """
        return (
            isinstance(
                configuration.trading_enabled,
                bool,
            )
            and cls.validate_mode(
                configuration.trading_mode
            )
        )

    @classmethod
    def validate_mode(
        cls,
        trading_mode: str,
    ) -> bool:
        """
        Validate the configured trading mode.
        """
        return (
            isinstance(trading_mode, str)
            and trading_mode in cls.VALID_MODES
        )

    @classmethod
    def is_execution_enabled(
        cls,
        configuration: TradingRuntimeConfiguration,
    ) -> bool:
        """
        Return whether runtime execution is enabled.

        This does not represent deployment approval
        or live-trading authorization.
        """
        if not cls.validate(configuration):
            return False

        return configuration.trading_enabled

    @classmethod
    def is_live_execution_requested(
        cls,
        configuration: TradingRuntimeConfiguration,
    ) -> bool:
        """
        Return True when LIVE mode and execution are both requested.

        This is only a configuration state.

        It does not grant live-trading approval.
        """
        return (
            cls.validate(configuration)
            and configuration.trading_mode == "LIVE"
            and configuration.trading_enabled
        )