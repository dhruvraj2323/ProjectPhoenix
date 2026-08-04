"""
=================================================
Project Phoenix
Analytics Engine Test
M57
=================================================
"""

from reporting.analytics_engine import (
    AnalyticsEngine,
)
from reporting.reporting_models import (
    TradeRecord,
)


def test_analytics_engine():

    trades = [

        TradeRecord(
            trade_id="T1",
            symbol="EURUSD",
            direction="BUY",
            strategy="Breakout",
            pattern="Bull Flag",
            profit_loss=100.0,
            status="CLOSED",
        ),

        TradeRecord(
            trade_id="T2",
            symbol="EURUSD",
            direction="SELL",
            strategy="Reversal",
            pattern="Double Top",
            profit_loss=-40.0,
            status="CLOSED",
        ),

        TradeRecord(
            trade_id="T3",
            symbol="EURUSD",
            direction="BUY",
            strategy="Trend",
            pattern="Channel",
            profit_loss=60.0,
            status="CLOSED",
        ),

    ]

    engine = AnalyticsEngine()

    summary = engine.calculate(
        trades,
    )

    assert summary.total_trades == 3

    assert summary.winning_trades == 2

    assert summary.losing_trades == 1

    assert summary.gross_profit == 160.0

    assert summary.gross_loss == 40.0

    assert summary.net_profit == 120.0

    assert round(
        summary.win_rate,
        2,
    ) == 66.67

    assert summary.average_profit == 80.0

    assert summary.average_loss == 40.0

    assert summary.profit_factor == 4.0