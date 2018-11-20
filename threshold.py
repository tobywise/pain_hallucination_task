from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class MultiStairCase:

    def __init__(self, n_trials, start_value, min=0, max=40, step=10, n_estimators=2):

        self.n_estimators = n_estimators
        self.estimators = []
        for i in range(n_estimators):
            self.estimators.append(CrappyThresholdEstimator(n_trials, start_value, min, max, step))

        self.trial = 0
        self.fit_success = False

    @staticmethod
    def func(x, b, c):  # logistic function
        return 1 / (1 + b * np.power(c, -x))

    @staticmethod
    def inv_func(y, b, c):  # inverse of the logistic function

        return -(np.log(1 / (b * ((y) / (1 - y)))) / np.log(c))

    def next(self):

        return self.estimators[self.trial % self.n_estimators].next()

    def add_response(self, response):

        success = self.estimators[self.trial % self.n_estimators].add_response(response)

        if success:
            self.trial += 1

    def fit(self):

        self.x = []
        self.y = []

        for i in self.estimators:
            self.x += i.intensities
            self.y += i.responses

        self.popt, self.pcov = curve_fit(self.func, self.x, self.y, method='trf')  # fit a curve

        self.fit_success = True

    def invert(self, level):

        if not self.fit_success:
            raise AttributeError("Curve has not been fit")

        return self.inv_func(level, *self.popt)

    def plot(self, levels=()):

        if not self.fit_success:
            raise AttributeError("Curve has not been fit")

        plt.scatter(self.x, self.y, facecolors='none', edgecolors='black', label='Responses')  # plot the data points
        plt.plot(np.arange(np.min(self.x), np.max(self.x), 0.05),
                 self.func(np.arange(np.min(self.x), np.max(self.x), 0.05), *self.popt),
                 label='Fit')
        for l in levels:
            plt.axvline(self.invert(l), color='gray', linestyle=':')
        plt.xlabel("Intensity")
        plt.ylabel("P(response)")
        plt.legend()
        plt.tight_layout()

    def __iter__(self):
        return self


class CrappyThresholdEstimator:

    def __init__(self, n_trials, start_value, min=0, max=40, step=10):

        self.responses = []
        self.intensities = []
        self.step = step
        self.start = start_value
        self.max = max
        self.min = min
        self.n_trials = n_trials

    def next(self):

        if len(self.intensities) == self.n_trials:
            raise StopIteration

        if len(self.responses) == 0:
            intensity = self.start

        else:
            if np.mean(self.responses) < 0.5:
                intensity = self.intensities[-1] + self.step * (0.5 - np.mean(self.responses))

            else:
                intensity = self.intensities[-1] - self.step * (np.mean(self.responses) - 0.5)

        if intensity > self.max:
            intensity = self.max

        if intensity < self.min:
            intensity = self.min

        self.intensities.append(intensity)

        return intensity

    def add_response(self, response):

        if response == [] or response == None or response == '':
            print "No response"
            self.intensities = self.intensities[:-1]
            return False

        elif response != 0 and response != 1:
            raise ValueError("Response should be 0 or 1")

        else:
            self.responses.append(int(response))
            return True

    def __iter__(self):
        return self