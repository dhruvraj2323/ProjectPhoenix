from signals.signal_models import (
    TradingSignal,
    SignalType,
)

from signals.signal_filters import SignalFilter


signal = TradingSignal(
    signal=SignalType.BUY,
    strength=0.80,
    confidence=0.90,
)

filter_engine = SignalFilter()

result = filter_engine.filter(signal)

print("===== Filter Test =====")
print("Accepted :", result.accepted)
print("Reason   :", result.reason)