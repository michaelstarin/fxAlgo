__author__ = 'michaelstarin'

import oandapy
import threading
from LiveTrade import RSS1

oanda_account_id = "ACCOUNT_ID"
oanda_access_token = "ACCOUNT_ACCESS-TOKEN"

currency_pair = 'AUD_USD'

oanda = oandapy.API(environment="practice", access_token=oanda_access_token)
close_ask_array = None
open_ask_array = None
sensitivity_range = .00065
srzone_range = .0002

sec_sleep = 6
granularity = 'M5'
count = 1152
sleep_time = 303
domain = "practice"


def call_method(granularity, count, sleeptime, currency_pair, oanda_account_id, oanda_access_token, domain, oanda,
                sensitivity_range, srzone_range):
    instance1 = RSS1(granularity, count, sleeptime, currency_pair, oanda_account_id, oanda_access_token, domain, oanda,
                     sensitivity_range, srzone_range)
    instance1.main_fx()


rss = threading.Thread(target=call_method, args=(
    granularity, count, sleep_time, currency_pair, oanda_account_id, oanda_access_token, domain, oanda,
    sensitivity_range, srzone_range))
rss.start()
