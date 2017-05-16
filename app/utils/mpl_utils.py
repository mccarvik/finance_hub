import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

COLORS = ["b", "c", "m", "g", "k", "r", "y", "w"]
MARKERS = ['-', '--', '-.', ':', '.', ',', 'o', 'v', '^', '<', '>', '1', '2',
            '3', '4', '5', 's', 'p', '*', 'h', 'H', 'D', 'd', '|', 'x', '+']

def autolabel(rects, ax, decs=2):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                round(height,decs),
                ha='center', va='bottom')