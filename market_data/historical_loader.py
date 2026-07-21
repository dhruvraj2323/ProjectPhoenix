import zipfile
import csv
import io
from datetime import datetime


class HistoricalLoader:

    def __init__(self):
        pass


    def load_zip(self, zip_path):

        candles = []

        with zipfile.ZipFile(zip_path, "r") as z:

            csv_files = [
                file
                for file in z.namelist()
                if file.lower().endswith(".csv")
            ]


            print("CSV Files Found:")
            print(len(csv_files))


            for csv_file in csv_files:

                print(
                    "Loading:",
                    csv_file
                )

                with z.open(csv_file) as f:

                    content = (
                        io.TextIOWrapper(
                            f,
                            encoding="utf-8"
                        )
                    )


                    reader = csv.reader(
                        content
                    )


                    for row in reader:

                        candle = (
                            self._parse_csv_row(
                                row
                            )
                        )

                        if candle:
                            candles.append(
                                candle
                            )


        return candles



    def _parse_csv_row(self, row):

        try:

            if len(row) < 6:
                return None


            date = row[0]
            time = row[1]

            candle_datetime = datetime.strptime(
                f"{date} {time}",
                "%Y.%m.%d %H:%M"
            )


            return {
                "datetime": candle_datetime,
                "open": float(row[2]),
                "high": float(row[3]),
                "low": float(row[4]),
                "close": float(row[5]),
                "volume": int(row[6])
                if len(row) > 6
                else 0
            }


        except Exception:

            return None



if __name__ == "__main__":

    print(
        "Historical Loader Module Loaded Successfully"
    )