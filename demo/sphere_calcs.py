"""
An example pandas dataframe extension that can be added
and shared easily using the pdext framework
"""

from math import pi

def sphere_calculations(df, radius='radius'):
    """
    Calculates the circumference and area of a circle 
    given a column of radius and adds the result to the
    dataframe
    Input:
        df -- dataframe
        radius -- column name containing the radius values
    """
    if radius not in df.columns:
        raise IndexError('Radius column {} not in dataframe')

    df['surface_area'] = 4 * pi * df[radius] ** 2
    df['volume'] = (4 / 3) * pi * df[radius] ** 3