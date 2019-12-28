import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
import numpy as np

from .wedge_plot_defaults import default_label_format, default_legend_tick, wedge_defaults

def wedge_plot(df, ring_values=None, slice_labels=None, colours=None,
        radius=None, wedge_width=None, wedge_labels=None,startangle=-30,  
        all_slices_percent=0.43, 
        
        hide_wedge_label= False, hide_slice_label= False, hide_legend=False,
        hide_centre_circle=False,hide_ring_label=True,
        
        legend_orientation= 'horizontal', legend_units=None,
        legend_fontweight= 'bold', legend_fontsize= 12, legend_fontstyle='normal',
        legend_boxheight= 0.05, legend_boxwidth= 0.25,
        legend_tickvalues= default_legend_tick,
        legend_x_start = 0.1, legend_y_start = -0.6,
        legend_gap=-0.1, legend_label_round_to=1,

        wedge_label_format= default_label_format, wedge_label_rotate=True,
        slice_label_nudge=0.02, slice_label_rotate=True, explode=0,

        circle_label='', circle_fontsize= 30,
        circle_ha='center', circle_va='center',
        title=None, title_x=0, title_y=.98, title_fontsize='xx-large',
        title_fontweight='bold',
        
        figsize=(10,10), edgecolour='k',
        linewidth=1.4, label_fontsize='large', label_fontweight='semibold',
        blankcolour='w', ls='-',alpha=1):
    """
    Produce a wedge plot figure from columns in the dataframe

    Input:
        There are no mandatory parameters if the number of wedges in
        each slice is 5 or less.  If there are more than five, then the
        colours, radius and wedge_width parameters must be specified.

        There are a large number of parameters that can be tweaked, but a
        sensible set of defaults is provided to generate most types
        of wedge plots.  The parameters are grouped below into the
        different aspects of the plot.

        Data parameters:
            ring_values -- list of column values to use for each ring
                           of data.  All columns used if none provided.
            slice_labels -- string of the column name which is to be used
                            for each wedge slice - one per row of data.
                            The index is used if none provided.
            colours -- A list of string names to use for each wedge colour
                       palette.  Same length as ring_values
            radius -- A list of radius widths for the outer radius of 
                      each wedge. Same length as ring_values
            wedge_width -- A list of widths for the each wedge. 
                           Same length as ring_values
            wedge_labels -- A list a labels for each wedge.  The column names
                            of ring_values is used if not provided.
            startangle -- the starting angle for drawing the wedge plot.
                          Should be between -90 and 270
            all_slices_percent -- the total percentage of a circle that should
                                  be taken up by all the wedges 
        
        Display parameters:
            All are True or False

            hide_wedge_label -- whether values are shown in each wedge
            hide_slice_label -- whether each slice is labelled
            hide_legend -- whether a legend is shown
            hide_centre_circle -- whether a circle is shown in the centre
            hide_ring_label -- whether is ring is labelled
            
        Legend parameters:
            These all take appropriate matplotlib values
            legend_orientation -- orientation of legend labels
            legend_units -- If None, no units shown on the legend scale.
                            If a single string, that is added to every legend
                            If a list, then a different unit is displayed for
                            each item in the legend
            legend_fontweight -- weight of legend font
            legend_fontsize -- size of legend font
            legend_fontstyle -- style of legend font
            legend_boxheight -- height of legend colour map
            legend_boxwidth -- width of legend colour map
            legend_tickvalues -- function to generate tick values and labels
                                 three ticks are provided by default.  If a 
                                 custom one is provided, it needs accept
                                 a list of values for each wedge and return
                                 two lists of ticks, tick_labels (each of the
                                 same length)
            legend_x_start -- x coord of the legend
            legend_y_start -- y coord of the first item in the legend
            legend_gap -- offset to layer each item in the legend.  Negative
                          to order the legends outer to inner and positive
                          for the other way around
            legend_label_round_to -- precision to show in the label of each
                                     item in the legend
        Wedge and Slice Parameters:
            wedge_label_format -- function to turn a wedge value to a string
                                  label.  Default is just a string.  A custom
                                  function can be provided that accepts a value
                                  and returns a string
            wedge_label_rotate -- whether wedge labels are rotated
            slice_label_nudge -- distance from edge of last wedge and the slice
                                 label
            slice_label_rotate -- whether the slice labels should be rotated
            explode -- gap between all wedges in a slice (0 for no gap)
        Centre circle and plot title parameters:
            circle_label -- label to show in the centre circle
            circle_fontsize -- font size of circle label
            circle_ha -- horizontal aligment of circle label
            circle_va -- vertical aligment of circle label
            title -- plot title
            title_x -- x co ordinate of the title
            title_y -- y co ordinate of the title
            title_fontsize -- fontsize of the title
            title_fontweight -- fontweight of the title
        
        General plot parameters
            figsize -- size of the figure
            edgecolour -- edge colour of wedges and circle
            linewidth -- width of lines in wedge
            label_fontsize -- size of font on slice and wedge labels
            label_fontweight -- weight of font on slice and wedge labels
            blankcolour -- background colour of centre circle and slice labels
            ls -- line style of circle and wedges
            alpha -- alpha setting for all colours
    """
    # A slice is a row of data across all columns
    #     A single triangular pizza slice
    # A wedge is a single row and single column 
    #     A portion of a slice
    # A ring is a column of data
    #     Wedges from each slice in the same layer
    
    if ring_values is None:
        ring_values = df.columns.tolist()
    if slice_labels is None:
        slice_labels = df.index.tolist()
    else:
        slice_labels = df[slice_labels].tolist()
        
    num_slices = df.shape[0]
    num_wedges = len(ring_values)
    
    # Gather all wedges parameters together and update
    # the defaults
    wedge_params = {
    'colours': colours,
    'radius': radius,
    'wedge_width': wedge_width,
    'slice_labels': slice_labels,
    }
    wedge_params = {k:v for k,v in wedge_params.items() if v is not None}
    wedges = wedge_defaults(num_wedges)
    wedges.update(wedge_params)    
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Replace any None values with the column name of ring_values
    if wedge_labels is None:
        wedges['wedge_labels'] = ring_values.copy()
    else:
        wedges['wedge_labels'] = wedge_labels

    
    wedges['radius'] = [r+i*explode for i, r in enumerate(wedges['radius'])]
    circle_radius = wedges['radius'][0] - wedges['wedge_width'][0] - explode
    
    # centre circle first
    if not hide_centre_circle:
        centre_circle = plt.Circle((0, 0),
                                circle_radius, 
                                color=blankcolour, 
                                ls=ls, 
                                ec=edgecolour, 
                                lw=linewidth)
        centre_label = ax.annotate(circle_label, 
                                xy=(0, 0), 
                                fontsize=circle_fontsize, 
                                ha=circle_ha, 
                                va=circle_va)
        ax.add_artist(centre_circle)
    
    # Add each wedge from outer to inner for each slice of data
    slice_sizes = [all_slices_percent/num_slices]*num_slices
    
    # add the outer labels first
    if not hide_slice_label:
        labels = slice_labels
        outer_labels = ax.pie(slice_sizes, 
                    radius=wedges['radius'][num_wedges-1],
                    startangle=startangle, 
                    colors=[blankcolour]*num_slices, 
                    labels=labels,
                    labeldistance=1 + slice_label_nudge,
                    rotatelabels=slice_label_rotate,
                    textprops=dict(fontsize=label_fontsize, 
                                   weight=label_fontweight,
                                   va='center', 
                                   wrap=True))
                                   
        # Set correct label ha for all wedge angles
        slice_angle = 360*all_slices_percent/num_slices

        for i, s in enumerate(outer_labels[1]):
            angle = startangle + (i+0.5)*slice_angle
            if -90 <= angle <= 90:
                s.set_ha('left')
            else:
                s.set_ha('right')
    
    # build rings from ouside in
    ring_values.reverse()       
    for idx, ring in enumerate(ring_values):
        idx = num_wedges - idx - 1
        ring_values = df[ring].tolist()
        vmin=min(ring_values)
        vmax=max(ring_values)
        
        # run a custom function to format the labels
        labels = [wedge_label_format(c) for c in ring_values]
        if hide_wedge_label:
            labels = [''] * num_slices
        
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
        mapper = ScalarMappable(norm=norm, cmap=wedges['colours'][idx])
        
        radius = wedges['radius'][idx]
        width = min(wedges['wedge_width'][idx], radius)
        label_distance = (radius - width/2)/radius

        layer = ax.pie(slice_sizes, 
                            radius=radius,
                            startangle=startangle, 
                            colors=mapper.to_rgba(ring_values, alpha=alpha), 
                            labels=labels, 
                            rotatelabels=wedge_label_rotate,
                            labeldistance=label_distance,
                            wedgeprops=dict(width=width, 
                                            edgecolor=edgecolour,linewidth= linewidth),
                            textprops=dict(fontsize=label_fontsize,weight=label_fontweight,
                                           va='center', ha='center',wrap=True))
                            
        # Place the legend
        if not hide_legend:
            axcmap = plt.axes([1+legend_x_start, 1+legend_y_start-idx*legend_gap, 
                                 legend_boxwidth,legend_boxheight])
            
            ticks, tick_labels = default_legend_tick(ring_values, round_to=legend_label_round_to)
            
            if legend_units is not None:
                if type(legend_units)==str:
                    unit_label = legend_units
                else:
                    unit_label = legend_units[idx]
                tick_labels[-1] = '{} {}'.format(tick_labels[-1], unit_label)

            cbar = plt.colorbar(mapper,cax=axcmap, orientation="horizontal",ticks=ticks, alpha=alpha)
            cbar.ax.set_xticklabels(tick_labels) 

            cbar.set_label(wedges['wedge_labels'][idx],
                           weight=legend_fontweight, 
                           fontsize=legend_fontsize, fontstyle=legend_fontstyle)
        
        # Place the legend label on the ring
        if not hide_ring_label:
            ring_label_angle = startangle + 360*all_slices_percent
            if -180 <=ring_label_angle <= 0:
                ring_label_just = 'left'
            else:
                ring_label_just = 'right'
            ring_label = ax.pie([0.01], 
                    radius=radius,
                    startangle=ring_label_angle, 
                    colors='w', 
                    labels=[wedges['wedge_labels'][idx]], 
                    rotatelabels=False,
                    labeldistance=label_distance,
                    wedgeprops=dict(width=width),
                    textprops=dict(fontsize=legend_fontsize,weight=legend_fontweight,
                                   fontstyle=legend_fontstyle,
                                   va='center', ha=ring_label_just,wrap=True))

                            
                
    ax.set(aspect="equal")
    if title is not None:
        fig.suptitle(title, x=title_x, y=title_y, fontsize=title_fontsize,
                     fontweight=title_fontweight)
    
    return fig
