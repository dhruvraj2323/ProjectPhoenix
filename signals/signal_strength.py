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
    Calculates the overall signal strength from trading rule results.
    """

    def calculate(self, rules: List[RuleResult]) -> float:
        """
        Calculate the average strength of all passed rules.

        Args:
            rules:
                List of RuleResult objects.

        Returns:
            float:
                Average strength of all passed rules.

        Raises:
            TypeError:
                If rules is not a list.

            ValueError:
                If any rule strength is outside the valid range.
        """

        if not isinstance(rules, list):
            raise TypeError("rules must be a list of RuleResult objects.")

        passed_rules = [rule for rule in rules if rule.passed]

        if not passed_rules:
            return 0.0

        for rule in passed_rules:
            if not (0.0 <= rule.strength <= 1.0):
                raise ValueError(
                    f"Invalid rule strength ({rule.strength}) "
                    f"for rule '{rule.rule_name}'. "
                    "Strength must be between 0.0 and 1.0."
                )

        total_strength = sum(rule.strength for rule in passed_rules)

        return total_strength / len(passed_rules)