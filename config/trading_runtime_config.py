"""
Project Phoenix - Trading Runtime Configuration
M62.2.4.1
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TradingRuntimeConfiguration:
    """
    Represents the runtime trading configuration.

    This model contains configuration state only.
    It does not connect to MT5 or execute trades.
    """

    trading_enabled: bool
    trading_mode: str

    def is_demo(self) -> bool:
        """Return True when runtime mode is DEMO."""
        return self.trading_mode == "DEMO"

    def is_live(self) -> bool:
        """Return True when runtime mode is LIVE."""
        return self.trading_mode == "LIVE"

    def execution_enabled(self) -> bool:
        """
        Return whether trading execution is enabled.

        This only reflects the runtime configuration.
        It does not grant deployment or live-trading approval.
        """
        return self.trading_enabled