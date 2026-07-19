from signals.signal_models import RuleDirection, RuleResult
from signals.signal_strength import SignalStrengthCalculator


calculator = SignalStrengthCalculator()

rules = [
    RuleResult(
        rule_name="Rule1",
        direction=RuleDirection.BULLISH,
        strength=0.80,
        passed=True,
    ),
    RuleResult(
        rule_name="Rule2",
        direction=RuleDirection.BULLISH,
        strength=0.60,
        passed=True,
    ),
    RuleResult(
        rule_name="Rule3",
        direction=RuleDirection.NEUTRAL,
        strength=0.40,
        passed=False,
    ),
]

strength = calculator.calculate(rules)

print("===== Strength Test =====")
print("Signal Strength :", strength)