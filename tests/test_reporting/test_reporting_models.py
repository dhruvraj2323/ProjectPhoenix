from reporting.reporting_models import (
    DailyReport,
    PerformanceSummary,
    TradeRecord,
)

def test_trade_record_m63_7_demo_fields():

    trade = TradeRecord(
        trade_id="M63-001",
        symbol="BTCUSDm",
        strategy="S01_EMA_TREND",

        strategy_decision="APPROVED",
        risk_decision="APPROVED",
        execution_status="EXECUTED",

        execution_retcode=10009,

        requested_price=60000.0,
        executed_price=60001.0,

        requested_volume=0.05,
        executed_volume=0.05,

        runtime_state="COMPLETED",
        trading_protection_state="ACTIVE",

        risk_percent=1.0,
        drawdown=0.5,
    )

    assert trade.symbol == (
        "BTCUSDm"
    )

    assert trade.strategy == (
        "S01_EMA_TREND"
    )

    assert trade.strategy_decision == (
        "APPROVED"
    )

    assert trade.risk_decision == (
        "APPROVED"
    )

    assert trade.execution_status == (
        "EXECUTED"
    )

    assert trade.execution_retcode == (
        10009
    )

    assert trade.requested_price == (
        60000.0
    )

    assert trade.executed_price == (
        60001.0
    )

    assert trade.runtime_state == (
        "COMPLETED"
    )

    assert trade.trading_protection_state == (
        "ACTIVE"
    )

    assert trade.risk_percent == (
        1.0
    )

    assert trade.drawdown == (
        0.5
    )