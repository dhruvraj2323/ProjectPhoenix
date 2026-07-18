"""
Project Phoenix
Milestone M8 - Signal Generation Engine

Module:
    signal_validator.py

Purpose:
    Validates generated trading signals before they are released.

Responsibilities:
    - Validate signal strength
    - Validate confidence
    - Return ValidationResult
"""

from __future__ import annotations

from signals.signal_models import TradingSignal, ValidationResult


class SignalValidator:
    """
    Validates TradingSignal objects.
    """

    def __init__(
        self,
        min_strength: float = 0.50,
        min_confidence: float = 0.50,
    ):
        self.min_strength = min_strength
        self.min_confidence = min_confidence

    def validate(self, signal: TradingSignal) -> ValidationResult:
        """
        Validate a trading signal.
        """

        if signal.strength < self.min_strength:
            return ValidationResult(
                valid=False,
                reason="Signal strength below minimum threshold."
            )

        if signal.confidence < self.min_confidence:
            return ValidationResult(
                valid=False,
                reason="Signal confidence below minimum threshold."
            )

        return ValidationResult(
            valid=True,
            reason="Signal validation passed."
        )