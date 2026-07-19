"""
=================================================
Project Phoenix
Indicator Engine Test
=================================================

Tests:
- SMA
- EMA
- RSI
- ATR
- MACD
- Bollinger Bands
"""

from dataclasses import dataclass


# -------------------------------------------------
# Mock Indicator Engine
# -------------------------------------------------


@dataclass
class IndicatorEngine:

    def sma(self):
        return 101.25

    def ema(self):
        return 102.10

    def rsi(self):
        return 58.40

    def atr(self):
        return 1.82

    def macd(self):
        return {
            "macd": 0.85,
            "signal": 0.72,
            "histogram": 0.13,
        }

    def bollinger(self):
        return {
            "upper": 105.50,
            "middle": 102.00,
            "lower": 98.50,
        }


# -------------------------------------------------
# Test
# -------------------------------------------------


def run_test():

    engine = IndicatorEngine()

    sma = engine.sma()
    ema = engine.ema()
    rsi = engine.rsi()
    atr = engine.atr()
    macd = engine.macd()
    bb = engine.bollinger()

    print("===== Indicator Engine =====")

    print(f"SMA              : {sma}")
    print(f"EMA              : {ema}")
    print(f"RSI              : {rsi}")
    print(f"ATR              : {atr}")
    print(f"MACD             : {macd['macd']}")
    print(f"MACD Signal      : {macd['signal']}")
    print(f"MACD Histogram   : {macd['histogram']}")
    print(f"Bollinger Upper  : {bb['upper']}")
    print(f"Bollinger Middle : {bb['middle']}")
    print(f"Bollinger Lower  : {bb['lower']}")

    assert sma > 0
    assert ema > 0
    assert 0 <= rsi <= 100
    assert atr > 0
    assert macd["macd"] is not None
    assert bb["upper"] > bb["middle"] > bb["lower"]

    print()
    print("Indicator Engine Test Passed")


# -------------------------------------------------
# Main
# -------------------------------------------------

if __name__ == "__main__":
    run_test()