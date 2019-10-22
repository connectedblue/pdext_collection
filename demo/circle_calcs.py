"""
An example pandas dataframe extension that can be added
and shared easily using the pdext framework
"""

from math import pi

def circle_calculations(df, radius='radius'):
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

    df['circumference'] = 2 * pi * df[radius]
    df['area'] = pi * df[radius] ** 2

    # extra comment for test
    # extra comment for tag1