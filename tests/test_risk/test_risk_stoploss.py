"""
Test for risk_stoploss.py
"""

from risk.risk_stoploss import StopLossCalculator


calculator = StopLossCalculator()

result = calculator.calculate(
    entry_price=250.0,
    stop_loss_percent=2.0,
)

print("===== Stop Loss Test =====")
print(f"Entry Price : 250.0")
print(f"Stop Loss   : {result.price}")
print(f"Reason      : {result.reason}")