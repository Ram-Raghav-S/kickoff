"""Kickoff Project: predictions.py

This module contains functionality for predicting future premier league match results.

This file is Copyright (c) 2023 Ram Raghav Sharma, Harshith Latchupatula, Vikram Makkar and Muhammad Ibrahim.
"""
import numpy as np

from models import League
from models import Match
from models import Team


def predict(home: str, away: str, season: str, league: League) -> float:
    """Predict the difference between the home and away teams' scores in
    a match between them based on data from matches in the specified season.

    The returned number is a float to retain accuracy of the prediction.

    Preconditions:
        - league.team_in_league(home_team)
        - league.team_in_league(away_team)
        - home in league.get_team_names(season)
        - away in league.get_team_names(season)
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
    """
    # depth 4 enables fast predictions while maintaining accuracy
    PREDICTION_DEPTH = 4
    home_team = league.get_team(home)
    away_team = league.get_team(away)
    paths = _find_all_paths(home_team, away_team, season, PREDICTION_DEPTH)

    goal_diffs = []
    weights = []

    for path in paths:
        weights.append(1 / len(path))
        total_diff = 0
        for i, match in enumerate(path):
            if i % 2 == 0:
                left_team_goals = match.details[match.home_team.name].full_time_goals
                right_team_goals = match.details[match.away_team.name].full_time_goals
            else:
                left_team_goals = match.details[match.away_team.name].full_time_goals
                right_team_goals = match.details[match.home_team.name].full_time_goals

            goal_diff = left_team_goals - right_team_goals
            total_diff += goal_diff
        goal_diffs.append(total_diff)

    predicted_home_goal_diff = np.average(goal_diffs, weights=weights)
    return predicted_home_goal_diff


def _find_all_paths(home_team: Team, away_team: Team, season: str, depth: int) -> list[list[Match]]:
    """Return a list of all paths of matches of length <= depth, starting with a match
    where home_team plays at home and ending with a match where away_team plays away from home.

    Preconditions:
        - league.team_in_league(home_team.name)
        - league.team_in_league(away_team.name)
        - home_team.name in league.get_team_names(season)
        - away_team.name in league.get_team_names(season)
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
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
            condition1 = match.season != season
            condition2 = other_team.name in visited
            condition3 = not at_home and (match.away_team == other_team)
            condition4 = at_home and (match.home_team == other_team)

            if any({condition1, condition2, condition3, condition4}):
                continue
            path.append(match)
            dfs(other_team, path, not at_home)
            path.pop()

        visited.remove(team.name)

    dfs(home_team, [], True)

    return paths
