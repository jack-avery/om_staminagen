###
#   Errors module for o!m 4K Stamina Generator utility
#   raspy#0292 - raspy_on_osu
###

class InvalidOsuModeError(Exception):
    """Raised when the osu! mode parsed is not mania."""
    pass

class NoInformationFoundError(Exception):
    """Raised when the osu! file has no uninherited timing points."""
    pass