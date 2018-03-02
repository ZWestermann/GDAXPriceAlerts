"""

File: GDAXMarketDataHandler.py
@author: Zack Westermann

The GDAXMarketDataHandler is a wrapper for the

"""


from gdax import WebsocketClient
from MarketDataBaseListener import BaseMarketDataListener

wsClient = WebsocketClient(url="wss://ws-feed.gdax.com", products="ETH-USD")


class MarketDataHandler(WebsocketClient):

    def __init__(self, url, pair, listener):
        assert issubclass(listener, BaseMarketDataListener)
        assert isinstance(pair, str)
        WebsocketClient.__init__(self, url=url, products=pair, message_type="subscribe")
        self._listener = listener
        self.message_count = 0
        self.pair = pair

    def on_open(self):
        print("Subscribed to %s" % self.products)

    def on_message(self, msg):
        self._listener.receive_message(msg)
        self.message_count += 1

    def on_close(self):
        print("Handled %s messages for product(s): %s" % (self.message_count, self.pair))
