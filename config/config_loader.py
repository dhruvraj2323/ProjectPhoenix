"""
Project Phoenix
Milestone M18 - Configuration & Settings Engine

Module:
    config_loader.py

Purpose:
    Loads default Project Phoenix
    configuration.
"""

from __future__ import annotations

from config.config_models import (
    ConfigurationContext,
    ConfigurationItem,
)


class ConfigurationLoader:
    """
    Loads default configuration.
    """

    def load(
        self,
        context: ConfigurationContext,
    ) -> list[ConfigurationItem]:
        """
        Load configuration items.
        """

        defaults = [

            ConfigurationItem(

                key="risk_percent",

                value=1.0,

                category="Risk",

                description="Maximum risk per trade.",

            ),

            ConfigurationItem(

                key="signal_strength",

                value=70,

                category="Signal",

                description="Minimum signal strength.",

            ),

            ConfigurationItem(

                key="portfolio_limit",

                value=10,

                category="Portfolio",

                description="Maximum open positions.",

            ),

            ConfigurationItem(

                key="strategy_mode",

                value="Adaptive",

                category="Strategy",

                description="Strategy execution mode.",

            ),

            ConfigurationItem(

                key="ai_enabled",

                value=True,

                category="AI",

                description="Enable AI decision engine.",

            ),

            ConfigurationItem(

                key="execution_timeout",

                value=5,

                category="Execution",

                description="Execution timeout in seconds.",

            ),

            ConfigurationItem(

                key="performance_window",

                value=30,

                category="Performance",

                description="Performance evaluation window.",

            ),

            ConfigurationItem(

                key="learning_enabled",

                value=True,

                category="Learning",

                description="Enable Learning Engine.",

            ),

        ]

        return defaults