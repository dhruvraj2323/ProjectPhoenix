"""
Test for risk_takeprofit.py
"""

from risk.risk_takeprofit import TakeProfitCalculator


calculator = TakeProfitCalculator()

result = calculator.calculate(
    entry_price=250.0,
    stop_loss_price=245.0,
    risk_reward_ratio=2.0,
)

print("===== Take Profit Test =====")
print(f"Entry Price    : 250.0")
print(f"Stop Loss      : 245.0")
print(f"Take Profit    : {result.price}")
print(f"Risk : Reward  : 1 : {result.risk_reward_ratio}")