from risk_engine.swing_detector import (
    SwingDetector,
)


def test_swing_detector():

    candles = [

        {
            "high": 100,
            "low": 90,
        },

        {
            "high": 110,
            "low": 85,
        },

        {
            "high": 105,
            "low": 95,
        },

        {
            "high": 120,
            "low": 88,
        },

        {
            "high": 115,
            "low": 91,
        },

    ]

    detector = SwingDetector()

    assert (

        detector.last_swing_high(
            candles,
        )

        == 120

    )

    assert (

        detector.last_swing_low(
            candles,
        )

        == 88

    )