"""Kickoff Project: models / team.py

This module contains the Team class and other related components.

This file is Copyright (c) 2023 Ram Raghav Sharma, Harshith Latchupatula, Vikram Makkar and Muhammad Ibrahim.
"""

from __future__ import annotations
from dataclasses import dataclass
from python_ta.contracts import check_contracts


from models.match import Match


class Team:
    """A football team playing in a particular season of the Premier League.

    Instance Attributes:
        - name: The name of this team.
        - matches: A chronologically ordered list of the matches played by this team in the season.
        - seasons: The seasons this team has participated in.

    Representation Invariants:
        - len(self.matches) > 0
        - len(self.seasons) > 0
    """

    name: str
    matches: list[Match]
    seasons: set[str]

    def __init__(self, name: str, matches: list[Match], seasons: set[str]) -> None:
        self.name = name
        self.matches = matches
        self.seasons = seasons


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(
        config={
            "extra-imports": ["__future__", "dataclasses", "match"],
            "allowed-io": [],
            "max-line-length": 120,
        }
    )
