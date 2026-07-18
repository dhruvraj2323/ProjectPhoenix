"""
Project Phoenix
Milestone M8 - Signal Generation Engine

Module:
    signal_filters.py

Purpose:
    Filters trading signals before they are released.

Responsibilities:
    - Apply signal filters
    - Accept or reject signals
"""

from __future__ import annotations

from signals.signal_models import TradingSignal, FilterResult


class SignalFilter:
    """
    Applies basic filtering to trading signals.
    """

    def filter(self, signal: TradingSignal) -> FilterResult:
        """
        Apply signal filters.

        Returns:
            FilterResult
        """

        if signal.signal.name == "HOLD":
            return FilterResult(
                accepted=False,
                reason="HOLD signals are filtered."
            )

        return FilterResult(
            accepted=True,
            reason="Signal accepted."
        )