"""
=================================================
Project Phoenix
Main Application
=================================================
"""

import os

from core.config import config
from core.logger import logger
from market.mt5_connector import MT5Connection
from market.market_data import MarketData


def main():
    """
    Application entry point.
    """

    app_logger = logger.initialize()

    # -----------------------------------------
    # Load Configuration
    # -----------------------------------------

    config.load_environment()
    config.load_settings()
    config.validate()

    app_logger.info("Project Phoenix started successfully.")

    app_logger.info(
        f"Project: {config.settings['project']['name']}"
    )

    app_logger.info(
        f"Version: {config.settings['project']['version']}"
    )

    app_logger.info(
        f"Symbol: {config.settings['market']['symbol']}"
    )

    app_logger.info(
        f"Timeframe: {config.settings['market']['timeframe']}"
    )

    # -----------------------------------------
    # MT5 Connection Test
    # -----------------------------------------

    mt5_connection = MT5Connection()

    if mt5_connection.initialize():

        login = int(os.getenv("MT5_LOGIN"))
        password = os.getenv("MT5_PASSWORD")
        server = os.getenv("MT5_SERVER")

        if mt5_connection.login(
            login,
            password,
            server
        ):

            account = mt5_connection.get_account_info()

            if account:

                app_logger.info(
                    f"Account : {account.login}"
                )

                app_logger.info(
                    f"Server  : {account.server}"
                )

                app_logger.info(
                    f"Balance : {account.balance}"
                )

                app_logger.info(
                    f"Equity  : {account.equity}"
                )

                # -----------------------------------------
                # Market Data Test
                # -----------------------------------------

                market_data = MarketData()

                dataframe = market_data.get_dataframe(
                    candle_count=10
                )

                if dataframe is not None:

                    app_logger.info(
                        "Historical Market Data:"
                    )

                    print(dataframe)

                    # -----------------------------------------
                    # Live Tick Test
                    # -----------------------------------------

                    tick = market_data.get_tick()

                    if tick is not None:

                        app_logger.info(
                            f"Bid Price : {tick.bid}"
                        )

                        app_logger.info(
                            f"Ask Price : {tick.ask}"
                        )

                        app_logger.info(
                            f"Last Price: {tick.last}"
                        )
                                            # -----------------------------------------
                    # Symbol Information Test
                    # -----------------------------------------

                    symbol_info = market_data.get_symbol_info()

                    if symbol_info is not None:

                        app_logger.info(
                            f"Symbol      : {symbol_info.name}"
                        )

                        app_logger.info(
                            f"Digits      : {symbol_info.digits}"
                        )

                        app_logger.info(
                            f"Point Value : {symbol_info.point}"
                        )

                        app_logger.info(
                            f"Spread      : {symbol_info.spread}"
                        )
                                            # -----------------------------------------
                    # Current Price Test
                    # -----------------------------------------

                    price = market_data.get_current_price()

                    if price is not None:

                        app_logger.info(
                            f"Current Bid : {price['bid']}"
                        )

                        app_logger.info(
                            f"Current Ask : {price['ask']}"
                        )

        mt5_connection.shutdown()


if __name__ == "__main__":
    main()