"""
=================================================
Project Phoenix
MT5 Initializer Test
M58
=================================================
"""

from deployment.mt5_initializer import (
    MT5Initializer,
)


def test_mt5_initializer():

    initializer = MT5Initializer()

    assert initializer.connector is not None