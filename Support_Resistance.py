__author__ = 'michaelstarin'

import numpy as np


class SRZones:
    def __init__(self, locations, currency_pair, srzone_range):
        self.locations = locations
        self.currency_pair = currency_pair
        self.srzone_range = srzone_range

    def sup_rest(self):
        sr1_line_avg = 0
        rounding_num = 5
        bounces = 4
        ticker = 0
        index = 0
        sr1_ar = []
        used_t = []
        used_i = []

        for i in range(0, len(self.locations)):
            for t in range(1, len(self.locations)):

                if i != t and used_t.count(t) == 0 and used_i.count(i) == 0:

                    if (self.locations[i] == self.locations[t]) or (
                                self.locations[i] + self.srzone_range > self.locations[t] and self.locations[i] <
                        self.locations[t]) or (
                                self.locations[i] - self.srzone_range < self.locations[t] and self.locations[i] >
                        self.locations[t]):

                        ticker += 1.0

                        if ticker == 1.0:
                            sr1_line_avg = round((sr1_line_avg + self.locations[t]), rounding_num)

                        if ticker > 1.0:
                            sr1_line_avg = round((sr1_line_avg + self.locations[t]) / 2.0, rounding_num)

                        used_t.append(t)
                        index += 1

                    else:
                        pass
                else:
                    pass

            if ticker > 0:
                used_t.append(i)

            if ticker >= bounces:
                sr1_ar.append(sr1_line_avg)
                np.round(sr1_ar, rounding_num)
                print ' '

                ticker = 0
                sr1_line_avg = 0

        return sr1_ar
