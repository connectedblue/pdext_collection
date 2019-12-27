# default functions used to create plot
# These may be substituted for custom functions
# if required
def default_legend_tick(values, round_to=1):
    def round_to(x, base=round_to):
        return base * round(x/base)
    minv = min(values)
    maxv = max(values)
    ticks = [minv, round_to((minv + maxv)/2) ,maxv]
    tick_labels = [str(round_to(l)) for l in ticks]
    return ticks, tick_labels

def default_label_format(c):
    return str(c)

def wedge_defaults(num_wedges):
    defaults = {
         1:{
    'colours': ["Purples"],
    'radius': [0.5],
    'wedge_width': [0.3],
    'slice_labels': None,
    },
        2:{
    'colours': ["Purples", "Greens"],
    'radius': [0.5, 0.7],
    'wedge_width': [0.3, 0.2],
    'slice_labels': None,
    },
         3:{
    'colours': ["Purples", "Greens", "OrRd" ],
    'radius': [0.5, 0.7, 0.9],
    'wedge_width': [0.3, 0.2, 0.2],
    'slice_labels': None,
    },
        4: {
    'colours': ["Purples", "Greens", "OrRd", "Blues" ],
    'radius': [0.5, 0.7, 0.9, 1.1],
    'wedge_width': [0.3, 0.2, 0.2, 0.2],
    'slice_labels': None,
    },
        5: {
    'colours': ["Purples", "Greens", "OrRd", "Blues", "RdPu" ],
    'radius': [0.5, 0.7, 0.9, 1.1, 1.3],
    'wedge_width': [0.3, 0.2, 0.2, 0.2, 0.2],
    'slice_labels': None,
    },
    }
    try:
        return defaults[num_wedges]
    except KeyError:
        return {
            'colours': None,
            'radius': None,
            'wedge_width': None,
            'slice_labels': None,
        }
