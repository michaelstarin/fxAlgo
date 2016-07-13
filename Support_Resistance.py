__author__ = 'michaelstarin'

import numpy as np



class SRZones:
    def __init__(self,locations,currency_pair,srzone_range):
        self.locations = locations
        self.currency_pair = currency_pair
        self.srzone_range = srzone_range

    def S_R(self):
        SR1_lineAVG = 0
        SR1_AR = []
        ticker = 0
        used_t = []
        used_i = []
        index = 0



        # if self.currency_pair == 'GBP_USD' or self.currency_pair == 'GBP_AUD' or self.currency_pair == 'EUR_AUD':
        #     bounces = 3.0
        # elif self.currency_pair == 'AUD_USD' or self.currency_pair == 'EUR_USD':
        #     bounces = 1.0
        # else:
        #     bounces = 100.0

        # if self.currency_pair == 'GBP_USD' or self.currency_pair == 'GBP_AUD' or self.currency_pair == 'EUR_AUD':
        #     bounces = 1.0
        # elif self.currency_pair == 'AUD_USD' or self.currency_pair == 'EUR_USD':
        #     bounces = 1.0
        # else:
        #     bounces = 1.0

        if self.currency_pair == 'GBP_USD' or self.currency_pair == 'GBP_AUD' or self.currency_pair == 'EUR_AUD':
            bounces = 9.0
        else:
            bounces = 4.0



        for i in range(0, len(self.locations)):
            for t in range(1, len(self.locations)):

                if i != t and used_t.count(t) == 0 and used_i.count(i) == 0:

                    if (self.locations[i] == self.locations[t]) or (
                                self.locations[i] + self.srzone_range > self.locations[t] and self.locations[i] < self.locations[t]) or (
                                self.locations[i] - self.srzone_range < self.locations[t] and self.locations[i] > self.locations[t]):
                        ticker += 1.0

                        if ticker == 1.0:
                            SR1_lineAVG = round((SR1_lineAVG + self.locations[t]), 5)

                        if ticker > 1.0:
                            SR1_lineAVG = round((SR1_lineAVG + self.locations[t]) / 2.0, 5)

                        used_t.append(t)
                        index += 1

                    else:
                        pass
                else:
                    pass

            if ticker > 0:
                used_t.append(i)

            if ticker >= bounces:
                SR1_AR.append(SR1_lineAVG)
                np.round(SR1_AR, 5)
                print ' '

                ticker = 0
                SR1_lineAVG = 0

        return SR1_AR
    ###################################################################################################################






