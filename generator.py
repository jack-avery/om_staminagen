import os
import sys
import click
import logging
from datetime import datetime
import osuparser
from errors import InvalidOsuModeError, NoInformationFoundError

@click.command()
@click.option(
    "--osu",
    required=True,
    help="The path to the .osu file to generate into."
)
@click.option(
    "--until",
    required=True,
    help="The time to generate until, in seconds."
)
def generate(osu:str, until:int):
    """Generates the stamina bars.

    :param osu: The .osu file to generate into.

    :param until: The second to end generation on.
    """

    # Set up logging
    logger = logging.getLogger(__name__)

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)

    # Parse the .osu file
    logger.info(f"Attempting to parse {osu}...")
    osu_info = osuparser.parse(osu)
    logger.info("Parsed! Found:\n"
            +f"     starttime={osu_info['starttime']}\n"
            +f"     beatlength={osu_info['beatlength']}")

if __name__ == "__main__":
    generate()