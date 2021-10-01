###
#   Main generation module for o!m 4K Stamina Generator utility
#   raspy#0292 - raspy_on_osu
###

import sys
import click
import logging
from datetime import datetime
import osuparser
import patterns

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
    time = osu_info['starttime']
    beat = osu_info['beatlength']
    logger.info("Parsed! Found:\n"
            +f"     starttime={time}\n"
            +f"     beatlength={beat}")

    om_note_template = '<pos>,192,<ms>,1,0,0:0:0:0:'

if __name__ == "__main__":
    generate()