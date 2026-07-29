import shutil
import tempfile
import zipfile
from pathlib import Path

from market_data.historical_parser import HistoricalParser


class HistoricalLoader:

    def __init__(self):
        self.parser = HistoricalParser()

    def load_zip(self, zip_path):

        candles = []

        zip_path = Path(zip_path)

        try:
            with zipfile.ZipFile(zip_path, "r") as archive:

                csv_files = sorted(
                    file
                    for file in archive.namelist()
                    if file.lower().endswith(".csv")
                )

                print("CSV Files Found:")
                print(len(csv_files))

                for csv_file in csv_files:

                    print("Loading:", csv_file)

                    with tempfile.TemporaryDirectory() as temp_dir:

                        temp_file = Path(temp_dir) / Path(csv_file).name

                        with archive.open(csv_file) as source:
                            with open(temp_file, "wb") as target:
                                shutil.copyfileobj(source, target)

                        parsed = self.parser.parse_file(temp_file)
                        candles.extend(parsed)

        except zipfile.BadZipFile:
            print(f"Invalid ZIP file: {zip_path.name}")
            return []

        candles.sort(key=lambda candle: candle["datetime"])

        return candles


if __name__ == "__main__":

    print("Historical Loader Module Loaded Successfully")