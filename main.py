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
from indicators.indicator_engine import IndicatorEngine
from indicators.candlestick_engine import CandlestickEngine
from signals.signal_generator import SignalGenerator
from risk.risk_engine import RiskEngine
from risk.risk_models import RiskContext
from execution.execution_engine import ExecutionEngine
from performance.performance_engine import PerformanceEngine
from performance.performance_models import (
    PerformanceContext,
    TradeOutcome,
    TradeResult,
)

from portfolio.portfolio_engine import PortfolioEngine

from portfolio.portfolio_models import (
    PortfolioContext,
    PositionDirection,
    PositionInfo,
)

from strategy_optimizer.strategy_engine import StrategyEngine

from strategy_optimizer.strategy_models import (
    StrategyContext,
    StrategyPerformance,
)
from ai_decision.ai_engine import AIEngine

from ai_decision.ai_models import (
    AIContext,
)

from orchestrator.orchestrator_engine import OrchestratorEngine

from orchestrator.orchestrator_models import (
    TradingDecision,
)

from backtesting.backtest_engine import BacktestEngine

from backtesting.backtest_models import (
    BacktestContext,
    BacktestDecision,
)

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
                    # EMA Test
                    # -----------------------------------------

                    indicator_engine = IndicatorEngine()
                    import indicators.indicator_engine

                    print(indicators.indicator_engine.__file__)
                    print(type(indicator_engine))
                    print(dir(indicator_engine))

                    dataframe = indicator_engine.calculate_ema(
                        dataframe,
                        period=20
                    )

                    app_logger.info(
                        "EMA 20 Calculation:"
                    )

                    print(
                        dataframe[
                            ["time", "close", "EMA_20"]
                        ].tail(10)
                    )
                                        # -----------------------------------------
                    # SMA Test
                    # -----------------------------------------

                    dataframe = indicator_engine.calculate_sma(
                        dataframe,
                        period=20
                    )

                    app_logger.info(
                        "SMA 20 Calculation:"
                    )

                    print(
                        dataframe[
                            ["time", "close", "SMA_20"]
                        ].tail(10)
                    )
                    dataframe = indicator_engine.calculate_rsi(
                        dataframe,
                        period=14
                    )

                    app_logger.info(
                        "RSI 14 Calculation:"
                    )

                    print(
                        dataframe[
                            ["time", "close", "RSI_14"]
                        ]
                    )
                   
                    # -----------------------------------------
                    # MACD Test
                    # -----------------------------------------

                    dataframe = indicator_engine.calculate_macd(
                        dataframe
                    )

                    app_logger.info(
                        "MACD Calculation:"
                    )

                    print(
                        dataframe[
                            [
                                "time",
                                "close",
                                "MACD",
                                "MACD_SIGNAL",
                                "MACD_HISTOGRAM"
                            ]
                        ].tail(10)
                    )
                                    # -----------------------------------------
                    # Bollinger Bands Test
                    # -----------------------------------------

                    dataframe = indicator_engine.calculate_bollinger_bands(
                        dataframe,
                        period=20,
                        std_dev=2
                    )

                    app_logger.info(
                        "Bollinger Bands Calculation:"
                    )

                    print(
                        dataframe[
                            [
                                "time",
                                "close",
                                "BB_MIDDLE",
                                "BB_UPPER",
                                "BB_LOWER"
                            ]
                        ].tail(10)
                    )
                    # -----------------------------------------
                    # ATR Test
                    # -----------------------------------------

                    dataframe = indicator_engine.calculate_atr(
                        dataframe,
                        period=14
                    )

                    app_logger.info(
                        "ATR 14 Calculation:"
                    )

                    print(
                        dataframe[
                            ["time", "high", "low", "close", "ATR_14"]
                        ]
                    )
                    # -----------------------------------------
                    # Candlestick Engine Test
                    # -----------------------------------------

                    candlestick_engine = CandlestickEngine()

                    dataframe = candlestick_engine.prepare_candles(
                        dataframe
                    )
                    
                    dataframe = candlestick_engine.detect_doji(
                        dataframe
                    )

                    app_logger.info(
                        "Doji Detection:"
                    )
                    dataframe = candlestick_engine.detect_hammer(
                        dataframe
                    )

                    app_logger.info(
                        "Hammer Detection:"
                    )

                    print(
                        dataframe[
                            [
                                "time",
                                "BODY",
                                "UPPER_WICK",
                                "LOWER_WICK",
                                "HAMMER"
                            ]
                        ]
                    )
                    
                    # -----------------------------------------
                    # Inverted Hammer Test
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_inverted_hammer(
                        dataframe
                    )

                    app_logger.info(
                        "Inverted Hammer Detection:"
                    )

                    print(
                        dataframe[
                            [
                                "time",
                                "BODY",
                                "UPPER_WICK",
                                "LOWER_WICK",
                                "INVERTED_HAMMER"
                            ]
                        ]
                    )
                    print(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BODY",
                                "RANGE",
                                "DOJI"
                            ]
                        ]
                    )

                    app_logger.info(
                        "Candlestick Preparation:"
                    )
                    # -----------------------------------------
                    # Shooting Star Test
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_shooting_star(
                        dataframe
                    )

                    app_logger.info(
                        "Shooting Star Detection:"
                    )
                    # -----------------------------------------
                    # Hanging Man Test
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_hanging_man(
                        dataframe
                    )

                    app_logger.info(
                        "Hanging Man Detection:"
                    )
                    # -----------------------------------------
                    # Spinning Top Test
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_spinning_top(
                        dataframe
                    )

                    app_logger.info(
                        "Spinning Top Detection:"
                    )

                    print(
                        dataframe[
                            [
                                "time",
                                "BODY",
                                "RANGE",
                                "UPPER_WICK",
                                "LOWER_WICK",
                                "SPINNING_TOP"
                            ]
                        ]
                    )
                    # -----------------------------------------
                    # Marubozu Test
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_marubozu(
                        dataframe
                    )

                    app_logger.info(
                        "Marubozu Detection:"
                    )
                    # -----------------------------------------
                    # Bullish Engulfing Test
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_bullish_engulfing(
                        dataframe
                    )

                    app_logger.info(
                        "Bullish Engulfing Detection:"
                    )

                    print(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BULLISH",
                                "BEARISH",
                                "BULLISH_ENGULFING"
                            ]
                        ].tail(10)
                    )
                    # -----------------------------------------
                    # Bearish Engulfing Test
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_bearish_engulfing(
                        dataframe
                    )

                    app_logger.info(
                        "Bearish Engulfing Detection:"
                    )

                    print(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BULLISH",
                                "BEARISH",
                                "BEARISH_ENGULFING"
                            ]
                        ].tail(10)
                    )
                    # -----------------------------------------
                    # Piercing Pattern Test
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_piercing_pattern(
                        dataframe
                    )

                    app_logger.info(
                        "Piercing Pattern Detection:"
                    )
                    dataframe = candlestick_engine.detect_dark_cloud_cover(
                        dataframe
                    )

                    app_logger.info(
                        "Dark Cloud Cover Detection:"
                    )

                    print(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BULLISH",
                                "BEARISH",
                                "DARK_CLOUD_COVER"
                            ]
                        ].tail(10)
                    )
                    dataframe = candlestick_engine.detect_harami(
                        dataframe=dataframe
                    )

                    app_logger.info("Harami Detection:")

                    print(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BULLISH",
                                "BEARISH",
                                "BULLISH_HARAMI",
                                "BEARISH_HARAMI",
                            ]
                        ].tail(10)
                    )
                    print(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BULLISH",
                                "BEARISH",
                                "PIERCING_PATTERN"
                            ]
                        ].tail(10)
                    )
                    print(
                        dataframe[
                            [
                                "time",
                                "BODY",
                                "UPPER_WICK",
                                "LOWER_WICK",
                                "MARUBOZU"
                            ]
                        ]
                    )
                    print(
                        dataframe[
                            [
                                "time",
                                "BODY",
                                "UPPER_WICK",
                                "LOWER_WICK",
                                "BEARISH",
                                "HANGING_MAN"
                            ]
                        ]
                    )
                    print(
                        dataframe[
                            [
                                "time",
                                "BODY",
                                "UPPER_WICK",
                                "LOWER_WICK",
                                "BEARISH",
                                "SHOOTING_STAR"
                            ]
                        ]
                    )

                    print(
                        dataframe[
                            [
                                "time",
                                "open",
                                "high",
                                "low",
                                "close",
                                "BODY",
                                "UPPER_WICK",
                                "LOWER_WICK",
                                "RANGE",
                                "BULLISH",
                                "BEARISH"
                            ]
                        ].tail(10)
                    )
                    # -----------------------------------------
                    # Morning Star Detection
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_morning_star(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Morning Star Detection:"
                    )

                    print(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BODY",
                                "BULLISH",
                                "BEARISH",
                                "MORNING_STAR"
                            ]
                        ].tail(10)
                    )
                    # -----------------------------------------
                    # Evening Star
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_evening_star(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Evening Star Detection:"
                    )

                    app_logger.info(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BULLISH",
                                "BEARISH",
                                "EVENING_STAR"
                            ]
                        ].tail(10)
                    )
                    # -----------------------------------------
                    # Three White Soldiers
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_three_white_soldiers(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Three White Soldiers Detection:"
                    )

                    app_logger.info(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BULLISH",
                                "THREE_WHITE_SOLDIERS"
                            ]
                        ].tail(10)
                    )
                    dataframe = candlestick_engine.detect_three_black_crows(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Three Black Crows Detection:"
                    )

                    app_logger.info(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BEARISH",
                                "THREE_BLACK_CROWS"
                            ]
                        ].tail(10)
                    )
                    # -----------------------------------------
                    # Tweezer Top
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_tweezer_top(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        dataframe[
                            [
                                "time",
                                "open",
                                "high",
                                "close",
                                "BULLISH",
                                "BEARISH",
                                "TWEEZER_TOP"
                            ]
                        ].tail(10)
                    )                    
                    dataframe = candlestick_engine.detect_tweezer_bottom(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Tweezer Top Detection:"
                    )
                    app_logger.info(
                    "Tweezer Bottom Detection:"
                    )

                    app_logger.info(
                        dataframe[
                            [
                                "time",
                                "open",
                                "low",
                                "close",
                                "BULLISH",
                                "BEARISH",
                                "TWEEZER_BOTTOM"
                            ]
                        ].tail(10)
                    )
                    # -----------------------------------------
                    # Inside Bar
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_inside_bar(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Inside Bar Detection:"
                    )

                    app_logger.info(
                        dataframe[
                            [
                                "time",
                                "high",
                                "low",
                                "INSIDE_BAR"
                            ]
                        ].tail(10)
                    )
                    dataframe = candlestick_engine.detect_outside_bar(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Outside Bar Detection:"
                    )

                    app_logger.info(
                        dataframe[
                            [
                                "time",
                                "high",
                                "low",
                                "OUTSIDE_BAR"
                            ]
                        ].tail(10)
                    )
                    dataframe = candlestick_engine.detect_rising_three_methods(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Rising Three Methods Detection:"
                    )

                    app_logger.info(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BULLISH",
                                "BEARISH",
                                "RISING_THREE_METHODS",
                            ]
                        ].tail(10)
                    )
                    dataframe = candlestick_engine.detect_falling_three_methods(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Falling Three Methods Detection:"
                    )

                    app_logger.info(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BULLISH",
                                "BEARISH",
                                "FALLING_THREE_METHODS",
                            ]
                        ].tail(10)
                    )
                                        # -----------------------------------------
                    # Three Inside Up
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_three_inside_up(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Three Inside Up Detection:"
                    )

                    app_logger.info(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BULLISH",
                                "BEARISH",
                                "THREE_INSIDE_UP"
                            ]
                        ].tail(10)
                    )
                                        # -----------------------------------------
                    # Three Inside Down
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_three_inside_down(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Three Inside Down Detection:"
                    )

                    app_logger.info(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BULLISH",
                                "BEARISH",
                                "THREE_INSIDE_DOWN"
                            ]
                        ].tail(10)
                    )
                                        # -----------------------------------------
                    # Tasuki Gap
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_tasuki_gap(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Tasuki Gap Detection:"
                    )

                    app_logger.info(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BULLISH",
                                "BEARISH",
                                "BULLISH_TASUKI_GAP",
                                "BEARISH_TASUKI_GAP"
                            ]
                        ].tail(10)
                    )
                    # -----------------------------------------
                    # Bullish Marubozu
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_bullish_marubozu(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Bullish Marubozu Detection:"
                    )

                    # -----------------------------------------
                    # Bearish Marubozu
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_bearish_marubozu(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Bearish Marubozu Detection:"
                    )
                    # -----------------------------------------
                    # Kicking Pattern
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_kicking_pattern(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Kicking Pattern Detection:"
                    )

                    app_logger.info(
                        dataframe[
                            [
                                "time",
                                "open",
                                "close",
                                "BULLISH_MARUBOZU",
                                "BEARISH_MARUBOZU",
                                "BULLISH_KICKING",
                                "BEARISH_KICKING"
                            ]
                        ].tail(10)
                    )
                                        # -----------------------------------------
                    # Belt Hold
                    # -----------------------------------------

                    dataframe = candlestick_engine.detect_belt_hold(
                        dataframe=dataframe
                    )

                    app_logger.info(
                        "Belt Hold Detection:"
                    )

                    app_logger.info(
                        dataframe[
                            [
                                "time",
                                "open",
                                "high",
                                "low",
                                "close",
                                "BULLISH_BELT_HOLD",
                                "BEARISH_BELT_HOLD"
                            ]
                        ].tail(10)
                    )
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
                    
                                        # -----------------------------------------
                    # Signal Generation Engine Test (M8)
                    # -----------------------------------------

                    signal_generator = SignalGenerator()

                    signal = signal_generator.generate()

                    app_logger.info(
                        "Signal Generation Engine:"
                    )

                    app_logger.info(
                        f"Signal     : {signal.signal.value}"
                    )

                    app_logger.info(
                        f"Strength   : {signal.strength}"
                    )

                    app_logger.info(
                        f"Confidence : {signal.confidence}"
                    )

                    app_logger.info(
                        f"Reason     : {signal.reason}"
                    )
                    
                    # -----------------------------------------
                    # Risk Management Engine Test (M9)
                    # -----------------------------------------

                    risk_engine = RiskEngine()

                    risk_context = RiskContext(
                        signal=signal,
                        account_balance=100000,
                        symbol=config.settings["market"]["symbol"],
                    )

                    risk_decision = risk_engine.evaluate(risk_context)

                    app_logger.info("Risk Management Engine:")

                    app_logger.info(
                        f"Decision      : {risk_decision.decision.value}"
                    )

                    app_logger.info(
                        f"Approved      : {risk_decision.approved}"
                    )

                    app_logger.info(
                        f"Position Size : {risk_decision.position.quantity}"
                    )

                    app_logger.info(
                        f"Stop Loss     : {risk_decision.stop_loss.price}"
                    )

                    app_logger.info(
                        f"Take Profit   : {risk_decision.take_profit.price}"
                    )

                    app_logger.info(
                        f"Reason        : {risk_decision.reason}"
                    )

                    # -----------------------------------------
                    # Execution Rules Engine Test (M10)
                    # -----------------------------------------

                    execution_engine = ExecutionEngine()

                    execution_decision = execution_engine.execute(
                        risk_decision
                    )

                    app_logger.info(
                        "Execution Rules Engine:"
                    )

                    app_logger.info(
                        f"Status       : {execution_decision.status.value}"
                    )

                    app_logger.info(
                        f"Approved     : {execution_decision.approved}"
                    )

                    app_logger.info(
                        f"Symbol       : {execution_decision.order.symbol}"
                    )

                    app_logger.info(
                        f"Side         : {execution_decision.order.side.value}"
                    )

                    app_logger.info(
                        f"Order Type   : {execution_decision.order.order_type.value}"
                    )

                    app_logger.info(
                        f"Volume       : {execution_decision.order.volume}"
                    )

                    app_logger.info(
                        f"Entry Price  : {execution_decision.order.entry_price}"
                    )

                    app_logger.info(
                        f"Stop Loss    : {execution_decision.order.stop_loss}"
                    )

                    app_logger.info(
                        f"Take Profit  : {execution_decision.order.take_profit}"
                    )

                    app_logger.info(
                        f"Reason       : {execution_decision.reason}"
                    )

                    # -----------------------------------------
                    # Performance Feedback Engine Test (M11)
                    # -----------------------------------------

                    performance_engine = PerformanceEngine()

                    trades = [
                        TradeResult(
                            symbol=config.settings["market"]["symbol"],
                            outcome=TradeOutcome.WIN,
                            profit_loss=150.0,
                            entry_price=250.0,
                            exit_price=260.0,
                        ),
                        TradeResult(
                            symbol=config.settings["market"]["symbol"],
                            outcome=TradeOutcome.LOSS,
                            profit_loss=-75.0,
                            entry_price=260.0,
                            exit_price=255.0,
                        ),
                        TradeResult(
                            symbol=config.settings["market"]["symbol"],
                            outcome=TradeOutcome.WIN,
                            profit_loss=100.0,
                            entry_price=255.0,
                            exit_price=265.0,
                        ),
                    ]

                    performance_context = PerformanceContext(
                        trades=trades
                    )

                    performance_decision = performance_engine.evaluate(
                        performance_context
                    )

                    app_logger.info(
                        "Performance Feedback Engine:"
                    )

                    app_logger.info(
                        f"Decision        : {performance_decision.decision.value}"
                    )

                    app_logger.info(
                        f"Approved        : {performance_decision.approved}"
                    )

                    app_logger.info(
                        f"Total Trades    : {performance_decision.metrics.total_trades}"
                    )

                    app_logger.info(
                        f"Wins            : {performance_decision.metrics.wins}"
                    )

                    app_logger.info(
                        f"Losses          : {performance_decision.metrics.losses}"
                    )

                    app_logger.info(
                        f"Breakeven       : {performance_decision.metrics.breakeven}"
                    )

                    app_logger.info(
                        f"Win Rate        : {performance_decision.metrics.win_rate:.2f}%"
                    )

                    app_logger.info(
                        f"Average Profit  : {performance_decision.metrics.average_profit}"
                    )

                    app_logger.info(
                        f"Average Loss    : {performance_decision.metrics.average_loss}"
                    )

                    app_logger.info(
                        f"Reason          : {performance_decision.reason}"
                    )

                    # ==========================================================
                    # M12 - Portfolio Management Engine
                    # ==========================================================

                    from portfolio.portfolio_engine import PortfolioEngine
                    from portfolio.portfolio_models import (
                        PortfolioContext,
                        PositionDirection,
                        PositionInfo,
                    )

                    positions = [
                        PositionInfo(
                            symbol="XAUUSD",
                            direction=PositionDirection.BUY,
                            volume=1000.0,
                            entry_price=250.0,
                            current_price=252.0,
                            floating_profit=2000.0,
                            currency="USD",
                        ),
                        PositionInfo(
                            symbol="EURUSD",
                            direction=PositionDirection.SELL,
                            volume=500.0,
                            entry_price=1.1000,
                            current_price=1.0950,
                            floating_profit=250.0,
                            currency="USD",
                        ),
                    ]

                    portfolio_context = PortfolioContext(
                        account_balance=100000.0,
                        account_equity=102250.0,
                        positions=positions,
                    )

                    portfolio_engine = PortfolioEngine()

                    portfolio_decision = portfolio_engine.evaluate(
                        portfolio_context
                    )

                    logger.info("Portfolio Management Engine:")
                    logger.info(
                        f"Decision          : "
                        f"{portfolio_decision.decision.value}"
                    )
                    logger.info(
                        f"Approved          : "
                        f"{portfolio_decision.approved}"
                    )
                    logger.info(
                        f"Open Positions    : "
                        f"{portfolio_decision.metrics.open_positions}"
                    )
                    logger.info(
                        f"Portfolio Heat    : "
                        f"{portfolio_decision.metrics.portfolio_heat:.2f}%"
                    )
                    logger.info(
                        f"Margin Level      : "
                        f"{portfolio_decision.metrics.margin_level:.2f}%"
                    )
                    logger.info(
                        f"Gross Exposure    : "
                        f"{portfolio_decision.exposure.gross_exposure}"
                    )
                    logger.info(
                        f"Net Exposure      : "
                        f"{portfolio_decision.exposure.net_exposure}"
                    )
                    logger.info(
                        f"Correlation Risk  : "
                        f"{portfolio_decision.risk.correlation_risk:.2f}%"
                    )
                    logger.info(
                        f"Risk Score        : "
                        f"{portfolio_decision.risk.risk_score:.2f}"
                    )
                    logger.info(
                        f"Reason            : "
                        f"{portfolio_decision.reason}"
                    )
                    # =================================================
                    # Strategy Optimizer Engine
                    # =================================================

                    performance = StrategyPerformance(
                        total_trades=150,
                        win_rate=45.0,
                        average_profit=180.0,
                        average_loss=-90.0,
                        drawdown=6.0,
                        profit_factor=1.40,
                        sharpe_ratio=1.20,
                    )

                    strategy_context = StrategyContext(
                        performance=performance,
                        current_parameters={
                            "risk_percent": 1.0,
                        },
                    )

                    strategy_engine = StrategyEngine()

                    strategy_decision = strategy_engine.evaluate(
                        strategy_context
                    )

                    logger.info("Strategy Optimizer Engine:")
                    logger.info(
                        f"Status             : {strategy_decision.status.value}"
                    )
                    logger.info(
                        f"Approved           : {strategy_decision.approved}"
                    )
                    logger.info(
                        f"Optimization Type  : "
                        f"{strategy_decision.recommendation.optimization_type.value}"
                    )
                    logger.info(
                        f"Current Value      : "
                        f"{strategy_decision.recommendation.current_value}"
                    )
                    logger.info(
                        f"Suggested Value    : "
                        f"{strategy_decision.recommendation.suggested_value}"
                    )
                    logger.info(
                        f"Confidence         : "
                        f"{strategy_decision.recommendation.confidence:.2f}"
                    )
                    logger.info(
                        f"Reason             : "
                        f"{strategy_decision.reason}"
                    )
                    # =================================================
                    # AI Decision Engine
                    # =================================================

                    ai_context = AIContext(
                        signal_strength=84.0,
                        risk_score=18.0,
                        performance_score=79.0,
                        portfolio_score=91.0,
                        optimization_score=85.0,
                    )

                    ai_engine = AIEngine()

                    ai_decision = ai_engine.evaluate(
                        ai_context
                    )

                    logger.info("AI Decision Engine:")

                    logger.info(
                        f"Decision           : "
                        f"{ai_decision.recommendation.decision.value}"
                    )

                    logger.info(
                        f"Approved           : "
                        f"{ai_decision.approved}"
                    )

                    logger.info(
                        f"Confidence         : "
                        f"{ai_decision.recommendation.confidence:.2f}"
                    )

                    logger.info(
                        f"Score              : "
                        f"{ai_decision.recommendation.score:.2f}"
                    )

                    logger.info(
                        f"AI Reason          : "
                        f"{ai_decision.recommendation.reason}"
                    )

                    logger.info(
                        f"Validation Reason  : "
                        f"{ai_decision.reason}"
                    )
                    # ==========================================
                    # Trading Orchestrator Engine
                    # ==========================================

                    orchestrator_engine = OrchestratorEngine()

                    trading_decision: TradingDecision = (
                        orchestrator_engine.execute()
                    )

                    logger.info("Trading Orchestrator Engine:")

                    logger.info(
                        f"Result             : "
                        f"{trading_decision.status.value}"
                    )

                    logger.info(
                        f"Approved           : "
                        f"{trading_decision.approved}"
                    )

                    logger.info(
                        f"Completed Stages   : "
                        f"{trading_decision.result.metadata.completed_stages}"
                    )

                    logger.info(
                        f"Execution Time     : "
                        f"{trading_decision.result.metadata.execution_time_ms:.3f} ms"
                    )

                    logger.info(
                        f"Reason             : "
                        f"{trading_decision.reason}"
                    )
                    # ==========================================
                    # Backtesting Engine
                    # ==========================================

                    backtest_engine = BacktestEngine()

                    backtest_context = BacktestContext(

                        strategy_name="Phoenix Strategy",

                        symbol="RELIANCE",

                        timeframe="15m",

                        initial_balance=100000.0,

                    )

                    backtest_decision: BacktestDecision = (
                        backtest_engine.run(
                            backtest_context
                        )
                    )

                    logger.info(
                        "Backtesting Engine:"
                    )

                    logger.info(
                        f"Status             : "
                        f"{backtest_decision.status.value}"
                    )

                    logger.info(
                        f"Approved           : "
                        f"{backtest_decision.approved}"
                    )

                    logger.info(
                        f"Total Trades       : "
                        f"{backtest_decision.statistics.total_trades}"
                    )

                    logger.info(
                        f"Win Rate           : "
                        f"{backtest_decision.statistics.win_rate:.2f}%"
                    )

                    logger.info(
                        f"Net Profit         : "
                        f"{backtest_decision.statistics.net_profit}"
                    )

                    profit_factor = (
                        backtest_decision.statistics.profit_factor
                    )

                    logger.info(
                        "Profit Factor      : "
                        + (
                            "Infinity"
                            if profit_factor == float("inf")
                            else f"{profit_factor:.2f}"
                        )
                    )

                    logger.info(
                        f"Drawdown           : "
                        f"{backtest_decision.statistics.max_drawdown:.2f}%"
                    )

                    logger.info(
                        f"Expectancy         : "
                        f"{backtest_decision.statistics.expectancy:.2f}"
                    )

                    logger.info(
                        f"Reason             : "
                        f"{backtest_decision.reason}"
                    )

        mt5_connection.shutdown()


if __name__ == "__main__":
    main()