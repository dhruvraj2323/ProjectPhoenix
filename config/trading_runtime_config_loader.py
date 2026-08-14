"""
Project Phoenix - Trading Runtime Configuration Loader
M62.2.4.2
"""

from __future__ import annotations

import os
from typing import Mapping

from config.trading_runtime_config import (
    TradingRuntimeConfiguration,
)


class TradingRuntimeConfigurationLoader:
    """
    Loads trading runtime configuration from environment variables.

    Environment variables:

        TRADING_ENABLED
        TRADING_MODE

    This loader does not validate the configuration.
    Validation belongs to the validator layer.
    """

    TRADING_ENABLED = "TRADING_ENABLED"
    TRADING_MODE = "TRADING_MODE"

    def __init__(
        self,
        environment: Mapping[str, str] | None = None,
    ) -> None:
        """
        Initialize the loader.

        A custom environment mapping can be supplied
        for deterministic testing.
        """
        self._environment = (
            dict(os.environ)
            if environment is None
            else dict(environment)
        )

    def load(self) -> TradingRuntimeConfiguration:
        """
        Load trading runtime configuration.

        Raw environment values are converted into their
        corresponding model types. Validation of whether
        those values are acceptable belongs to the validator.
        """
        trading_enabled = (
            self._get(self.TRADING_ENABLED)
            .strip()
            .lower()
            == "true"
        )

        trading_mode = (
            self._get(self.TRADING_MODE)
            .strip()
            .upper()
        )

        return TradingRuntimeConfiguration(
            trading_enabled=trading_enabled,
            trading_mode=trading_mode,
        )

    def _get(self, name: str) -> str:
        """
        Return an environment value or an empty string.
        """
        return self._environment.get(
            name,
            "",
        )