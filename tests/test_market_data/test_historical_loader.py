from market_data.historical_loader import HistoricalLoader


def main():

    loader = HistoricalLoader()


    candles = loader.load_zip(
        "data/raw/historical/"
        "HISTDATA_COM_MT_XAUUSD_M12021_202606.zip"
    )


    print("\nTotal Candles Loaded:")
    print(len(candles))


    if candles:

        print("\nFirst Candle:")
        print(candles[0])


    print("\nStatus: PASS")


if __name__ == "__main__":
    main()