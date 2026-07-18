from signals.signal_models import (
    TradingSignal,
    SignalType,
)

from signals.signal_logger import SignalLogger


signal = TradingSignal(
    signal=SignalType.BUY,
    strength=0.80,
    confidence=0.92,
    reason="Test signal."
)

logger = SignalLogger()

logger.log(signal)