from signals.signal_generator import SignalGenerator


generator = SignalGenerator()

signal = generator.generate()

print("\n===== Generator Test =====")
print("Final Signal :", signal.signal.value)
print("Strength     :", signal.strength)
print("Confidence   :", signal.confidence)
print("Reason       :", signal.reason)