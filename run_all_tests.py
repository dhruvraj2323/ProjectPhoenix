"""
=================================================
Project Phoenix
Run All Tests
=================================================
"""

import subprocess
import sys


TEST_MODULES = [

# =================================================
# M8 - Signal Generation
# =================================================

"tests/test_signals/test_signal_rules.py",
"tests/test_signals/test_signal_strength.py",
"tests/test_signals/test_signal_validator.py",
"tests/test_signals/test_signal_filters.py",
"tests/test_signals/test_signal_logger.py",
"tests/test_signals/test_signal_generator.py",

# =================================================
# M9 - Risk Management
# =================================================

"tests/test_risk/test_risk_position.py",
"tests/test_risk/test_risk_stoploss.py",
"tests/test_risk/test_risk_takeprofit.py",
"tests/test_risk/test_risk_validator.py",
"tests/test_risk/test_risk_engine.py",

# =================================================
# M10 - Execution Engine
# =================================================

"tests/test_execution/test_execution_models.py",
"tests/test_execution/test_execution_rules.py",
"tests/test_execution/test_execution_validator.py",
"tests/test_execution/test_execution_engine.py",

# =================================================
# M11 - Performance Engine
# =================================================

"tests/test_performance/test_performance_models.py",
"tests/test_performance/test_performance_metrics.py",
"tests/test_performance/test_performance_analyzer.py",
"tests/test_performance/test_performance_validator.py",
"tests/test_performance/test_performance_engine.py",

# =================================================
# M12 - Market
# =================================================

"tests/test_market/test_mt5_connector.py",
"tests/test_market/test_market_data.py",

# =================================================
# M13 - Indicators
# =================================================

"tests/test_indicators/test_indicator_engine.py",
"tests/test_indicators/test_candlestick_engine.py",

# =================================================
# M14 - Database
# =================================================

"tests/test_database/test_database_models.py",
"tests/test_database/test_database_connection.py",
"tests/test_database/test_database_repository.py",
"tests/test_database/test_database_logger.py",
"tests/test_database/test_database_engine.py",

# =================================================
# M15 - Configuration
# =================================================

"tests/test_config/test_config_models.py",
"tests/test_config/test_config_loader.py",
"tests/test_config/test_config_validator.py",
"tests/test_config/test_config_logger.py",
"tests/test_config/test_config_engine.py",

# =================================================
# M16 - Strategy Optimizer
# =================================================

"tests/test_strategy_optimizer/test_strategy_models.py",
"tests/test_strategy_optimizer/test_strategy_analyzer.py",
"tests/test_strategy_optimizer/test_strategy_optimizer.py",
"tests/test_strategy_optimizer/test_strategy_validator.py",
"tests/test_strategy_optimizer/test_strategy_logger.py",
"tests/test_strategy_optimizer/test_strategy_engine.py",

# =================================================
# M17 - Backtesting
# =================================================

"tests/test_backtesting/test_backtest_models.py",
"tests/test_backtesting/test_backtest_simulator.py",
"tests/test_backtesting/test_backtest_statistics.py",
"tests/test_backtesting/test_backtest_validator.py",
"tests/test_backtesting/test_backtest_logger.py",
"tests/test_backtesting/test_backtest_engine.py",

# =================================================
# M18 - AI
# =================================================

"tests/test_ai/test_ai_models.py",
"tests/test_ai/test_ai_reasoning.py",
"tests/test_ai/test_ai_scoring.py",
"tests/test_ai/test_ai_validator.py",
"tests/test_ai/test_ai_logger.py",
"tests/test_ai/test_ai_engine.py",

# =================================================
# M19 - Learning
# =================================================

"tests/test_learning/test_learning_models.py",
"tests/test_learning/test_learning_patterns.py",
"tests/test_learning/test_learning_recommender.py",
"tests/test_learning/test_learning_validator.py",
"tests/test_learning/test_learning_logger.py",
"tests/test_learning/test_learning_engine.py",

# =================================================
# M20 - Reporting
# =================================================

"tests/test_reporting/test_reporting_models.py",
"tests/test_reporting/test_report_generator.py",
"tests/test_reporting/test_analytics_engine.py",
"tests/test_reporting/test_reporting_logger.py",
"tests/test_reporting/test_reporting_engine.py",

# =================================================
# M21 - Portfolio
# =================================================

"tests/test_portfolio/test_portfolio_models.py",
"tests/test_portfolio/test_portfolio_allocator.py",
"tests/test_portfolio/test_portfolio_exposure.py",
"tests/test_portfolio/test_portfolio_correlation.py",
"tests/test_portfolio/test_portfolio_analyzer.py",
"tests/test_portfolio/test_portfolio_validator.py",
"tests/test_portfolio/test_portfolio_logger.py",
"tests/test_portfolio/test_portfolio_engine.py",

# =================================================
# M22 - Market Adapter
# =================================================

"tests/test_market_adapter/test_market_adapter_models.py",
"tests/test_market_adapter/test_market_data_provider.py",
"tests/test_market_adapter/test_market_adapter_factory.py",
"tests/test_market_adapter/test_market_adapter_logger.py",
"tests/test_market_adapter/test_market_adapter_engine.py",

# =================================================
# M23 - Broker
# =================================================

"tests/test_broker/test_broker_models.py",
"tests/test_broker/test_broker_interface.py",
"tests/test_broker/test_broker_factory.py",
"tests/test_broker/test_broker_logger.py",
"tests/test_broker/test_broker_engine.py",

# =================================================
# M24 - Paper Trading
# =================================================

"tests/test_paper_trading/test_paper_models.py",
"tests/test_paper_trading/test_paper_order_manager.py",
"tests/test_paper_trading/test_paper_portfolio.py",
"tests/test_paper_trading/test_paper_logger.py",
"tests/test_paper_trading/test_paper_engine.py",

# =================================================
# M25 - Live Trading
# =================================================

"tests/test_live_trading/test_live_models.py",
"tests/test_live_trading/test_live_order_manager.py",
"tests/test_live_trading/test_live_portfolio.py",
"tests/test_live_trading/test_live_logger.py",
"tests/test_live_trading/test_live_engine.py",

# =================================================
# M26 - Dashboard
# =================================================

"tests/test_dashboard/test_dashboard_models.py",
"tests/test_dashboard/test_dashboard_controller.py",
"tests/test_dashboard/test_dashboard_renderer.py",
"tests/test_dashboard/test_dashboard_logger.py",
"tests/test_dashboard/test_dashboard_engine.py",

# =================================================
# M27 - Alert System
# =================================================

"tests/test_alert_system/test_alert_models.py",
"tests/test_alert_system/test_alert_formatter.py",
"tests/test_alert_system/test_alert_sender.py",
"tests/test_alert_system/test_alert_logger.py",
"tests/test_alert_system/test_alert_engine.py",

# =================================================
# M28 - Scheduler
# =================================================

"tests/test_scheduler/test_scheduler_models.py",
"tests/test_scheduler/test_scheduler_tasks.py",
"tests/test_scheduler/test_scheduler_queue.py",
"tests/test_scheduler/test_scheduler_logger.py",
"tests/test_scheduler/test_scheduler_engine.py",

# =================================================
# M29 - Deployment
# =================================================

"tests/test_deployment/test_deployment_models.py",
"tests/test_deployment/test_runtime_manager.py",
"tests/test_deployment/test_health_monitor.py",
"tests/test_deployment/test_deployment_logger.py",
"tests/test_deployment/test_deployment_engine.py",

]


# =================================================
# RUN ALL TESTS
# =================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Project Phoenix - Running All Tests")
    print("=" * 60)

    failed_tests = []

    for test_module in TEST_MODULES:

        print("\nRunning:", test_module)

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                test_module
            ]
        )

        if result.returncode != 0:
            failed_tests.append(test_module)


    print("\n" + "=" * 60)
    print("TEST EXECUTION COMPLETE")
    print("=" * 60)


    if failed_tests:

        print("\nFAILED TESTS:")

        for test in failed_tests:
            print("-", test)

        sys.exit(1)

    else:

        print("\nALL TESTS PASSED SUCCESSFULLY")

        sys.exit(0)