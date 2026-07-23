"""
=================================================
Project Phoenix
Indicator Models Test
M32
=================================================
"""

from indicator_engine.indicator_models import (
    IndicatorType,
    IndicatorStatus,
    IndicatorValue,
    IndicatorSeries,
    IndicatorStatistics,
    IndicatorResult,
)


def test_indicator_models():

    value = IndicatorValue(
        indicator=IndicatorType.EMA,
        value=3450.25,
        period=20,
    )

    series = IndicatorSeries(
        indicator=IndicatorType.RSI,
    )

    series.values.extend(
        [52.4, 54.8, 56.1]
    )

    statistics = IndicatorStatistics(
        total_indicators=24,
        calculated=24,
        failed=0,
        execution_time_ms=18.72,
    )

    result = IndicatorResult(
        status=IndicatorStatus.SUCCESS,
        approved=True,
        statistics=statistics,
        reason="Indicator calculation completed.",
    )

    result.indicators["EMA20"] = value.value
    result.indicators["RSI14"] = series.values[-1]

    assert value.indicator == IndicatorType.EMA
    assert value.period == 20

    assert len(series.values) == 3

    assert result.status == IndicatorStatus.SUCCESS
    assert result.approved is True

    assert result.statistics.total_indicators == 24
    assert result.statistics.failed == 0

    print("===== Indicator Models =====")
    print("Status          :", result.status.value)
    print("Approved        :", result.approved)
    print("Indicators      :", result.statistics.total_indicators)
    print("Execution (ms)  :", result.statistics.execution_time_ms)
    print()

    print("Indicator Models Test Passed")


if __name__ == "__main__":
    test_indicator_models()