"""
=================================================
Project Phoenix
Database Connection
=================================================

Manages SQLite database connection.
"""

import sqlite3
from pathlib import Path

from database.database_models import DatabaseStatus


DATABASE_NAME = (
    Path(__file__).resolve().parent
    / "project_phoenix.db"
)


class DatabaseConnection:
    """
    Handles SQLite database connection.
    """

    def __init__(self):

        self.database_path = DATABASE_NAME

        self.connection = None

    # -------------------------------------------------

    def connect(self):

        self.connection = sqlite3.connect(
            self.database_path
        )

        return self.connection

    # -------------------------------------------------

    def initialize(self):

        if self.connection is None:

            self.connect()

        return DatabaseStatus(
            connected=True,
            initialized=True,
            database_name=self.database_path.name,
        )

    # -------------------------------------------------

    def close(self):

        if self.connection:

            self.connection.close()

            self.connection = None