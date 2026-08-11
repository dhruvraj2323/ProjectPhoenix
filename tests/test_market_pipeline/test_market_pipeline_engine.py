"""
Test Pipeline Manager
"""

from unittest.mock import patch

from market_pipeline.pipeline_context import (
    PipelineContext,
)

from market_pipeline.pipeline_manager import (
    PipelineManager,
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
    digits = 3


class DummyTick:
    bid = 3349.500
    ask = 3350.000


class DummyResult:
    retcode = 10009
    order = 123456
    price = 3350.0
    volume = 0.10
    comment = "Executed"


class DummyOrderCheckResult:
    retcode = 0
    comment = "Done"


@patch(
    "MetaTrader5.symbol_info",
)
@patch(
    "MetaTrader5.symbol_info_tick",
)
@patch(
    "MetaTrader5.order_check",
)
@patch(
    "MetaTrader5.order_send",
)
def test_pipeline_manager(
    mock_order_send,
    mock_order_check,
    mock_symbol_info_tick,
    mock_symbol_info,
):

    # -------------------------------------------------
    # MT5 Mocks
    # -------------------------------------------------

    mock_symbol_info.return_value = (
        DummySymbolInfo()
    )

    mock_symbol_info_tick.return_value = (
        DummyTick()
    )

    mock_order_check.return_value = (
        DummyOrderCheckResult()
    )

    mock_order_send.return_value = (
        DummyResult()
    )

    # -------------------------------------------------
    # Pipeline Manager
    # -------------------------------------------------

    manager = PipelineManager()

    context = PipelineContext(
        pipeline_id="PIPELINE-001",
        symbol="XAUUSD",
        timeframe="M1",
        market_data_source=TEST_DATA,
    )

    result = manager.run(
        context,
    )

    # -------------------------------------------------
    # Basic Validation
    # -------------------------------------------------

    assert result.completed is True

    assert result.approved is True

    assert result.failed is False

    # -------------------------------------------------
    # Decision
    # -------------------------------------------------

    assert (
        result.decision
        == "PIPELINE_COMPLETED"
    )

    # -------------------------------------------------
    # Market Data Validation
    # -------------------------------------------------

    market_data = result.get_metadata(
        "market_data",
    )

    assert market_data is not None

    assert market_data.success is True

    assert len(
        result.candles,
    ) > 0

    assert (
        len(result.candles)
        == len(market_data.candles)
    )

    # -------------------------------------------------
    # Indicator Validation
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Patterns
    # -------------------------------------------------

    assert isinstance(
        result.patterns,
        list,
    )

    # -------------------------------------------------
    # MT5 Boundary Validation
    # -------------------------------------------------

    mock_symbol_info.assert_called()

    mock_symbol_info_tick.assert_called_once_with(
        "XAUUSD",
    )

    mock_order_check.assert_called()

    mock_order_send.assert_called()

    # -------------------------------------------------
    # Console Report
    # -------------------------------------------------

    print()

    print(
        "===== Pipeline Manager ====="
    )

    print(
        "Pipeline ID     :",
        result.pipeline_id,
    )

    print(
        "Symbol          :",
        result.symbol,
    )

    print(
        "Timeframe       :",
        result.timeframe,
    )

    print(
        "Candles Loaded  :",
        len(result.candles),
    )

    print(
        "Indicators      :",
        len(result.indicators),
    )

    print(
        "Completed       :",
        result.completed,
    )

    print(
        "Approved        :",
        result.approved,
    )

    print(
        "Decision        :",
        result.decision,
    )

    print(
        "Reason          :",
        result.reason,
    )

    print()

    print(
        "Pipeline Manager Test Passed"
    )


if __name__ == "__main__":
    test_pipeline_manager()