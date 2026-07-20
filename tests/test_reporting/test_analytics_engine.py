"""
=================================================
Project Phoenix
Analytics Engine Test
=================================================
"""

from reporting.analytics_engine import AnalyticsEngine


def run_test():

    analytics = AnalyticsEngine()

    result = analytics.calculate(
        winning_trades=68,
        losing_trades=32,
        gross_profit=18000.0,
        gross_loss=5500.0,
    )

    print("===== Analytics Engine =====")

    print(f"Total Trades   : {result['total_trades']}")
    print(f"Win Rate       : {result['win_rate']}")
    print(f"Loss Rate      : {result['loss_rate']}")
    print(f"Net Profit     : {result['net_profit']}")
    print(f"Profit Factor  : {result['profit_factor']}")

    assert result["total_trades"] == 100
    assert result["winning_trades"] == 68
    assert result["losing_trades"] == 32
    assert result["win_rate"] == 68.0
    assert result["loss_rate"] == 32.0
    assert result["net_profit"] == 12500.0
    assert result["profit_factor"] == 3.27

    print()
    print("Analytics Engine Test Passed")


if __name__ == "__main__":

    run_test()