"""
=================================================
Project Phoenix
Test Signal Models
M34
=================================================
"""

from signal_engine.signal_models import (
    TradingSignal,
    SignalDirection,
    SignalStrength,
    SignalStatus,
    SignalResult,
)


def test_signal_models():

    signal = TradingSignal(
        signal_id="SIG-001",
        symbol="XAUUSD",
        timeframe="M1",
        direction=SignalDirection.BUY,
        strength=SignalStrength.STRONG,
        confidence=92.5,
    )

    assert signal.signal_id == "SIG-001"
    assert signal.direction == SignalDirection.BUY
    assert signal.strength == SignalStrength.STRONG

    result = SignalResult(
        status=SignalStatus.CREATED,
    )

    result.signals.append(signal)

    result.statistics.total_signals = 1
    result.statistics.buy_signals = 1

    assert result.statistics.total_signals == 1
    assert len(result.signals) == 1
    assert result.status == SignalStatus.CREATED