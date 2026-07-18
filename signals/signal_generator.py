"""
Project Phoenix
Milestone M8 - Signal Generation Engine

Module:
    signal_generator.py

Purpose:
    Coordinates all Signal Engine modules.

Responsibilities:
    - Generate trading signals
    - Validate signals
    - Filter signals
    - Log signals
"""

from __future__ import annotations

from signals.signal_models import TradingSignal, SignalType
from signals.signal_validator import SignalValidator
from signals.signal_filters import SignalFilter
from signals.signal_logger import SignalLogger


class SignalGenerator:
    """
    Main Signal Generation Engine.
    """

    def __init__(self) -> None:
        self.validator = SignalValidator()
        self.filter = SignalFilter()
        self.logger = SignalLogger()

    def generate(self) -> TradingSignal:
        """
        Generate a trading signal.
        """

        signal = TradingSignal(
            signal=SignalType.BUY,
            strength=0.80,
            confidence=0.90,
            reason="Initial M8 placeholder signal."
        )

        validation = self.validator.validate(signal)

        if not validation.valid:
            raise ValueError(validation.reason)

        filtered = self.filter.filter(signal)

        if not filtered.accepted:
            raise ValueError(filtered.reason)

        self.logger.log(signal)

        return signal