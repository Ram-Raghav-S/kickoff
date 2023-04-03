"""Kickoff Project: errors.py

This module contains various error checking functions for the commands.py file.

This file is Copyright (c) 2023 Ram Raghav Sharma, Harshith Latchupatula, Vikram Makkar and Muhammad Ibrahim.
"""
import output as io
from models import League
from constants import Constants


def validate_team(league: League, team_input: str) -> None:
    """Check if the given team is in the League. If not, print an error."""
    if not league.team_in_league(team_input):
        io.error("The given team is not a valid team.")


def validate_season(season_input: str) -> None:
    """Check if the given season is in the list of datasets. If not, print an error."""
    constants = Constants()
    if season_input is not None and season_input not in constants.retrieve("VALID_SEASONS"):
        io.error("The given season is not in the format '20XX-XX' between 2009-10 and 2018-19.")


def validate_team_in_season(league: League, team_input: str, season_input: str) -> None:
    """Check if the given team played in the given season. If not, print an error."""
    if season_input is not None and season_input not in league.get_team(team_input).seasons:
        io.error("This team did not play a match in the given season.")


def validate_topx(topx_input: int, topx_max: int = None) -> None:
    """Check if the given topx input is less than the given topx maximum. If not, print an error."""
    if topx_max is not None:
        if not 0 < topx_input <= topx_max:
            io.error(f"The top x value should be greater than 0 and less than {topx_max}")
    else:
        if not 0 < topx_input:
            io.error("The top x value should be greater than 0")
