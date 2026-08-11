"""
=================================================
Project Phoenix
Trade Record Mapper Test
M60.3.1
=================================================
"""

from datetime import UTC, datetime

from execution_engine.execution_context import (
    ExecutionContext,
)

from execution_engine.execution_models import (
    ExecutionResult,
    ExecutionStatus,
)

from reporting.trade_record_mapper import (
    TradeRecordMapper,
)

from strategy.strategy_models import (
    StrategyResult,
    StrategySignal,
    StrategyType,
    TradeDirection,
)

from risk_engine.risk_models import (
    RiskMetrics,
    RiskResult,
)


class DummyTradeResponse:

    ticket = 2372901969

    executed_price = 4381.838

    executed_volume = 0.01

    broker_message = "ok"

    execution_time = datetime(
        2026,
        8,
        11,
        16,
        51,
        4,
        tzinfo=UTC,
    )

    retcode = 10009


def test_trade_record_mapper():

    # --------------------------------------------------
    # Execution Context
    # --------------------------------------------------

    context = ExecutionContext(
        execution_id="EXEC-001",
        symbol="XAUUSDm",
        timeframe="M15",
    )

    # --------------------------------------------------
    # Strategy
    # --------------------------------------------------

    signal = StrategySignal(
        strategy_id="S01",
        strategy_name=(
            StrategyType.S01_EMA_TREND
        ),
        direction=(
            TradeDirection.BUY
        ),
        confidence=90,
        entry_price=4380.000,
        stop_loss=4370.000,
        take_profit=4400.000,
        risk_percent=1,
        reason="BUY",
    )

    strategy = StrategyResult()

    strategy.signals.append(
        signal,
    )

    context.strategy_result = (
        strategy
    )

    # --------------------------------------------------
    # Risk
    # --------------------------------------------------

    risk = RiskResult()

    risk.metrics = RiskMetrics(
        position_size=0.01,
        stop_loss=4370.000,
        take_profit=4400.000,
    )

    context.risk_result = risk

    # --------------------------------------------------
    # Execution Result
    # --------------------------------------------------

    context.execution_result = (
        ExecutionResult(
            accepted=True,
            status=(
                ExecutionStatus.ACCEPTED
            ),
            order_id="2372901969",
            executed_price=4381.838,
        )
    )

    # --------------------------------------------------
    # Actual MT5 Trade Response
    # --------------------------------------------------

    context.metadata[
        "trade_response"
    ] = DummyTradeResponse()

    # --------------------------------------------------
    # Mark Execution Complete
    # --------------------------------------------------

    context.complete()

    # --------------------------------------------------
    # Mapper
    # --------------------------------------------------

    mapper = TradeRecordMapper()

    trade = mapper.map(
        context,
    )

    # --------------------------------------------------
    # Assertions
    # --------------------------------------------------

    assert trade.trade_id == (
        "2372901969"
    )

    assert trade.symbol == (
        "XAUUSDm"
    )

    assert trade.direction == "BUY"

    assert trade.strategy == (
        "S01_EMA_TREND"
    )

    assert trade.entry_price == (
        4381.838
    )

    assert trade.stop_loss == (
        4370.000
    )

    assert trade.take_profit == (
        4400.000
    )

    assert trade.volume == 0.01

    assert trade.profit_loss == 0.0

    assert trade.status == "OPEN"

    assert trade.opened_at == (
        DummyTradeResponse.execution_time
    )

    assert trade.closed_at == (
        DummyTradeResponse.execution_time
    )