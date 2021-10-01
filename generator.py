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

    # The template for osu! Mania hitnotes.
    OM_NOTE_TEMPLATE = '<pos>,192,<ms>,1,0,0:0:0:0:'

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

    # Set up for notes creation
    notes = list()
    patternlist = patterns.patterns
    logger.info("Generating notes...")

    # Generate new patterns until the specified time is reached
    previous_pattern = '0'
    current_pattern = '0'
    while time < until:
        while current_pattern == previous_pattern:
            current_pattern = patternlist[randint(0,len(patternlist)-1)]

            # Determine whether this should vertically flip (see VERTICAL_FLIP_CHANCE)
            if randint(0,VERTICAL_FLIP_CHANCE) == VERTICAL_FLIP_CHANCE:
                current_pattern = patterns.flip_vertical(current_pattern)

            # Determine whether the patterns would result in a jack,
            # and flip horizontally if they would to avoid this
            if patterns.would_jack(previous_pattern,current_pattern):
                current_pattern = patterns.flip_horizontal(current_pattern)
        
        # Generate the notes from the pattern chosen...
        for note in patterns.convert_to_pos(current_pattern):
            # Replacing info in the template to generate the note
            note = OM_NOTE_TEMPLATE.replace("<pos>",note)
            note = note.replace("<ms>",str(mstime))

            # Adding newline and appending to notes list
            note += "\n"
            notes.append(note)

            # Advancing time forward and rounding for ms time
            time+=beat/4
            mstime = round(time)

        # Designate the current pattern as the previous.
        previous_pattern = current_pattern
    
    # Write the new notes to the file.
    logger.info("Generated! Writing to file...")
    with open(osu,"r") as osufile:
        lines = osufile.readlines()

    lines+=notes

    with open(osu,"w") as osufile:
        osufile.writelines(lines)

    # Inform the user that the operation is complete.
    logger.info("Done!")

if __name__ == "__main__":
    generate()