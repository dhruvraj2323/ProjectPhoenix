"""
Project Phoenix

Unit Test
Portfolio Allocator
"""

from portfolio.portfolio_allocator import (
    PortfolioAllocator,
)


def test_portfolio_allocator():

    allocator = PortfolioAllocator()

    allocation = allocator.allocate(
        total_capital=10000.0,
        allocation_percent=10.0,
    )

    assert allocation.capital_used == 1000.0

    assert allocation.capital_available == 9000.0

    assert allocation.allocation_percent == 10.0

    print("===== Portfolio Allocator Test =====")
    print(f"Capital Used      : {allocation.capital_used}")
    print(f"Capital Available : {allocation.capital_available}")
    print(f"Allocation %      : {allocation.allocation_percent}")
    print(f"Risk Used         : {allocation.risk_used}")
    print(f"Risk Available    : {allocation.risk_available}")
    print()
    print("Portfolio Allocator Test Passed")


if __name__ == "__main__":

    test_portfolio_allocator()