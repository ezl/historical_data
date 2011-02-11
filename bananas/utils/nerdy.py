import scipy
from scipy.interpolate import UnivariateSpline
import pylab
import numpy as np
from ipshell import ipshell

def moneyness(strike, forward, sigma, t):
    return (np.log(strike) - np.log(forward)) / (sigma * np.sqrt(t))

def forward_price(spot, r, t):
    return spot * np.exp(r * t)

def find_implied_forward(synthetic_bids, synthetic_offers):
    best_bid = max(synthetic_bids)
    best_offer = min(synthetic_offers)
    IF = (best_bid + best_offer) / 2
    warning = None
    if max(synthetic_bids) > min(synthetic_offers):
        avg_mid =  np.average((synthetic_bids + synthetic_offers) / 2)
        warning = """\n
                 WARNING: Crossed synthetic market
                 nbbo is %s @ %s
                 bid:   %s, %s
                 offer: %s, %s
                 average: %s
              """ % (best_bid, best_offer,
                    np.average(synthetic_bids), np.std(synthetic_bids),
                    np.average(synthetic_offers), np.std(synthetic_offers),
                    avg_mid)
        print warning
    if warning is not None:
        return avg_mid
    else:
        return IF

from functools import partial
from openopt import NLP
import pyipopt
def wls_fit(function, initial_guess, X, Y, weights=None, lb=None, ub=None):
    """[Inputs]
        function is of form:
            def function(coeffs, xdata)
    """

    if weights is None:
        weights = [1] * len(X)

    def penalty(c):
        fit = function(c, X)
        error = (weights * (Y - fit) ** 2).sum()
        return error

    problem = NLP(penalty, initial_guess)

    if lb is not None:
        problem.lb = lb
    if ub is not None:
        problem.ub = ub

    solver = 'ipopt'
    result = problem.solve(solver)

    coeffs = result.xf
    return coeffs

def spline_fit(strikes, implied_vols, degree=4):
    '''
    No idea what spline.get_coeffs() is giving me... scrapping this

    Unused for now. Keeping for reference.
    '''
    spline = UnivariateSpline(strikes, implied_vols, w=None, k=degree)
    return spline

def nth_degree_poly(n):
    def f(x, *p):
        return sum([p[i]*x**i for i in range(n)])
    return f

def line(x, p1, p0):
    return (p1*x) + p0

def quadratic(x, p2, p1, p0):
    return (p2*x**2) + (p1*x) + p0

def cubic(x, p3, p2, p1, p0):
    return (p3*x**3) + (p2*x**2) + (p1*x) + p0

def quartic(x, p4, p3, p2, p1, p0):
    return (p4*x**4) + (p3*x**3) + (p2*x**2) + (p1*x) + p0

# TODO: i hate this how can i generate the necessary function?

def polyfit_unweighted(strikes, implied_vols, degree=4):
    '''Fit a vol smile'''
    poly_coeffs = scipy.polyfit(strikes, implied_vols, degree)
    return poly_coeffs

def fit_smile(strikes, implied_vols, degree=4, w=None):
    return polyfit_unweighted(strikes, implied_vols, degree=degree)
    # return polyfit_weighted(strikes, implied_vols, degree=4, w=w)

def clip_repeated_wings(*data):
    '''Clips numpy vectors on both ends if any vector repeats.

        Inputs: Any number of numpy arrays
        Process: If any array has repeated elements on either end, repeated values
                 and corresponding indexed values of other arrays are popped.
        Returns: Clipped numpy arrays
    '''
    def clip_dupes(data):
        '''
        Sometimes call_iv == put_iv. Almost certainly shitty data. Clip.
        '''
        if len(data[0]) < 2:
            return [[] for d in data]
        top_row = [d[0] for d in data]
        dupe_found = any([top_row.count(item) > 1 for item in top_row])
        if dupe_found:
            [d.pop(0) for d in data]
            return clip_dupes(data)
        return data

    def clip_left(data):
        if len(data[0]) < 2:
            return [[] for d in data]
        repeat_found = any([d[0] == d[1] for d in data])
        if repeat_found:
            [d.pop(0) for d in data]
            return clip_left(data)
        else:
            clip_dupes(data)
            return data

    def clip_right(data):
        [d.reverse() for d in data]
        data = clip_left(data)
        [d.reverse() for d in data]
        return data

    all_same_length = all([len(d) == len(data[0]) for d in data])
    if not all_same_length:
        msg = "Inputs not all same length"
        raise Exception, msg
    list_data = [list(d) for d in data]
    list_data = clip_left(list_data)
    list_data = clip_right(list_data)
    data = [np.array(d) for d in list_data]
    if len(data) == 1:
    # don't return a list of one nparrays
        data = data[0]
    return data
