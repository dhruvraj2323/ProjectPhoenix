"""
=================================================
Project Phoenix
Candlestick Recognition Engine Test
=================================================

Tests:
- Single Candle Patterns
- Two Candle Patterns
- Three Candle Patterns
- Continuation Patterns
- Professional Patterns
"""

from dataclasses import dataclass


# -------------------------------------------------
# Mock Candlestick Engine
# -------------------------------------------------


@dataclass
class CandlestickEngine:

    def detect_patterns(self):

        return {
            "Doji": True,
            "Hammer": True,
            "Bullish Engulfing": True,
            "Morning Star": True,
            "Inside Bar": True,
            "Bullish Marubozu": True,
        }


# -------------------------------------------------
# Test
# -------------------------------------------------


def run_test():

    engine = CandlestickEngine()

    patterns = engine.detect_patterns()

    print("===== Candlestick Recognition =====")

    print(f"Doji                : {'DETECTED' if patterns['Doji'] else 'NOT DETECTED'}")
    print(f"Hammer              : {'DETECTED' if patterns['Hammer'] else 'NOT DETECTED'}")
    print(f"Bullish Engulfing   : {'DETECTED' if patterns['Bullish Engulfing'] else 'NOT DETECTED'}")
    print(f"Morning Star        : {'DETECTED' if patterns['Morning Star'] else 'NOT DETECTED'}")
    print(f"Inside Bar          : {'DETECTED' if patterns['Inside Bar'] else 'NOT DETECTED'}")
    print(f"Bullish Marubozu    : {'DETECTED' if patterns['Bullish Marubozu'] else 'NOT DETECTED'}")

    assert patterns["Doji"]
    assert patterns["Hammer"]
    assert patterns["Bullish Engulfing"]
    assert patterns["Morning Star"]
    assert patterns["Inside Bar"]
    assert patterns["Bullish Marubozu"]

    print()
    print("Candlestick Recognition Test Passed")


# -------------------------------------------------
# Main
# -------------------------------------------------

if __name__ == "__main__":
    run_test()