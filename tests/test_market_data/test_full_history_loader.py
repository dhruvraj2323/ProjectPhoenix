from market_data.full_history_loader import FullHistoryLoader


def main():

    loader = FullHistoryLoader(
        "data/raw/historical"
    )

    candles = loader.load_all_history()


    print("\n===================")
    print("TOTAL CANDLES:")
    print(len(candles))


    print("\nFIRST CANDLE:")
    print(candles[0])


    print("\nLAST CANDLE:")
    print(candles[-1])


    print("\nSTATUS: PASS")


if __name__ == "__main__":
    main()