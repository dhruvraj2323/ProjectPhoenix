"""
=================================================
Project Phoenix
Database Repository Test
=================================================
"""

from database.database_connection import (
    DatabaseConnection,
)

from database.database_repository import (
    DatabaseRepository,
)


def run_test():

    db = DatabaseConnection()

    connection = db.connect()

    repository = DatabaseRepository(connection)

    repository.insert_trade(

        trade_id=1,

        symbol="EURUSD",

        direction="BUY",

        profit=125.50,

    )

    trade = repository.get_trade(1)

    trades = repository.get_all_trades()

    print("===== Database Repository =====")

    print(f"Trade ID   : {trade[0]}")
    print(f"Symbol     : {trade[1]}")
    print(f"Direction  : {trade[2]}")
    print(f"Profit     : {trade[3]}")

    print()

    print(f"Total Trades : {len(trades)}")

    assert trade[0] == 1

    assert trade[1] == "EURUSD"

    assert trade[2] == "BUY"

    assert len(trades) >= 1

    db.close()

    print()

    print("Database Repository Test Passed")


if __name__ == "__main__":

    run_test()