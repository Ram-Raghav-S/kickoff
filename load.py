"""Kickoff Project: load.py

This file contains various functions that load the dataset CSV files into a graph.

This file is Copyright (c) 2023 Ram Raghav Sharma, Harshith Latchupatula, Vikram Makkar and Muhammad Ibrahim.
"""

import os
import time
import pandas as pd
from rich.progress import Progress, SpinnerColumn, TextColumn

from constants import Constants
from models import League
from models import Match, MatchDetails


def load_csv_files() -> League:
    """Loads all csv files in /assets into a League class and returns it"""
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Retrieving datasets...", total=None)

        files = [file for file in os.listdir("./assets") if "csv" in file]
        file_paths = ["./assets/" + file for file in files]
        time.sleep(0.5)

        progress.add_task(description="Parsing data...", total=None)
        dataframes = [generate_pandas_dataframe(path) for path in file_paths]
        time.sleep(0.5)

        progress.add_task(description="Generating graph...", total=None)
        league = League()
        for i, dataframe in enumerate(dataframes):
            season = files[i][:7]
            convert_to_graph(dataframe, league, season)

        time.sleep(0.5)

    return league


def generate_pandas_dataframe(csv_file: str) -> pd.DataFrame:
    """Initializes a DataTable class with the provided csv_file name and season.

    Preconditions:
        - csv_file is a valid csv file stored in the assets folder
    """
    constants = Constants()
    dataframe = pd.read_csv(csv_file, usecols=constants.retrieve("USE_COLUMNS"))
    return dataframe


def convert_to_graph(dataframe: pd.DataFrame, league: League, season: str) -> None:
    """Populate the graph with the provided dataframe representing the match and overall season statistics

    Preconditions:
        - dataframe is a valid representation of a csv file stored in the assets folder
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
    """
    for i in range(len(dataframe.index)):
        ht_name = dataframe["HomeTeam"][i]
        at_name = dataframe["AwayTeam"][i]

        if not league.team_in_league(ht_name):
            home_team = league.add_team(ht_name)
        else:
            home_team = league.get_team(ht_name)

        if not league.team_in_league(at_name):
            away_team = league.add_team(at_name)
        else:
            away_team = league.get_team(at_name)

        league.add_season_to_team(ht_name, season)
        league.add_season_to_team(at_name, season)

        home_team_details = MatchDetails(
            team=home_team,
            fouls=dataframe["HF"][i],
            shots=int(dataframe["HS"][i]),
            shots_on_target=int(dataframe["HST"][i]),
            red_cards=int(dataframe["HR"][i]),
            yellow_cards=int(dataframe["HY"][i]),
            half_time_goals=int(dataframe["HTHG"][i]),
            full_time_goals=int(dataframe["FTHG"][i]),
            referee=dataframe["Referee"][i],
        )
        away_team_details = MatchDetails(
            team=away_team,
            fouls=dataframe["AF"][i],
            shots=int(dataframe["AS"][i]),
            shots_on_target=int(dataframe["AST"][i]),
            red_cards=int(dataframe["AR"][i]),
            yellow_cards=int(dataframe["AY"][i]),
            half_time_goals=int(dataframe["HTAG"][i]),
            full_time_goals=int(dataframe["FTAG"][i]),
            referee=dataframe["Referee"][i],
        )

        if dataframe["FTR"][i] == "H":
            result = home_team
        elif dataframe["FTR"][i] == "A":
            result = away_team
        else:
            result = None

        details = {ht_name: home_team_details, at_name: away_team_details}
        match = Match(
            season=season, home_team=home_team, away_team=away_team, order=(i + 1), details=details, result=result
        )

        league.add_match(ht_name, at_name, match)
