"""
=================================================
Project Phoenix
Trading Cycle
M58.12.14
=================================================
"""

from __future__ import annotations

from deployment.live_market_data import (
    LiveMarketData,
)

from deployment.market_data_adapter import (
    MarketDataAdapter,
)

from deployment.runtime_config import (
    RuntimeConfig,
)

from market_pipeline.market_pipeline_engine import (
    MarketPipelineEngine,
)

from market_pipeline.pipeline_context import (
    PipelineContext,
)

from reporting.reporting_engine import (
    ReportingEngine,
)

from risk_engine.risk_engine import (
    RiskEngine,
)

from strategy.strategy_engine import (
    StrategyEngine,
)


class TradingCycle:
    """
    Executes one complete
    Project Phoenix trading cycle.
    """

    def __init__(
        self,
    ) -> None:

        # ==================================================
        # Market Services
        # ==================================================

        self.market = (
            LiveMarketData()
        )

        self.config = (
            RuntimeConfig()
        )

        self.market_adapter = (
            MarketDataAdapter()
        )

        self.market_data = {}

        self.candles = []

        self.pipeline_context = None

        self.current_symbol = ""

        # ==================================================
        # Runtime Status
        # ==================================================

        self.connected = False

        self.pipeline_completed = False

        self.execution_completed = False

        self.paper_trading_completed = False

        self.last_error = ""

        # ==================================================
        # Analysis Engines
        # ==================================================

        self.market_pipeline = (
            MarketPipelineEngine()
        )

        self.strategy_engine = (
            StrategyEngine()
        )

        self.risk_engine = (
            RiskEngine()
        )

        self.reporting_engine = (
            ReportingEngine()
        )

    # ==================================================
    # Initialize
    # ==================================================

    def _initialize(
        self,
    ) -> None:

        print()

        print("======================================")

        print("Starting Trading Cycle")

        print("======================================")

    # ==================================================
    # MT5 Connection
    # ==================================================

    def _connect_mt5(
        self,
    ) -> None:
        """
        Connect to MT5.
        """

        print("Step 1 : MT5 Connection")

        if not self.market.connect():

            self.last_error = (
                "MT5 Connection Failed"
            )

            raise RuntimeError(
                self.last_error
            )

        self.connected = True

    # ==================================================
    # Live Market Data
    # ==================================================

    def _load_market_data(
        self,
    ) -> None:
        """
        Download live market data.
        """

        print("Step 2 : Live Market Data")

        self.market_data = (
            self.market.get_multi_timeframe_data(
                symbol=self.current_symbol,
                bars=self.config.bars,
            )
        )

        self.candles = (
            self.market_adapter.normalize(
                self.market_data[
                    self.config.timeframe
                ]
            )
        )

        print(
            f"M15 Candles Loaded : {len(self.candles)}"
        )

    # ==================================================
    # Market Pipeline
    # ==================================================

    def _run_market_pipeline(
        self,
    ) -> None:
        """
        Execute Market Pipeline
        using live MT5 candles.
        """

        print("Step 3 : Market Pipeline")

        context = PipelineContext(

            pipeline_id="LIVE-PIPELINE",

            symbol=self.current_symbol,

            timeframe=self.config.timeframe,
        )

        context.candles = self.candles

        context = self.market_pipeline.engine.run(
            context,
        )

        if not context.approved:

            raise RuntimeError(

                f"Pipeline Failed : {context.reason}"

            )

        self.pipeline_context = context

        self.pipeline_completed = (
            context.completed
        )

        self.execution_completed = (
            context.execution_result is not None
        )

        self.paper_trading_completed = (
            context.execution_result is not None
        )

        print(
            f"Pipeline Approved : {len(context.candles)} candles"
        )

    # ==================================================
    # Validate Pipeline Output
    # ==================================================

    def _validate_pipeline_result(
        self,
    ) -> None:
        """
        Validate pipeline outputs before
        completing the trading cycle.
        """

        if self.pipeline_context is None:

            raise RuntimeError(
                "Pipeline context not available."
            )

        context = self.pipeline_context

        if len(context.candles) == 0:

            raise RuntimeError(
                "No candles available."
            )

        if not context.indicators:

            raise RuntimeError(
                "Indicators not generated."
            )

        if context.patterns is None:

            raise RuntimeError(
                "Patterns not generated."
            )

        if context.strategy_result is None:

            raise RuntimeError(
                "Strategy result missing."
            )

        if context.signals is None:

            raise RuntimeError(
                "Signal result missing."
            )

        if context.risk_result is None:

            raise RuntimeError(
                "Risk result missing."
            )

        if context.ai_result is None:

            raise RuntimeError(
                "AI result missing."
            )

        if context.execution_result is None:

            raise RuntimeError(
                "Execution result missing."
            )

        if context.portfolio_result is None:

            raise RuntimeError(
                "Portfolio result missing."
            )

        print()

        print("Pipeline Validation Passed")

    # ==================================================
    # Trading Cycle Report
    # ==================================================

    def _generate_trading_report(
        self,
    ) -> None:
        """
        Generate Trading Cycle Summary.
        """

        if self.pipeline_context is None:

            return

        context = self.pipeline_context

        print()

        print("========================================")

        print("Project Phoenix Trading Cycle Report")

        print("========================================")

        print(
            f"Symbol              : {context.symbol}"
        )

        print(
            f"Timeframe           : {context.timeframe}"
        )

        print(
            f"Candles             : {len(context.candles)}"
        )

        print(
            f"Indicators          : {len(context.indicators)}"
        )

        print(
            f"Patterns            : {len(context.patterns)}"
        )

        print(
            f"Signals             : {len(context.signals)}"
        )

        print(
            f"Pipeline Approved   : {context.approved}"
        )

        print(
            f"Decision            : {context.decision}"
        )

        print(
            f"Reason              : {context.reason}"
        )

        print("========================================")
    
    # ==================================================
    # Finish
    # ==================================================

    def _finish(
        self,
    ) -> None:
        """
        Complete Trading Cycle.
        """

        self.market.disconnect()

        print()

        print("========== SYSTEM STATUS ==========")

        print(
            f"MT5 Connected        : {self.connected}"
        )

        print(
            f"Pipeline Completed   : {self.pipeline_completed}"
        )

        print(
            f"Execution Completed  : {self.execution_completed}"
        )

        print(
            f"Paper Trading        : {self.paper_trading_completed}"
        )

        print("===================================")

        print()

        print("--------------------------------------")

        print("Trading Cycle Completed")

        print("--------------------------------------")

        print()

    # ==================================================
    # Execute
    # ==================================================

    def execute(
        self,
    ) -> bool:
        """
        Execute one complete
        Project Phoenix trading cycle.
        """

        self._initialize()

        self._connect_mt5()

        for symbol in self.config.symbols:

            print()

            print("=" * 50)

            print(
                f"Scanning : {symbol}"
            )

            print("=" * 50)

            self.current_symbol = symbol

            self._load_market_data()

            self._run_market_pipeline()

            self._validate_pipeline_result()

            self._generate_trading_report()

        self._finish()

        return True