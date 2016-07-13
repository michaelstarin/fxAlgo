__author__ = 'michaelstarin'

import httplib
import urllib
from datetime import timedelta
from pandas.io.json import json_normalize
import json


class RestfulAPI:
    def __init__(self,granularity,count,currency_pair,
                oanda_account_id,oanda_access_token,domain,now):
        self.granularity = granularity
        self.now = now
        self.domain = domain
        self.oanda_access_token = oanda_access_token
        self.oanda_account_id = oanda_account_id
        self.currency_pair = currency_pair
        self.count = count
        self.stop = None

    def get_restful_price_1hr(self):

        self.stop = self.now - timedelta(hours = self.now.hour % 1, minutes=self.now.minute % 60, seconds=self.now.second % 60, microseconds=self.now.microsecond)
        current_time = self.stop.strftime('%Y-%m-%dT%H' + '%%3A' + '%M' + '%%3A' + '%S') + 'Z'

        conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
        params = urllib.urlencode({"instrument": "AUD_JPY","granularity": "M1","candleFormat" : "bidask"})
        headers = {"Content-Type" : "application/x-www-form-urlencoded","Authorization": "Bearer 5108711d40780491345a5685ceeaea34-8e2e72d27392bc7d65afa73bbf8f887d"}
        url = "/v1/candles?instrument=" + self.currency_pair + "&granularity=M30" + "&end=" + current_time + "&candleFormat=bidask" + "&count=" + str(self.count)
        conn.request("GET", url, params, headers)

        try:

            price_action = conn.getresponse().read()
            data = json.loads(price_action)
            data_frame = json_normalize(data['candles'])
            return data_frame
        except:
            price_action = conn.getresponse().read()
            data = json.loads(price_action)
            print 'error, data is ', data

            return exit()



    def get_restful_price_5min(self):

        self.stop = self.now - timedelta(minutes=self.now.minute % 5, seconds=self.now.second % 60, microseconds=self.now.microsecond)
        current_time = self.stop.strftime('%Y-%m-%dT%H' + '%%3A' + '%M' + '%%3A' + '%S') + 'Z'

        conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
        params = urllib.urlencode({"instrument": "AUD_JPY","granularity": "M1","candleFormat" : "bidask"})
        headers = {"Content-Type" : "application/x-www-form-urlencoded","Authorization": "Bearer 5108711d40780491345a5685ceeaea34-8e2e72d27392bc7d65afa73bbf8f887d"}
        url = "/v1/candles?instrument=" + self.currency_pair + "&granularity=M5" + "&end=" + current_time + "&candleFormat=bidask" + "&count=" + str(self.count)
        conn.request("GET", url, params, headers)

        try:

            price_action = conn.getresponse().read()
            data = json.loads(price_action)
            data_frame = json_normalize(data['candles'])
            return data_frame
        except:
            price_action = conn.getresponse().read()
            data = json.loads(price_action)
            print 'error, data is ', data

            return exit()