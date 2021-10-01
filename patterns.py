###
#   Patterns file for o!m 4K Stamina Generator utility
#   raspy#0292 - raspy_on_osu
###

"""
Patterns module for o!m 4K Stamina Generator utility

Creating your own patterns:

Assuming you use DF JK controls:
1 = D
2 = F
3 = J
4 = K

e.g. a pattern that would go DFJKJFD would be 1234321.

Each pattern is spaced so that each note is on a 1/4 tick.

Checks are done automatically to ensure no jacks are in the map.

These patterns may be flipped horizontally or vertically.
"""

# A list of patterns. See above comment for how to add your own.
patterns = [
    '121',
    '12321',
    '1234',
    '1234231',
    '123424',
    '2314',
    '314'
]

def flip_horizontal(pattern:str) -> str:
    """Flip a pattern horizontally.
    
    :param pattern: The pattern to flip horizontally.
    """
    pattern = [char for char in pattern]

    for i,c in enumerate(pattern):
        if c=='1':
            pattern[i]='4'
        elif c=='2':
            pattern[i]='3'
        elif c=='3':
            pattern[i]='2'
        else:
            pattern[i]='1'
    
    return ''.join(pattern)

def flip_vertical(pattern:str) -> str:
    """Flip a pattern vertically.

    :param pattern: The pattern to flip vertically.
    """
    return pattern[::-1]

def would_jack(pattern1:str,pattern2:str) -> bool:
    """Determines whether two patterns would create a jack.

    :param pattern1: The first pattern.

    :param pattern2: The second pattern.
    """
    if pattern1[-1] == pattern2[0]:
        return True
    else:
        return False

def convert_to_pos(pattern:str) -> list:
    """Converts the pattern to a list of osu! mania positions.

    :param pattern: The pattern to convert.
    """
    pattern = [char for char in pattern]

    for i,c in enumerate(pattern):
        if c=='1':
            pattern[i]='64'
        elif c=='2':
            pattern[i]='192'
        elif c=='3':
            pattern[i]='320'
        else:
            pattern[i]='448'

    return pattern