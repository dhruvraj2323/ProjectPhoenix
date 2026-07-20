"""
=================================================
Project Phoenix
Broker Interface
=================================================

Abstract broker interface.
"""

from abc import ABC, abstractmethod


class BrokerInterface(ABC):
    """
    Standard interface that every broker implementation
    must follow.
    """

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def account_info(self):
        pass

    @abstractmethod
    def positions(self):
        pass

    @abstractmethod
    def orders(self):
        pass

    @abstractmethod
    def place_order(self):
        pass

    @abstractmethod
    def modify_order(self):
        pass

    @abstractmethod
    def close_order(self):
        pass

    @abstractmethod
    def cancel_order(self):
        pass

    @abstractmethod
    def symbols(self):
        pass

    @abstractmethod
    def balance(self):
        pass

    @abstractmethod
    def is_connected(self):
        pass