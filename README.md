## o!m Stamina Generator utility
Automatic, primitive stamina generator utility for osu! Mania charts.

Contact me at `raspy#0292` on Discord about bugs and glitches.

Installing:
1. Download [Python version 3.6.5+](https://www.python.org/downloads/)
2. Download the Source Code (using [git](https://git-scm.com/downloads) or otherwise)
3. Run this command in a console in the installation folder to install requirements:
```
pip install -r requirements.txt
```

## Usage
1. Ensure that your .osu file is in **Mania-only** mode. (Mode: 3)
2. Have your first **uninherited** timing point be where you want the program to start charting.
3. Have **no notes placed**, meaning the .osu file is empty after [HitObjects].
4. Run this command, replacing <> with appropriate information:
```
generator.py --osu <path_to_.osu_file> --until <time_in_seconds>
```
