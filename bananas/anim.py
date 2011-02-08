from matplotlib import pyplot
import pylab
import numpy as np
import time


pyplot.ion()
def animate(x_list, y_list, title_list=None, interval=.2):
    """
    Flip through a series of slides.
    """
    # Init.  Have to draw the first frame to initialize, then animate.
    ax = pyplot.subplot(111)
    line, = pyplot.plot(x_list[0], y_list[0], "bo")

    # Show nothing if no titles are supplied
    if title_list is None:
        title_list = ["" for i in x_list]

    # Animate this guy.
    for x, y, title in zip(x_list, y_list, title_list):
        # reset data
        ax.set_title(title)
        line.set_xdata(x)
        line.set_ydata(y)

        # reset axis
        xlim = [np.min(x), np.max(x)]
        ylim = [np.min(y), np.max(y)]
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        # draw the new frame
        pyplot.draw()
        time.sleep(interval)


if __name__ == "__main__":

    x_list = np.array([np.arange(10) for i in range(100)])
    y_list = np.random.randn(100, 10)
    animate(x_list, y_list)
