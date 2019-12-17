import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap


def heat_stripes(df, col, reference = None, clim = None, 
                     first=None, last=None,index=None, cmap = None):
    """
    Creates a stripped heatmap.
    Inspired by Maximilian Nöthe -- https://matplotlib.org/matplotblog/posts/warming-stripes/

    Input:
        col -- the name of the column to be heatstriped.  Must be
               numeric and missing values are dropped
        reference -- A string of the form 'A:B' that identifies the index
                     rows where the colour pallette should be centered.
                     If None, the row in the middle of col is used
        clim  -- a numeric value +/- the reference value that controls 
                 the colour limit of the stripes.  Default is 2 standard
                 deviations of the values in col
        first -- First index row to use in stripes.  If None, then first row
        last -- Last index row to use in stripes.  If None, then last row
        index -- the name of the reference column.  If None the existing
                 index to df is used.
        cmap -- a ListedColormap pallette for the striped output colour.
                Default is a red/blue scale  
    Output:
        fig -- a matplotlib plot of the heat_stripes

    """
    if index is None:
        data = df.loc[:, col].dropna()
    else:
        data = df[[index, col]].set_index(index)
        data = data.loc[:, col].dropna()

    # calculate mean value of the reference rows
    if reference is None:
        reference = data.reset_index().loc[len(data)//2][col].mean()
    else:
        first_ref, last_ref = [int(r) for r in reference.split(':')]
        reference = data.loc[first_ref:last_ref].mean()

    if clim is None:
        clim = 2 * data.std()

    if first is None:
        first = data.index[0]
    if last is None:
        last = data.index[-1]
    
    if cmap is None:
        # the colors in this colormap come from http://colorbrewer2.org
        # the 8 more saturated colors from the 9 blues / 9 reds
        cmap = ListedColormap([
            '#08306b', '#08519c', '#2171b5', '#4292c6',
            '#6baed6', '#9ecae1', '#c6dbef', '#deebf7',
            '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a',
            '#ef3b2c', '#cb181d', '#a50f15', '#67000d',
        ])

    fig = plt.figure(figsize=(10, 1))

    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()

    # create a collection with a rectangle for each row
    col = PatchCollection([
        Rectangle((y, 0), 1, 1)
        for y in range(first, last + 1)
    ])

    # set data, colormap and color limits
    col.set_array(data)
    col.set_cmap(cmap)
    col.set_clim(reference - clim, reference + clim)
    ax.add_collection(col)

    ax.set_ylim(0, 1)
    ax.set_xlim(first, last + 1)

    return fig
