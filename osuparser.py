###
#   .osu parser for o!m Stamina Generator utility
#   raspy#0292 - raspy_on_osu
###

import re
from errors import InvalidOsuModeError, NoInformationFoundError

def parse(osu: str) -> dict:
    """Parses the provided .osu file and returns
    all relevant information formatted into a dict.

    Provides this information in the dict as keys:

    starttime

    beatlength

    :param osu: The path to the .osu file.
    """
    with open(osu, "r", encoding="utf-8") as osufile:
        lines = osufile.readlines()

    # Parsing the file initially
    invalid_mode_re = re.compile('(Mode:\s[0-2]+)')
    for i,line in enumerate(lines):

        # If the mode is not osu!mania, raise an InvalidOsuModeError
        if invalid_mode_re.match(line):
            raise InvalidOsuModeError(f"{osu} is not osu!mania mode")

        # Finding our timing points
        if "[TimingPoints]" in line:
            lines = lines[i+1:]
            break

    # Finding our first uninherited timing point
    # Format expected: 334,285.714285714286,4,1,0,100,1,0
    # ... meaning inheritance bool would be on line[6]
    for i,line in enumerate(lines):
        line = line.split(",")
        if line[6] == '1':
            return {"starttime": int(line[0]), "beatlength": float(line[1])}
        
        # If there are no uninherited timing points found
        # (we reached HitObjects), raise a NoInformationFoundError
        if "[HitObjects]" in line:
            raise NoInformationFoundError(f"{osu} has no uninherited timing points")