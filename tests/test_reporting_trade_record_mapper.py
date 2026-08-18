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
    RiskDecision,
)

def test_trade_record_mapper_m63_7_observation_fields():

    context = ExecutionContext(
        execution_id="EXEC-M63-7",
        symbol="EURUSDm",
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
        entry_price=1.1000,
        stop_loss=1.0950,
        take_profit=1.1100,
        risk_percent=1.0,
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

    risk.decision = RiskDecision.APPROVED

    risk.metrics = RiskMetrics(
        risk_percent=1.25,
        position_size=0.10,
        stop_loss=1.0950,
        take_profit=1.1100,
        drawdown=0.75,
    )

    context.risk_result = risk

    # --------------------------------------------------
    # Execution
    # --------------------------------------------------

    context.execution_result = (
        ExecutionResult(
            accepted=True,
            status=(
                ExecutionStatus.ACCEPTED
            ),
            order_id="100001",
            executed_price=1.1002,
        )
    )

    # --------------------------------------------------
    # Requested order
    # --------------------------------------------------

    context.order = type(
        "DummyOrder",
        (),
        {
            "entry_price": 1.1000,
            "quantity": 0.10,
        },
    )()

    # --------------------------------------------------
    # MT5 Response
    # --------------------------------------------------

    response = type(
        "DummyTradeResponse",
        (),
        {
            "ticket": 100001,
            "executed_price": 1.1002,
            "executed_volume": 0.10,
            "broker_message": "Executed",
            "execution_time": datetime(
                2026,
                8,
                18,
                10,
                0,
                0,
                tzinfo=UTC,
            ),
            "retcode": 10009,
        },
    )()

    context.metadata[
        "trade_response"
    ] = response

    context.metadata[
        "mt5_order_check_retcode"
    ] = 0

    context.metadata[
        "mt5_order_check_comment"
    ] = "Done"

    context.metadata[
        "trading_protection_state"
    ] = "ACTIVE"

    # --------------------------------------------------
    # Optional DEMO analytics supplied upstream
    # --------------------------------------------------

    context.metadata[
        "spread"
    ] = 0.0002

    context.metadata[
        "slippage"
    ] = 0.0002

    context.metadata[
        "mfe"
    ] = 0.0010

    context.metadata[
        "mae"
    ] = 0.0003

    # --------------------------------------------------
    # Mark complete
    # --------------------------------------------------

    context.complete()

    # --------------------------------------------------
    # Map
    # --------------------------------------------------

    trade = TradeRecordMapper().map(
        context
    )

    # --------------------------------------------------
    # Assertions
    # --------------------------------------------------

    assert trade.strategy == (
        "S01_EMA_TREND"
    )

    assert trade.direction == "BUY"

    assert trade.strategy_decision == (
        strategy.status.value
        if hasattr(
            strategy.status,
            "value",
        )
        else str(strategy.status)
    )

    assert trade.risk_decision == (
        "APPROVED"
    )

    assert trade.execution_status == (
        "ACCEPTED"
    )

    assert trade.execution_message == (
        "Executed"
    )

    assert trade.execution_retcode == (
        10009
    )

    assert trade.requested_price == (
        1.1000
    )

    assert trade.executed_price == (
        1.1002
    )

    assert trade.requested_volume == (
        0.10
    )

    assert trade.executed_volume == (
        0.10
    )

    assert trade.order_check_retcode == 0

    assert trade.order_check_message == (
        "Done"
    )

    assert trade.runtime_state == (
        "COMPLETED"
    )

    assert trade.trading_protection_state == (
        "ACTIVE"
    )

    assert trade.risk_percent == (
        1.25
    )

    assert trade.drawdown == (
        0.75
    )

    assert trade.spread == (
        0.0002
    )

    assert trade.slippage == (
        0.0002
    )

    assert trade.mfe == (
        0.0010
    )

    assert trade.mae == (
        0.0003
    )
