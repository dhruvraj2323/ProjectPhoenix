"""
Test for performance_logger.py
"""

from performance.performance_logger import PerformanceLogger
from performance.performance_models import PerformanceMetrics

metrics = PerformanceMetrics(
    total_trades=10,
    wins=7,
    losses=2,
    breakeven=1,
    win_rate=70.0,
    average_profit=120.0,
    average_loss=-60.0,
)

logger = PerformanceLogger()

logger.log(metrics)