"""Kickoff Project: controllers / records.py

This module contains functionality for predicting future premier league matches.

This file is Copyright (c) 2023 Ram Raghav Sharma, Harshith Latchupatula, Vikram Makkar and Muhammad Ibrahim.
"""
import numpy as np

from models.league import League
from models.match import Match
from models.team import Team
from utils.constants import Constants
contants = Constants()


def predict(home: str, away: str, season: str, league: League) -> float:
    """Predict the difference between the home and away teams' scores in
    a match between them based on data from matches in the specified season.

    The returned number is a float to retain accuracy of the prediction.

    Preconditions: 
        - league.team_in_league(home_team)
        - league.team_in_league(away_team)
        - home team has played in the season
        - away team has played in the season
        - season in constants.retrieve constants
    """
    # depth 4 enables fast predictions while maintaining accuracy
    PREDICTION_DEPTH = 4
    home_team = league.get_team(home)
    away_team = league.get_team(away)
    paths = _find_all_paths(home_team, away_team, season, PREDICTION_DEPTH)

    home_goal_diffs = []
    weights = []

    for path in paths:
        weights.append(1 / len(path))
        total_diff = 0
        for match in path:
            home_team_goals = match.details[match.home_team.name].full_time_goals
            away_team_goals = match.details[match.away_team.name].full_time_goals
            home_goal_diff = home_team_goals - away_team_goals
            total_diff += home_goal_diff
        home_goal_diffs.append(total_diff)

    predicted_home_goal_diff = np.average(home_goal_diffs, weights=weights)
    return predicted_home_goal_diff


def _find_all_paths(home_team: Team, away_team: Team, season: str, depth: int) -> list[list[Match]]:
    """Return a list of all paths of matches of length <= depth, starting with a match 
    where home_team plays at home and ending with a match where away_team plays away from home.
    """
    paths: list[list[Match]] = []
    visited: set[str] = set()  # set of all team names that have been visited

    def dfs(team: Team, path: list[Match], at_home: bool) -> None:
        """DFS helper for _find_all_paths"""
        if len(path) > depth:
            return

        if path and path[-1].away_team == away_team:  # found a complete path
            paths.append(path.copy())
            return

        visited.add(team.name)

        for match in team.matches:
            other_team = match.get_other_team(team)
            if match.season != season or \
                other_team.name in visited or \
                (not at_home and (match.away_team == other_team)) or \
                    (at_home and (match.home_team == other_team)):
                continue

            path.append(match)
            dfs(other_team, path, not at_home)
            path.pop()

        visited.remove(team.name)

    dfs(home_team, [], True)

    return paths
