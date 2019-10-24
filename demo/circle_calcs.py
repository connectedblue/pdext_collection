"""
An example pandas dataframe extension that can be added
and shared easily using the pdext framework
"""

from math import pi

def circle_calculations(df, radius='radius'):
    """
    Version: pdext_test_tag tag
    """
    if radius not in df.columns:
        raise IndexError('Radius column {} not in dataframe')

    df['circumference'] = 2 * pi * df[radius]
    df['area'] = pi * df[radius] ** 2