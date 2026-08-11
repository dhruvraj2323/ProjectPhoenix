"""
=================================================
Project Phoenix
Market Pipeline
Unit Test - Pipeline Executor
M40.X.5 - Risk Engine Integration
=================================================
"""

from unittest.mock import patch

from market_data.market_data_models import (
    MarketDataResult,
)

from market_pipeline.pipeline_context import (
    PipelineContext,
)

from market_pipeline.pipeline_executor import (
    PipelineExecutor,
)

from market_pipeline.pipeline_models import (
    PipelineStage,
)

from risk_engine.risk_models import (
    RiskResult,
)


TEST_DATA = "tests/test_data/sample_xauusd.zip"


class DummySymbolInfo:
    name = "XAUUSD"
    visible = True
    trade_mode = 0
    trade_exemode = 0
    filling_mode = 1
    trade_stops_level = 0
    trade_freeze_level = 0


class DummyResult:
    retcode = 10009
    order = 123456
    price = 3350.0
    volume = 0.10
    comment = "Executed"


@patch(
    "MetaTrader5.symbol_info",
)
@patch(
    "MetaTrader5.order_send",
)
def test_pipeline_executor(
    mock_order_send,
    mock_symbol_info,
):

    mock_symbol_info.return_value = (
        DummySymbolInfo()
    )

    mock_order_send.return_value = (
        DummyResult()
    )

    context = PipelineContext(
        pipeline_id="PIPELINE-001",
        symbol="XAUUSD",
        timeframe="M1",
        market_data_source=TEST_DATA,
    )

    executor = PipelineExecutor()

    result = executor.execute(
        context,
    )

    # -------------------------------------------------
    # Basic Validation
    # -------------------------------------------------

    assert result.completed is True

    assert result.approved is True

    assert result.failed is False

    # -------------------------------------------------
    # Final Stage
    # -------------------------------------------------

    assert (
        result.current_stage
        == PipelineStage.COMPLETED
    )

    # -------------------------------------------------
    # Market Data
    # -------------------------------------------------

    market_data = result.get_metadata(
        "market_data",
    )

    assert isinstance(
        market_data,
        MarketDataResult,
    )

    assert market_data.success is True

    assert len(
        market_data.candles,
    ) > 0

    assert (
        result.candles
        == market_data.candles
    )

    # -------------------------------------------------
    # Indicator Engine
    # -------------------------------------------------

    indicator_context = (
        result.get_metadata(
            "indicator_context",
        )
    )

    assert indicator_context is not None

    assert (
        indicator_context.completed
        is True
    )

    assert (
        indicator_context.approved
        is True
    )

    assert isinstance(
        result.indicators,
        dict,
    )

    assert "EMA_20" in result.indicators

    assert "SMA_20" in result.indicators

    assert "RSI_14" in result.indicators

    assert "ATR_14" in result.indicators

    assert "MACD" in result.indicators

    assert (
        "BOLLINGER_BANDS"
        in result.indicators
    )

    assert "VWAP" in result.indicators

    assert (
        "SUPERTREND"
        in result.indicators
    )

    # -------------------------------------------------
    # Pattern Engine
    # -------------------------------------------------

    pattern_context = (
        result.get_metadata(
            "pattern_context",
        )
    )

    assert pattern_context is not None

    assert (
        pattern_context.completed
        is True
    )

    assert (
        pattern_context.approved
        is True
    )

    assert isinstance(
        result.patterns,
        list,
    )

    assert (
        result.patterns
        == pattern_context.patterns
    )

    # -------------------------------------------------
    # Signal Engine
    # -------------------------------------------------

    signal_context = (
        result.get_metadata(
            "signal_context",
        )
    )

    assert signal_context is not None

    assert (
        signal_context.completed
        is True
    )

    assert (
        signal_context.approved
        is True
    )

    assert isinstance(
        result.signals,
        list,
    )

    assert (
        result.signals
        == signal_context.signals
    )

    assert len(
        result.signals,
    ) > 0

    signal = result.signals[0]

    assert "direction" in signal

    assert "strength" in signal

    assert "reason" in signal

    # -------------------------------------------------
    # Risk Engine
    # -------------------------------------------------

    risk_context = (
        result.get_metadata(
            "risk_context",
        )
    )

    assert risk_context is not None

    assert (
        risk_context.completed
        is True
    )

    assert (
        risk_context.approved
        is True
    )

    assert isinstance(
        result.risk_result,
        RiskResult,
    )

    assert (
        result.risk_result
        == risk_context.risk_result
    )

    # -------------------------------------------------
    # Portfolio Engine
    # -------------------------------------------------

    from portfolio_engine.portfolio_models import (
        PortfolioSummary,
    )

    portfolio_context = (
        result.get_metadata(
            "portfolio_context",
        )
    )

    assert portfolio_context is not None

    assert (
        portfolio_context.completed
        is True
    )

    assert (
        portfolio_context.approved
        is True
    )

    assert isinstance(
        result.portfolio_result,
        PortfolioSummary,
    )

    assert (
        result.portfolio_result
        == portfolio_context.summary
    )

    # -------------------------------------------------
    # AI
    # -------------------------------------------------

    from ai_decision.ai_models import (
        AIDecision,
    )

    ai_decision = result.ai_result

    assert isinstance(
        ai_decision,
        AIDecision,
    )

    assert (
        ai_decision.approved
        is True
    )

    assert (
        result.get_metadata(
            "ai_decision",
        )
        == ai_decision
    )

    # -------------------------------------------------
    # Execution
    # -------------------------------------------------

    from execution_engine.execution_models import (
        ExecutionResult,
        ExecutionStatus,
    )

    assert isinstance(
        result.execution_result,
        ExecutionResult,
    )

    assert (
        result.execution_result.status
        == ExecutionStatus.ACCEPTED
    )

    assert (
        result.execution_result.accepted
        is True
    )

    # -------------------------------------------------
    # MT5 Boundary Validation
    # -------------------------------------------------

    mock_symbol_info.assert_called()

    mock_order_send.assert_called()

    # -------------------------------------------------
    # Console Report
    # -------------------------------------------------

    print()

    print(
        "===== Pipeline Executor ====="
    )

    print(
        "Pipeline ID      :",
        result.pipeline_id,
    )

    print(
        "Symbol           :",
        result.symbol,
    )

    print(
        "Timeframe        :",
        result.timeframe,
    )

    print(
        "Candles Loaded   :",
        len(result.candles),
    )

    print(
        "Indicators       :",
        len(result.indicators),
    )

    print(
        "Patterns         :",
        len(result.patterns),
    )

    print(
        "Signals          :",
        len(result.signals),
    )

    print(
        "Current Stage    :",
        result.current_stage.value,
    )

    print(
        "Approved         :",
        result.approved,
    )

    print(
        "Completed        :",
        result.completed,
    )

    print(
        "Decision         :",
        result.decision,
    )

    print(
        "Reason           :",
        result.reason,
    )

    print()

    print(
        "Pipeline Executor Test Passed"
    )


if __name__ == "__main__":
    test_pipeline_executor()