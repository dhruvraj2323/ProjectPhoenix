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