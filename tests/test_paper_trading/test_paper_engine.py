"""
=================================================
Project Phoenix
Paper Trading Engine Test
=================================================
"""

from paper_trading.paper_engine import PaperTradingEngine


def run_test():

    engine = PaperTradingEngine()

    result = engine.initialize()

    print()
    print("===== Paper Trading Engine =====")

    print(f"Approved : {result.approved}")
    print(f"Reason   : {result.reason}")

    assert result.approved

    print()
    print("Paper Trading Engine Test Passed")


if __name__ == "__main__":

    run_test()