import MetaTrader5 as mt5

PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

mt5.initialize(path=PATH)

symbols = mt5.symbols_get()

print(f"Total Symbols: {len(symbols)}")
print()

for symbol in symbols[:50]:
    print(symbol.name)

mt5.shutdown()