"""
=================================================
Project Phoenix
Database Models Test
=================================================
"""

from database.database_models import (
    ConfigurationRecord,
    DatabaseResult,
    DatabaseStatus,
    LearningRecord,
    PerformanceRecord,
    SignalRecord,
    TradeRecord,
)


def run_test():

    trade = TradeRecord(
        trade_id=1,
        symbol="EURUSD",
        direction="BUY",
        entry_price=1.1000,
        exit_price=1.1050,
        stop_loss=1.0950,
        take_profit=1.1100,
        lot_size=0.10,
        profit=50.0,
        open_time="2026-01-01 10:00",
        close_time="2026-01-01 11:00",
    )

    signal = SignalRecord(
        signal_id=1,
        symbol="EURUSD",
        signal_type="BUY",
        strength=82,
        confidence=0.91,
        timestamp="2026-01-01 09:59",
    )

    performance = PerformanceRecord(
        total_trades=100,
        win_rate=68.5,
        net_profit=12500.0,
        profit_factor=2.15,
        drawdown=4.2,
        expectancy=125.0,
        timestamp="2026-01-01",
    )

    learning = LearningRecord(
        recommendation_type="RISK_PERCENT",
        current_value=1.0,
        suggested_value=1.2,
        confidence=0.93,
        reason="Increase risk due to consistent profitability.",
        timestamp="2026-01-01",
    )

    config = ConfigurationRecord(
        name="strategy_mode",
        value="Adaptive",
        environment="DEVELOPMENT",
        version="1.0",
    )

    status = DatabaseStatus(
        connected=True,
        initialized=True,
        database_name="project_phoenix.db",
    )

    result = DatabaseResult(
        approved=True,
        reason="Database initialized successfully.",
        status=status,
    )

    assert trade.trade_id == 1
    assert signal.signal_type == "BUY"
    assert performance.total_trades == 100
    assert learning.confidence == 0.93
    assert config.environment == "DEVELOPMENT"
    assert status.connected
    assert result.approved

    print("===== Database Models =====")
    print(f"Trade ID        : {trade.trade_id}")
    print(f"Signal          : {signal.signal_type}")
    print(f"Win Rate        : {performance.win_rate}%")
    print(f"Recommendation  : {learning.recommendation_type}")
    print(f"Database        : {status.database_name}")

    print()
    print("Database Models Test Passed")


if __name__ == "__main__":

    run_test()