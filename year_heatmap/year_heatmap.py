"""
Calendar heatmaps from Pandas time series data.
Plot Pandas time series data sampled by day in a heatmap per calendar year,
similar to GitHub's contributions calendar.

Based on Martijn Vermaat's calmap:  https://github.com/martijnvermaat/calmap
"""

import calendar
import datetime

from matplotlib.colors import ColorConverter, ListedColormap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def year_heatmap(df,value_cols=None, time_col=None, year=None, 
                   how='sum', vmin=None, vmax=None, colour_map=None,
                   fillcolor='whitesmoke', linewidth=1, linecolor=None,
                   daylabels=calendar.day_abbr[:], dayticks=True,
                   monthlabels=calendar.month_abbr[1:], 
                   monthticks=True, base_figsize=(15,5),
                   fsize=None,vgap=None, **kwargs):
    """
    Plot multiple values and years from a timeseries as a calendar heatmap. 
    
    Parameters
    ----------
    df : DataFrame
        Data for the plot. Must be indexed by a DatetimeIndex.
    value_cols: list or str
        Single colum name or list of column names containing the values
        to be heatmapped. Default is all Columns.
    time_col: str
        Name of column where time series data is.  Default is the index
    year : integer
        Only data indexed by this year will be plotted. If `None`, the first
        year for which there is data will be plotted.
    how : string
        Method for resampling data by day. If `None`, assume data is already
        sampled by day and don't resample. Otherwise, this is passed to Pandas
        `Series.resample`.
    vmin, vmax : floats
        Values to anchor the colormap. If `None`, min and max are used after
        resampling data by day.
    colour_map : List of matplotlib colormap name or object
        The mapping from data values to color space for each column in value_cols
    fillcolor : matplotlib color
        Color to use for days without data.
    linewidth : float
        Width of the lines that will divide each day.
    linecolor : color
        Color of the lines that will divide each day. If `None`, the axes
        background color is used, or 'white' if it is transparent.
    daylabels : list
        Strings to use as labels for days, must be of length 7.
    dayticks : list or int or bool
        If `True`, label all days. If `False`, don't label days. If a list,
        only label days with these indices. If an integer, label every n day.
    monthlabels : list
        Strings to use as labels for months, must be of length 12.
    monthticks : list or int or bool
        If `True`, label all months. If `False`, don't label months. If a
        list, only label months with these indices. If an integer, label every
        n month.
    base_figsize : tuple (x,y)
        The base proportions used to build up the final plot size which depends
        on the number of years and the number of rows displayed.
    fsize : float
        fontsize (if None, then appropriate sizes are estimated based on
        the data)
    vgap: float
        adjustment to the gap between year plots (this value usually ranges
        from 0.5 to 5).  If None, then appropriate value is estimated.
        
        To adjust plot spacing by hand, values of fsize, vgap and base_figsize
        must be tweaked together.
    kwargs : other keyword arguments
        All other keyword arguments are passed to matplotlib `ax.pcolormesh`.
    Returns
    -------
    fig, ax : matplotlib Figure and Axes
        Fig and Axes objects with the calendar heatmap.
    
    """    
    if value_cols == None:
        value_cols = df.columns.tolist()
    elif type(value_cols) == str:
        value_cols = [value_cols]
    
    if time_col==None:
        row_data = df[value_cols]
    else:
        row_data = df[value_cols+[time_col]]
        row_data = row_data.set_index(time_col)
    
    if colour_map is None:
        colour_map = ['Purples', 'Reds', 'Blues', 'Greys']

    if how is None:
        # Assume already sampled by day.
        row_data = data
    else:
        # Sample by day.
        row_data = row_data.resample('D').agg(how)
    
    # Number of rows of plot to print for each year
    nrows = len(value_cols)
    colour_map = [colour_map[i % len(colour_map)] for i in range(0,nrows)]
    
    # Number of years
    years = list(set([r.year for r in row_data.index.tolist()]))
    years.sort()
    if year is not None:
        years = [y for y in years if y==year]
    num_years = len(years)
    
    # Calculate appropriate sizes for fonts and gaps
    if num_years == 1 or nrows>=3:
        fontsize=15
        v_gap=5
    elif num_years == 2:
        fontsize=30
        v_gap=0.5 if nrows==1 else 5
    elif nrows==1:
        fontsize=50
        v_gap=3
    elif nrows==2:
        fontsize=20
        v_gap=4
    else:
        fontsize=15
        v_gap=5
        
    if fsize is not None:
        fontsize=fsize
    if vgap is not None:
        v_gap=vgap
    
    
    figsize = (base_figsize[0]*len(years), 
               base_figsize[1]*len(years)+v_gap*(len(years)-1))
    
    fig, axes = plt.subplots(figsize=figsize, nrows=nrows*len(years), ncols=1, squeeze=False)
    
    for yr_idx, year in enumerate(years):
        axes_y = axes[yr_idx*nrows:(yr_idx*nrows+(nrows))]
        for idx, ax_lst in enumerate(axes_y):
            
            data = row_data[value_cols[idx]]
            ax = ax_lst[0]
            cmap = colour_map[idx]
            
            by_day = data
            # Min and max per day.
            if vmin is None:
                vmin = by_day.min()
            if vmax is None:
                vmax = by_day.max()

            if linecolor is None:
                # Unfortunately, linecolor cannot be transparent, as it is drawn on
                # top of the heatmap cells. Therefore it is only possible to mimic
                # transparent lines by setting them to the axes background color. This
                # of course won't work when the axes itself has a transparent
                # background so in that case we default to white which will usually be
                # the figure or canvas background color.
                linecolor = ax.get_fc()
                if ColorConverter().to_rgba(linecolor)[-1] == 0:
                    linecolor = 'white'

            # Filter on year.
            by_day = by_day[str(year)]

            # Add missing days.
            by_day = by_day.reindex(
                pd.date_range(start=str(year), end=str(year + 1), freq='D')[:-1])

            # Create data frame we can pivot later.
            by_day = pd.DataFrame({'data': by_day,
                                   'fill': 1,
                                   'day': by_day.index.dayofweek,
                                   'week': by_day.index.week})

            # There may be some days assigned to previous year's last week or
            # next year's first week. We create new week numbers for them so
            # the ordering stays intact and week/day pairs unique.
            by_day.loc[(by_day.index.month == 1) & (by_day.week > 50), 'week'] = 0
            by_day.loc[(by_day.index.month == 12) & (by_day.week < 10), 'week'] \
                = by_day.week.max() + 1

            # Pivot data on day and week and mask NaN days.
            plot_data = by_day.pivot('day', 'week', 'data').values[::-1]
            plot_data = np.ma.masked_where(np.isnan(plot_data), plot_data)

            # Do the same for all days of the year, not just those we have data for.
            fill_data = by_day.pivot('day', 'week', 'fill').values[::-1]
            fill_data = np.ma.masked_where(np.isnan(fill_data), fill_data)

            # Draw heatmap for all days of the year with fill color.
            ax.pcolormesh(fill_data, vmin=0, vmax=1, cmap=ListedColormap([fillcolor]))

            # Draw heatmap.
            kwargs['linewidth'] = linewidth
            kwargs['edgecolors'] = linecolor
            ax.pcolormesh(plot_data, vmin=vmin, vmax=vmax, cmap=cmap, **kwargs)

            # Limit heatmap to our data.
            ax.set(xlim=(0, plot_data.shape[1]), ylim=(0, plot_data.shape[0]))

            # Square cells.
            ax.set_aspect('equal')

            # Remove spines and ticks.
            for side in ('top', 'right', 'left', 'bottom'):
                ax.spines[side].set_visible(False)
            ax.xaxis.set_tick_params(which='both', length=0)
            ax.yaxis.set_tick_params(which='both', length=0)

            # Get indices for daylabels.
            if dayticks is True:
                dayticks = range(len(daylabels))
            elif dayticks is False:
                dayticks = []
            elif isinstance(dayticks, int):
                dayticks = range(len(daylabels))[dayticks // 2::dayticks]

            ax.set_xlabel('',fontsize=2)
            ax.set_xticklabels(['']*len(monthlabels), ha='center', fontsize=2)

            ax.set_ylabel('')
            ax.yaxis.set_ticks_position('right')
            ax.set_yticks([6 - i + 0.5 for i in dayticks])
            ax.set_yticklabels([daylabels[i] for i in dayticks], rotation='horizontal',
                               va='center', fontsize=fontsize)

            ax.set_title(value_cols[idx], loc='left', fontsize=fontsize)

        # Get indices for monthlabels.
        if monthticks is True:
            monthticks = range(len(monthlabels))
        elif monthticks is False:
            monthticks = []
        elif isinstance(monthticks, int):
            monthticks = range(len(monthlabels))[monthticks // 2::monthticks]

        ax.set_xticks([by_day.loc[datetime.date(year, i + 1, 15)].week
                           for i in monthticks])

        ax.set_xticklabels([monthlabels[i] for i in monthticks], 
                            ha='center', fontsize=fontsize)
        ax.set_xlabel(str(year), ha='center', fontsize=fontsize)

    # tidy up
    fig.tight_layout()
    return fig, axes