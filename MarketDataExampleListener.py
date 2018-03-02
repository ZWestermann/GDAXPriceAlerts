"""

File: MarketDataExampleListener.py
@author: Zack Westermann

This file contains the code for the MarketDataExampleListener object which handles market data in a JSON format, looks
at the max/min trade price passed in, and returns an alert if the trade price is outside of the bounds set by the configs.
Sample Message:

{'type': 'open', 'side': 'buy', 'price': '1160.44000000',
 'order_id': 'c76658d2-4695-455b-936d-a358777e6b32',
  'remaining_size': '0.04000000', 'product_id': 'ETH-USD',
   'sequence': 2255329417, 'time': '2018-01-29T17:17:43.874000Z'}

In this example, the listener triggers an alert if a trade price exceeds the max or min config price.

"""

from MarketDataBaseListener import BaseMarketDataListener


class MarketDataExampleListener(BaseMarketDataListener):

    def __init__(self, pair, alert_configs, alert_handler, logger):
        assert isinstance(alert_configs, dict)
        assert isinstance(pair, str)
        BaseMarketDataListener.__init__(self, pair, alert_configs, alert_handler)
        self.pair = pair
        self._latest_trade_price = None
        self._second_latest_trade_price = None
        self._params = alert_configs
        "params is a dict expecting the keys" \
        "min price: min price to send alert" \
        "max price: max price to send alert" \
        "update_on_trigger: whether to reset the alert on the price fluctuation of the new price of the trigger." \
        "percent_fluc_on_trigger:"
        self.email_handler = alert_handler
        self.logger = logger
        self.alert_triggered = False


    @staticmethod
    def get_percentage_difference(old_price, new_price):
        if isinstance(old_price, float) and isinstance(new_price, float):
            return round((((new_price - old_price) / old_price) * 100), 4)
        else:
            return "not enough data to calculate"

    def receive_message(self, message):
        if 'reason' not in message.keys():
            return
        if message['reason'] == 'filled' and 'price' in message.keys():
            self._second_latest_trade_price = self._latest_trade_price
            self._latest_trade_price = float(message['price'])
            price_change = self.get_percentage_difference(self._second_latest_trade_price,
                                                          self._latest_trade_price)
            print("Trade: %s Price: %s, Percent Change: %s" % (message['side'], message['price'], price_change))
            if self._latest_trade_price < self._params['min price']:
                message = "%s min price eclipsed: %s, sending message" % (self.get_ticker(), self._latest_trade_price)
                if self.alert_triggered is False:
                    self.email_handler.send_message(message, 'Price Alert Triggered: %s, Trigger Price: %s,'
                                                             ' L Trade Price: %s' %
                                                    (self.get_ticker(), self._params['min price'], self._latest_trade_price))
                    self.logger.info("Trigger alert: %s sent to %s" % (message, self.email_handler.get_destination_addresses()))
                    self.alert_triggered = True
                self.logger.info("%s min price eclipsed: %s, sending message" % (self.get_pair(), self._latest_trade_price))
            elif self._latest_trade_price > self._params['max price']:
                self.logger.info("%s max price eclipsed: %s" % (self.get_ticker(), self._latest_trade_price))
