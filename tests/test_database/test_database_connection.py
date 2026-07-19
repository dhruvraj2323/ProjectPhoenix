"""
=================================================
Project Phoenix
Database Connection Test
=================================================
"""

from database.database_connection import (
    DatabaseConnection,
)


def run_test():

    db = DatabaseConnection()

    connection = db.connect()

    status = db.initialize()

    print("===== Database Connection =====")

    print(f"Connected     : {status.connected}")
    print(f"Initialized   : {status.initialized}")
    print(f"Database      : {status.database_name}")

    assert connection is not None
    assert status.connected
    assert status.initialized

    db.close()

    print()
    print("Database Connection Test Passed")


if __name__ == "__main__":

    run_test()