"""
=================================================
Project Phoenix
Live Trading Engine Test
=================================================
"""

from live_trading.live_engine import LiveTradingEngine


def run_test():

    engine = LiveTradingEngine()

    result = engine.initialize()

    print()
    print("===== Live Trading Engine =====")

    print(f"Approved : {result.approved}")
    print(f"Reason   : {result.reason}")

    assert result.approved

    print()
    print("Live Trading Engine Test Passed")


if __name__ == "__main__":

    run_test()