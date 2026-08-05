"""
=================================================
Project Phoenix
Live Pipeline Test
M58.12.3
=================================================
"""

from deployment.live_pipeline import (
    LivePipeline,
)


def test_live_pipeline():

    pipeline = LivePipeline()

    results = pipeline.execute(

        symbol="EURUSD",

        bars=10,

    )

    assert isinstance(results, dict)

    assert "D1" in results

    assert "H4" in results

    assert "H1" in results

    assert "M15" in results

    assert "M5" in results

    for result in results.values():

        assert result is not None

        assert hasattr(result, "approved")