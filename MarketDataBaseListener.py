"""

File: MarketDataExampleListener.py
@author: Zack Westermann

This file contains the code for the MarketDataBaseListener which is the parent class for all market data listeners, which
are responsible for handling messages and comparing them to the configuration passed.

"""


class BaseMarketDataListener(object):

    def __init__(self, pair, alert_configs, alert_handler):
        assert isinstance(pair, str)
        self.pair = pair
        self.alert_configs = alert_configs
        self.alert_handler = alert_handler

    def get_pairs(self):
        """
        getter for pairs/product that is being tracked
        :return: self.pair (str)
        """
        return self.pair

    def receive_message(self):
        raise NotImplemented("Expects to be overwritten by child class.")
