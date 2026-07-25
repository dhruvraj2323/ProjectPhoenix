"""
Project Phoenix
M8 Test - signal_models.py
"""

from signals.signal_models import (
    FilterResult,
    RuleDirection,
    RuleResult,
    SignalContext,
    SignalType,
    TradingSignal,
    ValidationResult,
)


def main():
    print("===== Signal Models Test =====")

    rule = RuleResult(
        rule_name="EMA_Crossover",
        direction=RuleDirection.BULLISH,
        strength=0.85,
        passed=True,
        reason="Fast EMA crossed above Slow EMA",
    )

    signal = TradingSignal(
        signal=SignalType.BUY,
        strength=0.80,
        confidence=90.0,
        rules=[rule],
        reason="Strong Bullish Confirmation",
    )

    context = SignalContext(
        symbol="EURUSD",
        timeframe="H1",
        price=1.1050,
    )

    validation = ValidationResult(
        valid=True,
        score=95.0,
        reason="Signal passed all validation checks.",
    )

    filter_result = FilterResult(
        accepted=True,
        reason="Signal accepted by filter.",
    )

    print(f"Signal       : {signal.signal.name}")
    print(f"Strength     : {signal.strength}")
    print(f"Confidence   : {signal.confidence}")
    print(f"Rules        : {len(signal.rules)}")
    print(f"Symbol       : {context.symbol}")
    print(f"Timeframe    : {context.timeframe}")
    print(f"Price        : {context.price}")
    print(f"Validation   : {validation.valid}")
    print(f"Filter       : {filter_result.accepted}")

    print("\nSignal Models Test Completed Successfully.")


if __name__ == "__main__":
    main()