"""Kickoff Project: models.py

This module contains all the classes used throughout the program.

This file is Copyright (c) 2023 Ram Raghav Sharma, Harshith Latchupatula, Vikram Makkar and Muhammad Ibrahim.
"""

from __future__ import annotations
from typing import Optional
from dataclasses import dataclass


class Match:
    """A Premier League match between two teams in a particular season.

        Instance Attributes:
            - home_team: The team playing at its home ground in this match.
            - away_team: The team playing away from its home ground in this match.
            - order: The order in which this game is played in the corresonding season.
            - details: A mapping from each team name to its corresponding match details.
            - result: The team that won the match or None if the match was a draw

        Representation Invariants:
            - self.season in {'2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', \
            '2017-18', '2018-19'}
            - self.result in {self.home_team, self.away_team}
            - self.home_team.name in self.details and self.away_team.name in self.details
            - 1 <= self.order
    """

    season: str
    home_team: Team
    away_team: Team
    order: int
    details: dict[str, MatchDetails]
    result: Optional[Team]

    def __init__(
        self,
        season: str,
        home_team: Team,
        away_team: Team,
        order: int,
        details: dict[str, MatchDetails],
        result: Optional[Team],
    ) -> None:
        self.season = season
        self.home_team = home_team
        self.away_team = away_team
        self.order = order
        self.details = details
        self.result = result

    def get_other_team(self, known_team: Team) -> Team:
        """Return the other team that played in this match.

        Preconditions:
            - team in {self.home_team, self.away_team}
        """
        if known_team == self.home_team:
            return self.away_team
        return self.home_team

    def __repr__(self) -> str:
        return f"Home: {self.home_team.name} vs Away: {self.away_team.name}"


@dataclass(repr=True)
class MatchDetails:
    """The details of a team's performance in a Premier League match.

    Instance Attributes:
        - team: The team this MatchDetails refers to
        - fouls: number of fouls commited by the team in the match
        - shots: number of shots taken by the team in the match
        - shots_on_target: number of shots that were on target by the team in the match
        - red_cards: number of red cards given to the team in the match
        - yellow_cards: number of yellow cards given to the team in the match
        - half_time_goals: number of goals scored by the team at half time
        - full_time_goals: number of goals scored by the team at full time
        - referee: the name of the referee that officiated this match

    Representation Invariants:
        ...
    """

    team: Team
    fouls: int
    shots: int
    shots_on_target: int
    red_cards: int
    yellow_cards: int
    half_time_goals: int
    full_time_goals: int
    referee: str


@dataclass
class Team:
    """A football team playing in a particular season of the Premier League.

    Instance Attributes:
        - name: The name of this team.
        - matches: A chronologically ordered list of the matches played by this team in the season.
        - seasons: The seasons this team has participated in.

    Representation Invariants:
        - len(self.matches) > 0
        - len(self.seasons) > 0
        - all({ self == match.home_team or self == match.away_team for match in self.matches })
    """

    name: str
    matches: list[Match]
    seasons: set[str]


class League:
    """A graph-based representation of Premier League matches and teams.

    Instance Attributes:
        - teams: A mapping containing the teams playing in this season and the corresponding Team object.
        - matches: A chronologically ordered list of all matches played in this season.

    Representation Invariants:
        - all({ name == self.teams[name].name for name in self.teams })
    """

    _teams: dict[str, Team]

    def __init__(self) -> None:
        self._teams = {}

    def add_team(self, name: str) -> Team:
        """Add a new team with the given team name to this league and return it.

        Preconditions
            - name not in self._teams
        """
        team = Team(name=name, matches=[], seasons=set())
        self._teams[name] = team
        return team

    def add_season_to_team(self, team: str, season: str) -> None:
        """Add a new season to the given team.

        Preconditions
            - name in self._teams
            - season is a season string in the format '20XX-XX' between 2009-10 and 2018-19
        """
        self._teams[team].seasons.add(season)

    def add_match(self, team1: str, team2: str, match: Match) -> None:
        """Add a new match between the two given teams.
        Add each team to the league if they have not been added already.

        Preconditions
            - team1 in {match.away_team.name, match.home_team.name}
            - team2 in {match.away_team.name, match.home_team.name}
            - team1 != team2
        """
        if team1 not in self._teams:
            self.add_team(team1)
        if team2 not in self._teams:
            self.add_team(team2)

        self._teams[team1].matches.append(match)
        self._teams[team2].matches.append(match)

    def team_in_league(self, name: str) -> bool:
        """Check if the given team exists within this league by the given name"""
        return name in self._teams

    def get_team(self, name: str) -> Team:
        """Retrieve a specific team object based on the given name

        Preconditions
            - name in self._teams
        """
        return self._teams[name]

    def get_team_names(self, season: Optional[str] = None) -> list[str]:
        """Retreive the names of the teams in the league. If the season attribute is provided
        then this function will only return teams that have played in that season.

        Preconditions:
            - season is a season string in the format '20XX-XX' between 2009-10 and 2018-19 or season is None
        """
        team_names = list(self._teams.keys())
        if season is None:
            return team_names

        return [team_name for team_name in team_names if season in self.get_team(team_name).seasons]
