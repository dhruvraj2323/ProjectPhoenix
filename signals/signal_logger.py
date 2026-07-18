"""
Project Phoenix
Milestone M8 - Signal Generation Engine

Module:
    signal_logger.py

Purpose:
    Logs generated trading signals.

Responsibilities:
    - Log signal details
    - Provide a central logging point for the Signal Engine
"""

from __future__ import annotations

from signals.signal_models import TradingSignal


class SignalLogger:
    """
    Simple logger for trading signals.
    """

    def log(self, signal: TradingSignal) -> None:
        """
        Log a trading signal.
        """

        print("===== Trading Signal =====")
        print(f"Signal     : {signal.signal.value}")
        print(f"Strength   : {signal.strength}")
        print(f"Confidence : {signal.confidence}")
        print(f"Reason     : {signal.reason}")