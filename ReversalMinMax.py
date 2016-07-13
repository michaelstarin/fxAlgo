__author__ = 'michaelstarin'

import numpy as np


class Reversal:
    def __init__(self, array, sensitivity_range):
        self.array = array
        self.sensitivity_range = sensitivity_range

    def reversal_m_m(self):
        gradients = np.diff(self.array)
        locations = []
        locations_revision = []
        count = 0

        for i in gradients[:-1]:
            count += 1

            if ((cmp(i, 0) > 0) & (cmp(gradients[count], 0) < 0) & (i != gradients[count]) or (
                            (cmp(i, 0) < 0) & (cmp(gradients[count], 0) > 0) & (i != gradients[count]))):
                locations_revision.append(self.array[count])

        # locations_revision contains every local min and max
        # i starts at 1 because location_revision looks back, calculation does not consider first local min/max
        for i in range(1, len(locations_revision) - 1):
            if abs(locations_revision[i] - locations_revision[i + 1]) > self.sensitivity_range and abs(
                            locations_revision[i - 1] - locations_revision[i]) > self.sensitivity_range:
                locations.append(np.round(locations_revision[i], 6))

        return locations
