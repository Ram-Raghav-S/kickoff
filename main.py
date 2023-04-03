"""Kickoff Project: main.py

This module creates the overall Typer application that is used to read commands / options
from the user as a CLI. Primarily, it exports the app variable to all other files.

This file is Copyright (c) 2023 Ram Raghav Sharma, Harshith Latchupatula, Vikram Makkar and Muhammad Ibrahim.
"""

from commands import app

if __name__ == "__main__":
    app()
