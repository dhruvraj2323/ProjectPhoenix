"""
=================================================
Project Phoenix
Trading Cycle
M58.12.15
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

from reporting.trade_record_mapper import (
    TradeRecordMapper,
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

        # ==================================================
        # Reporting Services
        # ==================================================

        self.reporting_engine = (
            ReportingEngine()
        )

        self.trade_record_mapper = (
            TradeRecordMapper()
        )

        self.trade_records = []

        self.daily_report = None

    # ==================================================
    # Initialize
    # ==================================================

    def _initialize(
        self,
    ) -> None:

        print()

        print(
            "======================================"
        )

        print(
            "Starting Trading Cycle"
        )

        print(
            "======================================"
        )

    # ==================================================
    # MT5 Connection
    # ==================================================

    def _connect_mt5(
        self,
    ) -> None:
        """
        Connect to MT5.
        """

        print(
            "Step 1 : MT5 Connection"
        )

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

        print(
            "Step 2 : Live Market Data"
        )

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
            f"M15 Candles Loaded : "
            f"{len(self.candles)}"
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

        print(
            "Step 3 : Market Pipeline"
        )

        context = PipelineContext(

            pipeline_id="LIVE-PIPELINE",

            symbol=self.current_symbol,

            timeframe=self.config.timeframe,
        )

        context.candles = self.candles

        context = (
            self.market_pipeline.engine.run(
                context,
            )
        )

        if not context.approved:

            raise RuntimeError(

                f"Pipeline Failed : "
                f"{context.reason}"

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
            f"Pipeline Approved : "
            f"{len(context.candles)} candles"
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

        print(
            "Pipeline Validation Passed"
        )

    # ==================================================
    # Collect Execution Record
    # ==================================================

    def _collect_execution_record(
        self,
    ) -> None:
        """
        Convert a successful execution context
        into a TradeRecord and store it for the
        consolidated trading-cycle report.

        A rejected or non-executed pipeline is a
        valid trading-cycle outcome and therefore
        does not create a TradeRecord.
        """

        if self.pipeline_context is None:

            raise RuntimeError(
                "Pipeline context not available."
            )

        context = self.pipeline_context

        # --------------------------------------------------
        # Execution Result
        # --------------------------------------------------

        execution_result = (
            context.execution_result
        )

        if execution_result is None:

            print()

            print(
                "No execution result available."
            )

            return

        # --------------------------------------------------
        # No Executed Trade
        #
        # Rejected execution is a valid cycle outcome.
        # Do not create a TradeRecord.
        # --------------------------------------------------

        if not execution_result.accepted:

            print()

            print(
                "No executed trade for this cycle."
            )

            print(
                "Execution Status : "
                f"{execution_result.status}"
            )

            return

        # --------------------------------------------------
        # Map ExecutionContext -> TradeRecord
        # --------------------------------------------------

        trade_record = (
            self.trade_record_mapper.map(
                context,
            )
        )

        # --------------------------------------------------
        # Store Trade Record
        # --------------------------------------------------

        self.trade_records.append(
            trade_record,
        )

        print()

        print(
            "===== TRADE RECORD COLLECTED ====="
        )

        print(
            f"Trade ID    : "
            f"{trade_record.trade_id}"
        )

        print(
            f"Symbol      : "
            f"{trade_record.symbol}"
        )

        print(
            f"Direction   : "
            f"{trade_record.direction}"
        )

        print(
            f"Entry Price : "
            f"{trade_record.entry_price}"
        )

        print(
            f"Volume      : "
            f"{trade_record.volume}"
        )

        print(
            f"Status      : "
            f"{trade_record.status}"
        )

        print(
            "=================================="
        )

    # ==================================================
    # Consolidated Trading Report
    # ==================================================

    def _generate_consolidated_report(
        self,
    ) -> None:
        """
        Generate one consolidated report for
        all executed trades in the trading cycle.
        """

        if not self.trade_records:

            print()

            print(
                "No executed trades found."
            )

            return

        self.daily_report = (
            self.reporting_engine.run(
                self.trade_records,
            )
        )

        print()

        print(
            "===== CONSOLIDATED REPORT ====="
        )

        print(
            f"Trades Reported : "
            f"{len(self.trade_records)}"
        )

        print(
            f"Report File     : "
            f"{self.daily_report.output_file}"
        )

        print(
            "==============================="
        )

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

        print(
            "========================================"
        )

        print(
            "Project Phoenix Trading Cycle Report"
        )

        print(
            "========================================"
        )

        print(
            f"Symbol              : "
            f"{context.symbol}"
        )

        print(
            f"Timeframe           : "
            f"{context.timeframe}"
        )

        print(
            f"Candles             : "
            f"{len(context.candles)}"
        )

        print(
            f"Indicators          : "
            f"{len(context.indicators)}"
        )

        print(
            f"Patterns            : "
            f"{len(context.patterns)}"
        )

        print(
            f"Signals             : "
            f"{len(context.signals)}"
        )

        print(
            f"Pipeline Approved   : "
            f"{context.approved}"
        )

        print(
            f"Decision            : "
            f"{context.decision}"
        )

        print(
            f"Reason              : "
            f"{context.reason}"
        )

        print(
            "========================================"
        )

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

        print(
            "========== SYSTEM STATUS =========="
        )

        print(
            f"MT5 Connected        : "
            f"{self.connected}"
        )

        print(
            f"Pipeline Completed   : "
            f"{self.pipeline_completed}"
        )

        print(
            f"Execution Completed  : "
            f"{self.execution_completed}"
        )

        print(
            f"Paper Trading        : "
            f"{self.paper_trading_completed}"
        )

        print(
            "==================================="
        )

        print()

        print(
            "--------------------------------------"
        )

        print(
            "Trading Cycle Completed"
        )

        print(
            "--------------------------------------"
        )

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

        # --------------------------------------------------
        # Reset Cycle-Level Trade Collection
        # --------------------------------------------------

        self.trade_records = []

        self.daily_report = None

        # --------------------------------------------------
        # Process All Configured Symbols
        # --------------------------------------------------

        for symbol in self.config.symbols:

            print()

            print(
                "=" * 50
            )

            print(
                f"Scanning : {symbol}"
            )

            print(
                "=" * 50
            )

            self.current_symbol = symbol

            self._load_market_data()

            self._run_market_pipeline()

            self._validate_pipeline_result()

            self._collect_execution_record()

            self._generate_trading_report()

        # --------------------------------------------------
        # Generate One Consolidated Report
        # --------------------------------------------------

        self._generate_consolidated_report()

        # --------------------------------------------------
        # Finish
        # --------------------------------------------------

        self._finish()

        return True