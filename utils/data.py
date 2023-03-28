"""Kickoff Project: utils / data.py

This file contains various functions that utilize the provided datasets and transform them into 
pandas DataFrames and League graphs.

This file is Copyright (c) 2023 Ram Raghav Sharma, Harshith Latchupatula, Vikram Makkar and Muhammad Ibrahim.
"""

import pandas as pd
from python_ta.contracts import check_contracts

from utils.constants import Constants
from models.league import League
from models.match import Match, MatchDetails
from models.team import Team
from datetime import datetime


@check_contracts
def generate_pandas_df(csv_file: str) -> pd.DataFrame:
    """Initialize a DataTable class with the provided csv_file name and season.

    Preconditions:
        - csv_file is a valid csv file stored in the assets folder
    """
    constants = Constants()
    dataframe = pd.read_csv(
        csv_file, usecols=constants.retrieve("USE_COLUMNS"), parse_dates=constants.retrieve("DATE_COLUMNS")
    )
    return dataframe


@check_contracts
def convert_to_graph(dataframe: pd.DataFrame, league: League) -> None:
    """Populate the graph with the provided dataframe representing the match and overall season statistics

    Preconditions:
        - dataframe is a valid representation of a csv file stored in the assets folder
    """
    
    # TODO: Not sure how to work with pandas dataframe, someone take a look and edit as necessary
    for i in len(dataframe.index):  
        
        if dataframe["HomeTeam"][i] not in league.teams:
            home_team = Team(dataframe["HomeTeam"][i], [])
        else:
            home_team = league.teams[dataframe["HomeTeam"][i]]

        if dataframe["AwayTeam"][i] not in league.teams:
            away_team = Team(dataframe["AwayTeam"][i], [])
        else:
            away_team = league.teams[dataframe["AwayTeam"][i]]
        

        home_team_details = MatchDetails(home_team, dataframe["HF"][i], dataframe["HS"][i], dataframe["HST"][i], dataframe["HR"][i], dataframe["HY"][i], dataframe["HTHG"][i], dataframe["FTHG"][i])
        away_team_details = MatchDetails(away_team, dataframe["AF"][i], dataframe["AS"][i], dataframe["AST"][i], dataframe["AR"][i], dataframe["AY"][i], dataframe["HTAG"][i], dataframe["FTAG"][i])
        result_status = {"H": "HOME_WIN", "A": "AWAY_WIN", "D": "DRAW"}

        # TODO: Fix season attribute
        date_time = datetime.strptime(dataframe["Date"][i], "%m/%d/%y")
        match = Match('season', home_team, away_team, date_time, {home_team: home_team_details, away_team: away_team_details}, result_status[dataframe["FTR"][i]])
        home_team.matches.append(match)
        away_team.matches.append(match)
        league.matches.append(match)

if __name__ == "__main__":
    import python_ta

    python_ta.check_all()
