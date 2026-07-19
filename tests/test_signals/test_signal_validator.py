from signals.signal_models import (
    TradingSignal,
    SignalType,
)

from signals.signal_validator import SignalValidator


signal = TradingSignal(
    signal=SignalType.BUY,
    strength=0.80,
    confidence=0.90,
)

validator = SignalValidator()

result = validator.validate(signal)

print("===== Validator Test =====")
print("Valid  :", result.valid)
print("Reason :", result.reason)