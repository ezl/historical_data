

def garmanklass(o, h, l, c, c_previous=None):
    if c_previous == None:
        gk = 0.5 * (np.log(h / l) ** 2) - .39 * (np.log(c / o) ** 2)
    else:
        gk = (np.log(o / c_previous) ** 2) + 0.5 * (np.log(h / l) ** 2) - .39 * (np.log(c / o) ** 2)
    return gk

def closeclose(c1, c2, t, periods_per_year=270.08):
    cc = np.log(c2/c1) * np.sqrt(periods_per_year / t)
    return cc


