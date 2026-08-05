"""
=================================================
Project Phoenix
Runtime Configuration
M58.12.13
=================================================
"""

from __future__ import annotations

import json
from pathlib import Path


class RuntimeConfig:
    """
    Loads deployment runtime configuration.
    """

    def __init__(self) -> None:

        config_file = (
            Path("config")
            / "runtime_config.json"
        )

        with open(
            config_file,
            "r",
            encoding="utf-8",
        ) as file:

            self.data = json.load(file)

    @property
    def symbol(self) -> str:

        return self.data["market"]["symbol"]

    @property
    def timeframe(self) -> str:

        return self.data["market"]["timeframe"]

    @property
    def bars(self) -> int:

        return self.data["market"]["bars"]

    @property
    def interval(self) -> int:

        return self.data["runner"]["interval_seconds"]

    @property
    def cycles(self) -> int:

        return self.data["runner"]["cycles"]

    @property
    def reporting_enabled(self) -> bool:

        return self.data["reporting"]["enabled"]

    @property
    def paper_trading_enabled(self) -> bool:

        return self.data["paper_trading"]["enabled"]