import zipfile
import tempfile
from pathlib import Path

from market_data.historical_parser import HistoricalParser


class FullHistoryLoader:

    def __init__(self, historical_path):
        self.historical_path = Path(historical_path)
        self.parser = HistoricalParser()

    def find_zip_files(self):
        return sorted(self.historical_path.glob("*.zip"))

    def load_all_history(self):

        all_candles = []

        zip_files = self.find_zip_files()

        for zip_file in zip_files:

            print("\nProcessing ZIP:")
            print(zip_file.name)

            with zipfile.ZipFile(zip_file, "r") as archive:

                csv_files = sorted(
                    f for f in archive.namelist()
                    if f.lower().endswith(".csv")
                )

                print(f"CSV Files Found: {len(csv_files)}")

                for csv_file in csv_files:

                    print(f"Loading: {csv_file}")

                    with tempfile.TemporaryDirectory() as temp_dir:

                        temp_file = Path(temp_dir) / Path(csv_file).name

                        with archive.open(csv_file) as source:
                            with open(temp_file, "wb") as target:
                                target.write(source.read())

                        candles = self.parser.parse_file(temp_file)
                        all_candles.extend(candles)

        all_candles.sort(key=lambda candle: candle["datetime"])
        
        return all_candles