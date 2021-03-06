__author__ = 'michaelstarin'

import time
from datetime import datetime
from datetime import timedelta

import httplib
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import threading
import urllib
from Restful import RestfulAPI
from ReversalMinMax import Reversal
from Support_Resistance import SRZones
from pandas.io.json import json_normalize


class RSS1:
    def __init__(self, granularity, count, sleeptime, currency_pair,
                 oanda_account_id, oanda_access_token, domain, oanda, sensitivity_range, srzone_range):
        self.granularity = granularity
        self.count = count
        self.sleeptime = sleeptime
        self.currency_pair = currency_pair
        self.oanda_account_id = oanda_account_id
        self.oanda_access_token = oanda_access_token
        self.price_type1 = 'closeAsk'
        self.price_type2 = 'openAsk'
        self.oanda = oanda
        self.array = None
        self.now = None
        self.now_min = None
        self.domain = domain
        self.sensitivity_range = sensitivity_range
        self.srzone_range = srzone_range
        self.minutes = 5
        self.seconds = 60
        global close_ask_array
        global open_ask_array

    def main_fx(self):
        print 'Currency Pair is ', self.currency_pair

        while True:
            self.now = datetime.utcnow()
            self.now_min = self.now - timedelta(microseconds=self.now.microsecond)

            # if self.now_min.minute % 5 == 0 and self.now_min.second < 8 and self.now_min.second > 3:
            if True:
                while True:
                    self.now = datetime.utcnow()
                    self.now_rounded = self.now - timedelta(minutes=self.now.minute % self.minutes,
                                                            seconds=self.now.second % self.seconds,
                                                            microseconds=self.now.microsecond)
                    print ' The time is now rounded ', self.now_rounded

                    # fetch historical candlestick data
                    instance2 = RestfulAPI(self.granularity, self.count, self.currency_pair, self.oanda_account_id,
                                           self.oanda_access_token, self.domain, self.now)
                    self.array = instance2.get_restful_price()
                    global close_ask_array
                    global open_ask_array

                    close_ask_array = np.array(self.array[self.price_type1][0:len(self.array)])
                    open_ask_array = np.array(self.array[self.price_type2][0:len(self.array)])
                    print 'self.close_ask_array = np.array(self.array[self.price_type1][0:len(self.array)]) in Main', close_ask_array
                    print 'self.open_ask_array = np.array(self.array[self.price_type2][0:len(self.array)]) in Main', open_ask_array

                    # fetch array of support and resistance levels
                    instance3 = Reversal(close_ask_array, self.sensitivity_range)
                    locations = instance3.reversal_m_m()
                    instance4 = SRZones(locations, self.currency_pair, self.srzone_range)
                    sr1_ar = instance4.sup_rest()
                    condition = True

                    print 'SR1_AR ', sr1_ar
                    print 'a[-1] is ', close_ask_array[-1]
                    print 'a[-2] is ', close_ask_array[-2]
                    print 'a[-3] is ', close_ask_array[-3]

                    # Parse through each S/R level
                    for t in range(0, len(sr1_ar)):
                        # Does price break through resistance level
                        if (close_ask_array[-1] >= (sr1_ar[t] + .00001)) & (
                                    close_ask_array[-2] <= (sr1_ar[t] - .00001)):

                            print 'support line is ', sr1_ar[t]
                            print 'breakthrough up'
                            condition = False
                            inst1 = RSS1(self.granularity, self.count, self.sleeptime, self.currency_pair,
                                         self.oanda_account_id,
                                         self.oanda_access_token, self.domain, self.oanda, self.sensitivity_range,
                                         self.srzone_range)

                            rss = threading.Thread(target=inst1.reversal_min, args=(sr1_ar[t], close_ask_array[-1]))
                            rss.daemon = True
                            rss.start()

                        # Does price break through support level
                        elif (close_ask_array[-1] <= (sr1_ar[t] - .00001)) & (
                                    close_ask_array[-2] >= (sr1_ar[t] + .00001)):

                            print 'resistance line is ', sr1_ar[t]
                            print 'breakthrough down'
                            condition = False
                            inst2 = RSS1(self.granularity, self.count, self.sleeptime, self.currency_pair,
                                         self.oanda_account_id,
                                         self.oanda_access_token, self.domain, self.oanda, self.sensitivity_range,
                                         self.srzone_range)

                            rss = threading.Thread(target=inst2.reversal_max, args=(sr1_ar[t], close_ask_array[-1]))
                            rss.daemon = True
                            rss.start()

                        else:
                            pass

                        if condition:
                            pass
                        if not condition:
                            break
                    if condition:
                        print 'no crossover'

                    time.sleep(self.seconds)
                    break
            else:
                time.sleep(self.seconds / 15.0)

    def reversal_max(self, resistance_line, crossover_price):

        scope = 1
        condition = False
        condition_met = False
        global close_ask_array
        global open_ask_array

        # Wait 5 min for next candle to close
        time.sleep(305)
        # Condition searching loop time
        t_end = time.time() + 5400

        while time.time() < t_end:

            a = close_ask_array[-scope:]
            b = open_ask_array[-scope:]
            print 'a = self.close_ask_array[-scope:] in reversal Max ', a
            print 'b = self.open_ask_array[-scope:] in reversal Max ', b
            scope += 1

            # Last close price for candlestick in array
            latest_close_price = a[-1]
            # Last open price for candlestick in array
            latest_open_price = b[-1]

            if latest_close_price >= resistance_line + .0001:
                print 'got out of loop because close_price is ', latest_close_price
                print ' '
                break

            pass_down = min(a)
            print 'pass_down is ', pass_down

            # Check to see if most recent candle fails to close above resistance line
            if (latest_close_price <= (resistance_line + .0001)) & (
                        latest_close_price >= (resistance_line - .0003)) and (
                        latest_open_price < latest_close_price) and (
                        (resistance_line - pass_down) >= .0004):

                time.sleep(self.sleeptime)

                # Don't grab whole array just grab most recent candlestick of info

                next_close = close_ask_array[-1]
                next_open = open_ask_array[-1]
                print 'next_close = self.close_ask_array[-1] in reversal Max ', next_close
                print 'next_open = self.open_ask_array[-1] in reversal Max ', next_open

                response = self.oanda.get_prices(instruments=self.currency_pair)
                prices = response.get("prices")
                ask = prices[0].get("ask")
                bid = prices[0].get("bid")
                spread = ask - bid

                print 'spread ', spread
                if spread > .0003:
                    break

                # If next candle has a lower close_ask then open_ask then a short is entered.
                if (next_close < next_open) and (next_open < resistance_line) and (next_open - next_close <= .0004):

                    fiveMin_streaming_time = 0

                    short_price1 = self.oanda.create_order(6980117, instrument=self.currency_pair, units=13000,
                                                           side='sell',
                                                           type='market')
                    short_price2 = self.oanda.create_order(6980117, instrument=self.currency_pair, units=13000,
                                                           side='sell',
                                                           type='market')
                    short_price3 = self.oanda.create_order(6980117, instrument=self.currency_pair, units=13000,
                                                           side='sell',
                                                           type='market')

                    # Fetch trade position ID's
                    conn = httplib.HTTPSConnection("api-fxpractice.oanda.com")
                    params = urllib.urlencode({"instrument": self.currency_pair, })
                    headers = {"Content-Type": "application/x-www-form-urlencoded",
                               "Authorization": "Bearer 74b91ee3fda0251126b3d4a319067b88-7a70489e0dd38f5e6994ddda09b0e1ca"}
                    url = "/v1/accounts/6980117/trades?instrument=" + self.currency_pair + "&count=3"
                    conn.request("GET", url, params, headers)
                    price_action = conn.getresponse().read()
                    data = json.loads(price_action)
                    data_frame = json_normalize(data)
                    array = np.array(data_frame['trades'][0:len(data_frame)])
                    trade_id1 = array[0][2][u'id']
                    trade_id2 = array[0][1][u'id']
                    trade_id3 = array[0][0][u'id']

                    pickleDirRoot = '/Users/michaelstarin/Desktop/FOREX1/trading_graphs'
                    pickleDirDate = str(self.now)
                    pickleFileRoot = pickleDirRoot + '/' + pickleDirDate + '/' + self.currency_pair

                    try:
                        os.makedirs(pickleFileRoot)
                    except OSError:
                        pass

                    plt.axhline(y=resistance_line, color='red')
                    plt.xlim([0, 400])

                    plt.plot(close_ask_array[-400:], color='green')

                    plt.savefig(pickleFileRoot)

                    print 'SELL'

                    now = datetime.utcnow()
                    print ' The time is now rounded ', now
                    # Trade status: If True = position is closed, if False = position is open
                    trade_id1_status = False
                    trade_id2_status = False
                    trade_id3_status = False

                    while True:

                        streaming_time = 1
                        fiveMin_streaming_time += streaming_time
                        time.sleep(.05)

                        if fiveMin_streaming_time % 1200 == 0:
                            now = datetime.utcnow()
                            print ' The time is now rounded ', now
                            response = self.oanda.get_prices(instruments=self.currency_pair)
                            prices = response.get("prices")
                            short_price2 = short_price1[u'price']
                            buy_back_price = prices[0].get("ask")

                            # Cut losses
                            if (buy_back_price - short_price2) >= .0005 and trade_id1_status == False:
                                # close_order
                                print 'trade_id1 ', trade_id1
                                self.oanda.close_trade(6980117, trade_id1)
                                trade_id1_status = True
                                print 'short price ', short_price2
                                print 'buy back price ', buyBackprice
                                condition_met = True

                            if (
                                        buyBackprice - short_price2) >= .0005 and trade_id2_status == False and trade_id3_status == False:
                                # close_order
                                print 'trade_id2 ', trade_id2
                                print 'trade_id3 ', trade_id3
                                self.oanda.close_trade(6980117, trade_id2)
                                self.oanda.close_trade(6980117, trade_id3)
                                trade_id2_status = True
                                trade_id3_status = True

                                print 'short price ', short_price2
                                print 'buy back price ', buyBackprice
                                condition_met = True
                                break

                        if fiveMin_streaming_time % 1200 == 0 or fiveMin_streaming_time % 1 == 0:
                            response = self.oanda.get_prices(instruments=self.currency_pair)
                            prices = response.get("prices")

                            short_price2 = short_price1[u'price']
                            buyBackprice = prices[0].get("ask")
                            # Take the profit
                            if (short_price2 - buyBackprice) >= .0008 and trade_id1_status == False and \
                                            trade_id2_status == False:
                                # close_order
                                self.oanda.close_trade(6980117, trade_id1)
                                self.oanda.close_trade(6980117, trade_id2)
                                trade_id1_status = True
                                trade_id2_status = True

                                # Trade_id3 has a stop-loss of 5
                                self.oanda.modify_trade(self.oanda_account_id, trade_id3, trailingStop=1)
                                print 'short price ', short_price2
                                print 'buy back price ', buyBackprice
                                condition_met = True

                            if (short_price2 - buyBackprice) >= .0008 and trade_id3_status == False:
                                # close_order
                                print 'trade_id3 ', trade_id3
                                self.oanda.close_trade(6980117, trade_id3)
                                trade_id3_status = True
                                print 'short price ', short_price2
                                print 'buy back price ', buyBackprice
                                condition_met = True
                                break

                if condition_met:
                    break

                time.sleep(300)
            condition = False
            a = []
            b = []
            time.sleep(300)

        return

    def reversal_min(self, support_line, crossover_price):

        scope = 1
        condition = False
        condition_met = False
        global close_ask_array
        global open_ask_array

        # Wait 5 min for next candle to close
        time.sleep(self.sleeptime)
        # Condition searching loop time
        t_end = time.time() + 5400

        while time.time() < t_end:

            a = close_ask_array[-scope:]
            b = open_ask_array[-scope:]
            print 'a = self.close_ask_array[-scope:] in reversal Min ', a
            print 'b = self.open_ask_array[-scope:] in reversal Min ', b
            scope += 1

            # Last close price for candlestick in array
            latest_close_price = a[-1]
            # Last open price for candlestick in array
            latest_open_price = b[-1]

            if latest_close_price <= support_line - .0001:
                print 'got out of loop because close_price is ', latest_close_price
                print ' '
                break

            pass_up = max(a)
            print 'pass_up is ', pass_up

            if (latest_close_price <= (support_line + .0001)) & (latest_close_price >= (support_line - .0003)) and \
                    (latest_open_price > latest_close_price) and ((pass_up - support_line) >= .0004):

                time.sleep(self.sleeptime)

                # Don't grab whole array just grab most recent candlestick of info

                next_close = close_ask_array[-1]
                next_open = open_ask_array[-1]
                print 'next_close = self.close_ask_array[-1] in reversal Min ', next_close
                print 'next_open = self.open_ask_array[-1] in reversal Min ', next_open

                response = self.oanda.get_prices(instruments=self.currency_pair)
                prices = response.get("prices")
                ask = prices[0].get("ask")
                bid = prices[0].get("bid")
                spread = ask - bid

                print 'spread ', spread
                if spread > .0003:
                    break

                if (next_close > next_open) and (next_open > support_line) and (next_close - next_open <= .0004):

                    fiveMin_streaming_time = 0

                    long_price1 = self.oanda.create_order(6980117, instrument=self.currency_pair, units=13000,
                                                          side='buy',
                                                          type='market')
                    long_price2 = self.oanda.create_order(6980117, instrument=self.currency_pair, units=13000,
                                                          side='buy',
                                                          type='market')
                    long_price3 = self.oanda.create_order(6980117, instrument=self.currency_pair, units=13000,
                                                          side='buy',
                                                          type='market')

                    conn = httplib.HTTPSConnection("api-fxpractice.oanda.com")
                    params = urllib.urlencode({"instrument": self.currency_pair, })
                    headers = {"Content-Type": "application/x-www-form-urlencoded",
                               "Authorization": "Bearer 74b91ee3fda0251126b3d4a319067b88-7a70489e0dd38f5e6994ddda09b0e1ca"}
                    url = "/v1/accounts/6980117/trades?instrument=" + self.currency_pair + "&count=3"
                    conn.request("GET", url, params, headers)
                    price_action = conn.getresponse().read()
                    data = json.loads(price_action)
                    data_frame = json_normalize(data)
                    a = np.array(data_frame['trades'][0:len(data_frame)])
                    trade_id1 = a[0][2][u'id']
                    trade_id2 = a[0][1][u'id']
                    trade_id3 = a[0][0][u'id']

                    pickleDirRoot = '/Users/michaelstarin/Desktop/FOREX1/trading_graphs'
                    pickleDirDate = str(self.now)
                    pickleFileRoot = pickleDirRoot + '/' + pickleDirDate + '/' + self.currency_pair

                    try:
                        os.makedirs(pickleFileRoot)
                    except OSError:
                        pass

                    plt.axhline(y=support_line, color='red')
                    plt.xlim([0, 400])

                    plt.plot(close_ask_array[-400:], color='green')

                    plt.savefig(pickleFileRoot)
                    print 'BUY'

                    now = datetime.utcnow()
                    print ' The time is now rounded ', now
                    # Trade status: If True = position is closed, if False = position is open
                    trade_id1_status = False
                    trade_id2_status = False
                    trade_id3_status = False

                    while True:

                        streaming_time = 1
                        fiveMin_streaming_time += streaming_time
                        time.sleep(.05)

                        if fiveMin_streaming_time % 1200 == 0:
                            now = datetime.utcnow()
                            print ' The time is now rounded ', now
                            response = self.oanda.get_prices(instruments=self.currency_pair)
                            prices = response.get("prices")
                            long_price2 = long_price1[u'price']
                            buyBackprice = prices[0].get("bid")  # If buyback price is undesirable than cut losses
                            # Cut losses

                            if (long_price2 - buyBackprice) >= .0005 and trade_id1_status == False:
                                # close_order
                                print 'trade_id1 ', trade_id1
                                self.oanda.close_trade(6980117, trade_id1)
                                trade_id1_status = True
                                print 'short price ', long_price2
                                print 'buy back price ', buyBackprice
                                condition_met = True

                            if (
                                        long_price2 - buyBackprice) >= .0005 and trade_id2_status == False and trade_id3_status == False:
                                # close_order
                                print 'trade_id2 ', trade_id2
                                print 'trade_id3 ', trade_id3
                                self.oanda.close_trade(6980117, trade_id2)
                                self.oanda.close_trade(6980117, trade_id3)
                                trade_id2_status = True
                                trade_id3_status = True

                                print 'short price ', long_price2
                                print 'buy back price ', buyBackprice
                                condition_met = True
                                break

                        if fiveMin_streaming_time % 1200 == 0 or fiveMin_streaming_time % 1 == 0:
                            response = self.oanda.get_prices(instruments=self.currency_pair)
                            prices = response.get("prices")

                            long_price2 = long_price1[u'price']
                            buyBackprice = prices[0].get("bid")
                            # Take the profit
                            if (
                                buyBackprice - long_price2) >= .0008 and trade_id1_status == False and trade_id2_status == False:
                                # close_order
                                self.oanda.close_trade(6980117, trade_id1)
                                self.oanda.close_trade(6980117, trade_id2)
                                trade_id1_status = True
                                trade_id2_status = True

                                # Trade_id3 has a stop-loss of 5 pips
                                self.oanda.modify_trade(self.oanda_account_id, trade_id3, trailingStop=1)
                                print 'short price ', long_price2
                                print 'buy back price ', buyBackprice
                                condition_met = True

                            if (buyBackprice - long_price2) >= .0008 and trade_id3_status == False:
                                # close_order
                                print 'trade_id3 ', trade_id3
                                self.oanda.close_trade(6980117, trade_id3)
                                trade_id3_status = True
                                print 'short price ', long_price2
                                print 'buy back price ', buyBackprice
                                condition_met = True
                                break

                if condition_met:
                    break
                time.sleep(300)
            condition = False
            a = []
            b = []
            time.sleep(300)
        return
