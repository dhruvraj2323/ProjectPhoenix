from datetime import datetime
from pathlib import Path


class HistoricalParser:


    def parse_file(self, file_path):

        candles = []

        file_path = Path(file_path)


        with open(file_path, "r") as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue


                try:

                    candle = self.parse_line(line)

                    if candle:
                        candles.append(candle)


                except Exception:
                    continue


        return candles



    def parse_line(self, line):

        # Detect separator

        if "," in line:

            parts = line.split(",")

        else:

            parts = line.split()



        if len(parts) < 7:

            return None



        date = parts[0]
        time = parts[1]


        dt = datetime.strptime(
            f"{date} {time}",
            "%Y.%m.%d %H:%M"
        )


        candle = {

            "datetime": dt,

            "open": float(parts[2]),

            "high": float(parts[3]),

            "low": float(parts[4]),

            "close": float(parts[5]),

            "volume": int(float(parts[6]))

        }


        return candle