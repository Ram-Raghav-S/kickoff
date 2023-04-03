"""Kickoff Project: models / match.py

This module contains the Match class and other related components.

This file is Copyright (c) 2023 Ram Raghav Sharma, Harshith Latchupatula, Vikram Makkar and Muhammad Ibrahim.
"""

from __future__ import annotations
from typing import Optional
from dataclasses import dataclass

from python_ta.contracts import check_contracts

import models.team as team


class Match:
    """A Premier League match between two teams in a particular season.

        Instance Attributes:
            - home_team: The team playing at its home ground in this match.
            - away_team: The team playing away from its home ground in this match.
            - order: The order in which this game is played in the corresonding season.
            - details: A mapping from each team name to its corresponding match details.
            - result: The team that won the match or None if the match was a draw

        Representation Invariants:
            - len(teams) == 2
            - self.season in ['2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', \
            '2017-18', '2018-19']
            - self.result in ['HOME_WIN', 'AWAY_WIN', 'DRAW']
            - 1 <= self.order
    """

    season: str
    home_team: team.Team
    away_team: team.Team
    order: int
    details: dict[str, MatchDetails]
    result: Optional[team.Team]

    def __init__(self, season: str, home_team: team.Team, away_team: team.Team, order: int, details: dict[str, MatchDetails], result: Optional[team.Team]) -> None:
        self.season = season
        self.home_team = home_team
        self.away_team = away_team
        self.order = order
        self.details = details
        self.result = result

    def get_other_team(self, team: team.Team) -> team.Team:
        """Return the other team that played in this match.
        
        Preconditions:
            - team in {self.home_team, self.away_team}
        """
        if team == self.home_team:
            return self.away_team
        else:
            return self.home_team

    def __repr__(self) -> str:
        return f"home: {self.home_team.name} vs away: {self.away_team.name}"
    



# @check_contracts
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

    team: team.Team
    fouls: int
    shots: int
    shots_on_target: int
    red_cards: int
    yellow_cards: int
    half_time_goals: int
    full_time_goals: int
    referee: str


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(
        config={
            "extra-imports": ["__future__", "datetime", "dataclasses", "team"],
            "allowed-io": [],
            "max-line-length": 120,
        }
    )
