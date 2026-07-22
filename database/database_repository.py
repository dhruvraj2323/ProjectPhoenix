"""
=================================================
Project Phoenix
Database Repository
=================================================

Repository layer responsible for CRUD
operations.
"""

import sqlite3


class DatabaseRepository:
    """
    Repository for database CRUD operations.
    """

    def __init__(self, connection: sqlite3.Connection):

        self.connection = connection

        self.cursor = self.connection.cursor()

        self.create_tables()

    # -------------------------------------------------

    def create_tables(self):

        # -----------------------------
        # Trades
        # -----------------------------

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS trades (

                trade_id INTEGER PRIMARY KEY,

                symbol TEXT,

                direction TEXT,

                profit REAL

            )
            """
        )

        # -----------------------------
        # Signals
        # -----------------------------

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS signals (

                signal_id INTEGER PRIMARY KEY,

                symbol TEXT,

                signal_type TEXT,

                strength INTEGER,

                confidence REAL,

                timestamp TEXT

            )
            """
        )

        # -----------------------------
        # Performance
        # -----------------------------

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS performance (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                total_trades INTEGER,

                win_rate REAL,

                net_profit REAL,

                profit_factor REAL,

                drawdown REAL,

                expectancy REAL,

                timestamp TEXT

            )
            """
        )

        # -----------------------------
        # Learning
        # -----------------------------

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS learning (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                recommendation_type TEXT,

                current_value REAL,

                suggested_value REAL,

                confidence REAL,

                reason TEXT,

                timestamp TEXT

            )
            """
        )

        # -----------------------------
        # Configuration
        # -----------------------------

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS configuration (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT,

                value TEXT,

                environment TEXT,

                version TEXT

            )
            """
        )

        self.connection.commit()

    # -------------------------------------------------

    def insert_trade(
        self,
        trade_id: int,
        symbol: str,
        direction: str,
        profit: float,
    ):

        self.cursor.execute(

            """
            INSERT OR REPLACE INTO trades

            VALUES (?, ?, ?, ?)

            """,

            (
                trade_id,
                symbol,
                direction,
                profit,
            ),

        )

        self.connection.commit()

    # -------------------------------------------------

    def get_trade(self, trade_id: int):

        self.cursor.execute(

            """
            SELECT *

            FROM trades

            WHERE trade_id = ?

            """,

            (trade_id,),

        )

        return self.cursor.fetchone()

    # -------------------------------------------------

    def get_all_trades(self):

        self.cursor.execute(

            """
            SELECT *

            FROM trades

            ORDER BY trade_id

            """

        )

        return self.cursor.fetchall()