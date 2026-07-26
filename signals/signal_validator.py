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
        min_confidence: float = 50.0,
    ) -> None:

        if not (0.0 <= min_strength <= 1.0):
            raise ValueError(
                "min_strength must be between 0.0 and 1.0."
            )

        if not (0.0 <= min_confidence <= 100.0):
            raise ValueError(
                "min_confidence must be between 0.0 and 100.0."
            )

        self.min_strength = min_strength
        self.min_confidence = min_confidence

    def validate(self, signal: TradingSignal) -> ValidationResult:
        """
        Validate a trading signal.
        """

        if signal.strength < self.min_strength:
            return ValidationResult(
                valid=False,
                score=0.0,
                reason="Signal strength below minimum threshold.",
            )

        if signal.confidence < self.min_confidence:
            return ValidationResult(
                valid=False,
                score=0.0,
                reason="Signal confidence below minimum threshold.",
            )

        return ValidationResult(
            valid=True,
            score=100.0,
            reason="Signal validation passed.",
        )