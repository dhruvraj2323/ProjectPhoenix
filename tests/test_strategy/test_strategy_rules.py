"""
=================================================
Project Phoenix
Test Strategy Rules
M38
=================================================
"""

from strategy.strategy_context import (
    StrategyContext,
)

from strategy.strategy_models import (
    StrategyStatus,
    StrategyType,
    TradeDirection,
)

from strategy.strategy_rules import (
    StrategyRules,
)


def test_strategy_rules_buy():

    rules = StrategyRules()

    context = StrategyContext(
        engine_id="STRATEGY-001",
        symbol="XAUUSD",
        timeframe="M15",
    )

    context.indicators = {
        "EMA9": 2455.0,
        "EMA21": 2450.0,
        "EMA200": 2435.0,
        "RSI14": 62.0,
    }

    context.market_data = {
        "price": 2458.0,
    }

    result = rules.evaluate_s01(
        context,
    )

    assert (
        result.strategy_result.status
        == StrategyStatus.APPROVED
    )

    assert (
        result.strategy_result.selected_strategy
        == StrategyType.S01_EMA_TREND
    )

    assert (
        len(
            result.strategy_result.signals
        )
        == 1
    )

    signal = result.strategy_result.signals[0]

    assert (
        signal.direction
        == TradeDirection.BUY
    )


def test_strategy_rules_sell():

    rules = StrategyRules()

    context = StrategyContext(
        engine_id="STRATEGY-002",
        symbol="XAUUSD",
        timeframe="M15",
    )

    context.indicators = {
        "EMA9": 2435.0,
        "EMA21": 2440.0,
        "EMA200": 2455.0,
        "RSI14": 38.0,
    }

    context.market_data = {
        "price": 2430.0,
    }

    result = rules.evaluate_s01(
        context,
    )

    assert (
        result.strategy_result.status
        == StrategyStatus.APPROVED
    )

    assert (
        result.strategy_result.selected_strategy
        == StrategyType.S01_EMA_TREND
    )

    assert (
        len(
            result.strategy_result.signals
        )
        == 1
    )

    signal = result.strategy_result.signals[0]

    assert (
        signal.direction
        == TradeDirection.SELL
    )


def test_strategy_rules_rejected():

    rules = StrategyRules()

    context = StrategyContext(
        engine_id="STRATEGY-003",
        symbol="XAUUSD",
        timeframe="M15",
    )

    context.indicators = {
        "EMA9": 2450.0,
        "EMA21": 2450.0,
        "EMA200": 2450.0,
        "RSI14": 50.0,
    }

    context.market_data = {
        "price": 2450.0,
    }

    result = rules.evaluate_s01(
        context,
    )

    assert (
        result.strategy_result.status
        == StrategyStatus.CREATED
    )

    assert (
        len(
            result.strategy_result.signals
        )
        == 0
    )

    assert (
        result.strategy_result.statistics.rejected
        == 1
    )