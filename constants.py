"""Kickoff Project: constants.py

This file contains the Constants class which holds various constants used throughout the application.

This file is Copyright (c) 2023 Ram Raghav Sharma, Harshith Latchupatula, Vikram Makkar and Muhammad Ibrahim.
"""
from typing import Any


class Constants:
    """This class contains a dictionary of constants that are used throughout this application."""

    _constants: dict[str, Any] = {}

    def __init__(self) -> None:
        self._constants["USE_COLUMNS"] = [
            "HomeTeam",
            "AwayTeam",
            "FTHG",
            "FTAG",
            "FTR",
            "HTHG",
            "HTAG",
            "HTR",
            "HS",
            "AS",
            "HST",
            "AST",
            "HF",
            "AF",
            "HY",
            "AY",
            "HR",
            "AR",
            "Referee",
        ]
        self._constants[
            "HELP_COMMAND_INTRO"
        ] = "Kickoff is a football data analysis app that provides records and insights to football fans everywhere!"
        self._constants["VALID_SEASONS"] = [
            "2009-10",
            "2010-11",
            "2011-12",
            "2012-13",
            "2013-14",
            "2014-15",
            "2015-16",
            "2016-17",
            "2017-18",
            "2018-19",
        ]

    def retrieve(self, key: str) -> Any:
        """This function returns the corresponding constant when given the constant name.

        Preconditions:
            - key in self.constants
        """
        return self._constants[key]
