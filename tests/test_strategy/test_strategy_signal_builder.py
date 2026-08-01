from strategy.strategy_signal_builder import (
    StrategySignalBuilder,
)

from strategy.strategy_models import (
    StrategyType,
    TradeDirection,
)


def test_strategy_signal_builder():

    builder = StrategySignalBuilder()

    signal = builder.build(

        strategy_id="S01",

        strategy_name=StrategyType.S01_EMA_TREND,

        direction=TradeDirection.BUY,

        entry_price=2450.0,

        stop_loss=2440.0,

        take_profit=2475.0,

        risk_percent=1.0,

        reason="EMA Trend",

        strategy_score=92.0,

        pattern_score=18.0,

        indicator_score=60.0,

        confirmation_score=14.0,

        confidence=96.0,

    )

    assert signal.strategy_id == "S01"

    assert signal.strategy_score == 92.0

    assert signal.pattern_score == 18.0

    assert signal.indicator_score == 60.0

    assert signal.confirmation_score == 14.0

    assert signal.confidence == 96.0