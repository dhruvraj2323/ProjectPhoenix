"""
Test for performance_validator.py
"""

from performance.performance_models import PerformanceMetrics
from performance.performance_validator import PerformanceValidator

metrics = PerformanceMetrics(
    total_trades=10,
    wins=7,
    losses=2,
    breakeven=1,
    win_rate=70.0,
    average_profit=120.0,
    average_loss=-60.0,
)

validator = PerformanceValidator()

result = validator.validate(metrics)

print("===== Performance Validator Test =====")
print(f"Valid  : {result.valid}")
print(f"Reason : {result.reason}")