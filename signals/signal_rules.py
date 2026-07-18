"""
Project Phoenix
Milestone M8 - Signal Generation Engine

Module:
    signal_rules.py

Purpose:
    Evaluates trading rules and produces RuleResult objects.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from signals.signal_models import RuleResult, RuleDirection


class BaseRule(ABC):
    """
    Abstract base class for all trading rules.
    """

    @abstractmethod
    def evaluate(self) -> RuleResult:
        """
        Evaluate the trading rule.
        """
        pass


class AlwaysHoldRule(BaseRule):
    """
    Default placeholder rule.

    Always returns a neutral signal.
    """

    def evaluate(self) -> RuleResult:
        return RuleResult(
            rule_name="AlwaysHoldRule",
            direction=RuleDirection.NEUTRAL,
            strength=0.0,
            passed=True,
            reason="Default placeholder rule."
        )