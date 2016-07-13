__author__ = 'michaelstarin'


import threading
from LiveTrade import RSS1
import oandapy

oanda_account_id = 6980117
oanda_access_token = "74b91ee3fda0251126b3d4a319067b88-7a70489e0dd38f5e6994ddda09b0e1ca"
#currency_pair = ['EUR_USD','AUD_USD','USD_CAD','GBP_USD','GBP_AUD','EUR_AUD']
currency_pair = 'EUR_USD'
#currency_pair = 'USD_JPY'
#currency_pair = 'GBP_USD'
#currency_pair = 'USD_CHF'
#currency_pair = 'AUD_USD'
#currency_pair = 'USD_CAD'
#currency_pair = 'EUR_GBP'
#currency_pair = 'EUR_JPY'
#currency_pair = 'GBP_JPY'

oanda = oandapy.API(environment="practice",access_token=oanda_access_token)
close_ask_array = None
open_ask_array = None
sensitivity_range = .00065
srzone_range = .0002

sec_sleep = 60
granularity = 'M5'
count = 1152
sleeptime = 303
domain = "practice"


def call_method(granularity,count,sleeptime,currency_pair,oanda_account_id,oanda_access_token,domain,oanda,sensitivity_range,srzone_range):
    instance1 = RSS1(granularity,count,sleeptime,currency_pair,oanda_account_id,oanda_access_token,domain,oanda,sensitivity_range,srzone_range)
    instance1.main_FX()


rss = threading.Thread(target=call_method, args= (granularity,count,sleeptime,currency_pair,oanda_account_id,oanda_access_token,domain,oanda,sensitivity_range,srzone_range))
rss.start()

