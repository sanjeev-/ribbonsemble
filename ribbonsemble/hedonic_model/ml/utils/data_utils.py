import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
import ast
from collections import OrderedDict
from dateutil import parser
import mplleaflet

def history_to_sold_date(json_string):
	"""Takes sales history and returns most recent sale date

	Keyword arguments:
		json_string [string] the string representation of a json object

	Returns:
		solddate_dt [datetime object] the most recent date sold of the property
		if there's an error (e.g., missing json string) returns None

	"""
	if json_string == 'null':
		return None
	try:
	    d = ast.literal_eval(json_string)
	    od = OrderedDict(sorted(d.items(),key=lambda t: t[0]))
	    solddate = next(reversed(od))
	    solddate_dt = parser.parse(solddate)
	    return solddate_dt
	except Exception as e:
		print(e)
		return None

def facet_scatter(x, y, c, **kwargs):
    kwargs.pop("color")
    plt.scatter(x, y, c=c, **kwargs)

def mapHomes(df):
    g = sns.FacetGrid(df, palette = 'seismic')
    vmin, vmax = 15000, 500000
    cmap = plt.cm.winter
    norm=plt.Normalize(vmin=vmin, vmax=vmax)
    g = g.map(facet_scatter, 'longitude', 'latitude', "sold_price",
              s=50, alpha=0.8, norm=norm, cmap=cmap)
    # Make space for the colorbar
    g.fig.subplots_adjust(right=.92)
    # Define a new Axes where the colorbar will go
    cax = g.fig.add_axes([.94, .25, .02, .6])
    # Get a mappable object with the same colormap as the data
    points = plt.scatter([], [], c=[], vmin=vmin, vmax=vmax, cmap=cmap)
    # Draw the colorbar
    g.fig.colorbar(points, cax=cax)
    mplleaflet.show()