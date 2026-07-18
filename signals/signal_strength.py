"""
Project Phoenix
Milestone M8 - Signal Generation Engine

Module:
    signal_strength.py

Purpose:
    Calculates overall signal strength from rule results.
"""

from __future__ import annotations

from typing import List

from signals.signal_models import RuleResult


class SignalStrengthCalculator:
    """
    Calculates overall signal strength.
    """

    def calculate(self, rules: List[RuleResult]) -> float:
        """
        Returns average strength of all passed rules.

        Returns:
            float
        """

        passed_rules = [rule for rule in rules if rule.passed]

        if not passed_rules:
            return 0.0

        total_strength = sum(rule.strength for rule in passed_rules)

        return total_strength / len(passed_rules)