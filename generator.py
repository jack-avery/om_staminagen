###
#   Main generation module for o!m 4K Stamina Generator utility
#   raspy#0292 - raspy_on_osu
###

import sys
import logging
from random import randint
import click
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

    # The chance for a pattern vertical flip to occur,
    # as 1 / VERTICAL_FLIP_CHANCE
    VERTICAL_FLIP_CHANCE = 2

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
    mstime = time
    beat = osu_info['beatlength']
    until = int(until)*1000 # Converting until into MS for time comparison

    logger.info("Parsed! Found:\n"
            +f"     starttime={time}\n"
            +f"     beatlength={beat}")

    om_note_template = '<pos>,192,<ms>,1,0,0:0:0:0:'
    notes = list()
    patternlist = patterns.patterns
    
    logger.info("Generating notes...")
    previous_pattern = '0'
    while time < until:
        current_pattern = patternlist[randint(0,len(patternlist)-1)]

        if randint(0,VERTICAL_FLIP_CHANCE) == VERTICAL_FLIP_CHANCE:
            current_pattern = patterns.flip_vertical(current_pattern)

        if patterns.would_jack(previous_pattern,current_pattern):
            current_pattern = patterns.flip_horizontal(current_pattern)
        
        for note in patterns.convert_to_pos(current_pattern):
            note = om_note_template.replace("<pos>",note)
            note = note.replace("<ms>",str(mstime))
            note += "\n"
            notes.append(note)

            time+=beat/4
            mstime = round(time)

        previous_pattern = current_pattern
    
    logger.info("Generated! Writing to file...")
    with open(osu,"r") as osufile:
        lines = osufile.readlines()

    lines+=notes

    with open(osu,"w") as osufile:
        osufile.writelines(lines)

    logger.info("Done!")

if __name__ == "__main__":
    generate()