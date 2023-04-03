"""Kickoff Project: cmd / commands.py

This module sets up various CLI commands that the user can use to interact with our application. 
It simply parses user commands and ensures that inputs are acceptable and delegates the actual functionality 
to other functions / classes.

This file is Copyright (c) 2023 Ram Raghav Sharma, Harshith Latchupatula, Vikram Makkar and Muhammad Ibrahim.
"""

import cmd.output as io
import cmd.errors as errors
from typing import Optional
from rich.progress import Progress, SpinnerColumn, TextColumn
import typer

from utils import constants, data
from controllers import basic, records, optimization, predictions

league = data.load_csv_files()
constants = constants.Constants()
app = typer.Typer(help=constants.retrieve("HELP_COMMAND_INTRO"))


@app.command()
def winrate(
    team: str = typer.Option(...), season: Optional[str] = typer.Option(default=None, help="ex. 2009-10")
) -> None:
    """Outputs the winrate percent of the specified team.
    If season is specified, the winrate will be calculated only for the season.

    Preconditions
        - team is a valid team
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
        - If season is specified, team must have played a match in the season
    """
    errors.validate_team(league, team)
    if season is not None:
        errors.validate_season(season)
        errors.validate_team_in_season(league, team, season)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")

        winrate_percent = round(basic.overall_winrate(league, team, season), 2)

        if season is None:
            display_str = f"[yellow]{team}'s[/yellow] winrate across all Premier League seasons is {winrate_percent}%."
        else:
            display_str = (
                f"[yellow]{team}'s[/yellow] winrate in the [magenta]{season}[/magenta] season is {winrate_percent}%."
            )

    io.info(message=display_str, color="white")


@app.command()
def averages(team: str = typer.Option(...), season: str = typer.Option(..., help="ex. 2009-10")) -> None:
    """Outputs various team statistics compared to the overall league statistics for the specified season.

    Preconditions:
        - team is a valid team
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
    """
    errors.validate_team(league, team)
    errors.validate_season(season)
    errors.validate_team_in_season(league, team, season)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")

        updated_data = []
        average_data = [
            [
                "Average Goals Scored / Game",
                round(basic.get_team_goals_scored(league, team, season), 2),
                round(basic.get_season_goals_scored(league, season), 2),
            ],
            [
                "Average Shot Accuracy (%)",
                round(basic.get_team_shot_accuracy(league, team, season), 2),
                round(basic.get_season_shot_accuracy(league, season), 2),
            ],
            [
                "Average Fouls Committed / Game",
                round(basic.get_team_fouls(league, team, season), 2),
                round(basic.get_season_fouls(league, season), 2),
            ],
            [
                "Average Card Offenses / Game",
                round(basic.get_team_cards(league, team, season), 2),
                round(basic.get_season_cards(league, season), 2),
            ],
        ]

        for row in average_data:
            if row[1] - row[2] > 0:
                updated_data.append((row[0], row[1], row[2], f"+{round(row[1] - row[2], 2)}"))
            else:
                updated_data.append((row[0], row[1], row[2], round(row[1] - row[2], 2)))

        title = f"{team} Statistics Compared to League Averages in the {season} Premier League Season"
    io.table(
        title=title,
        headers=["Statistic", f"{team}", "League", "Difference"],
        colors=["cyan", "magenta", "yellow", "green"],
        data=updated_data,
        width=100,
    )


@app.command()
def homevsaway(
    team: str = typer.Option(default=None),
    season: str = typer.Option(default=None, help="ex. 2009-10"),
) -> None:
    """Outputs the home vs away winrates for the given team in the given season.
    If no team or season is provided, calculations will be done for the whole league.

    Preconditions:
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
    """
    if season is not None:
        errors.validate_season(season)
    if team is not None:
        errors.validate_team(league, team)
    if team is not None and season is not None:
        errors.validate_team_in_season(league, team, season)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")

        home_vs_away = basic.home_vs_away(league, team, season)
        if team is None and season is None:
            title = "Home vs Away Winrates in the Premier League"
        elif team is None and season is not None:
            title = f"Home vs Away Winrates in the {season} Premier League Season"
        else:
            title = f"Home vs Away Winrates for {team} in the {season} Premier League Season"

    io.table(
        title=title,
        headers=["Home Win Rate (%)", "Away Win Rate (%)", "Total Draw Rate (%)"],
        colors=["cyan", "magenta", "cyan"],
        data=home_vs_away,
        width=70,
    )


@app.command()
def streaks(
    season: str = typer.Option(..., help="ex. 2009-10"),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the longest win streaks statistic for the specified season.

    Preconditions:
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
    """
    errors.validate_season(season)
    errors.validate_topx(topx)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")

        highest_streaks = records.highest_win_streaks(league, season, topx)
    io.table(
        title=f"Top {len(highest_streaks)} Highest Win Streaks in the {season} Premier League",
        headers=["Team", "Streak Length"],
        colors=["cyan", "magenta"],
        data=highest_streaks,
        width=70,
    )


@app.command()
def comebacks(
    season: str = typer.Option(default=None, help="ex. 2009-10"),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the winrate statistic for the specified team & season.
    If no arguments are found, the statistic will be calculated for all teams and seasons.

    Preconditions
        - team is a valid team
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
        - topx > 0
    """
    if season is not None:
        errors.validate_season(season)
    errors.validate_topx(topx)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")

        best_comebacks = records.best_comebacks(league, season, topx)

        if season is None:
            title = f"Top {len(best_comebacks)} Best Comebacks Teams in the Premier League"
        else:
            title = f"Top {len(best_comebacks)} Best Comebacks Teams in the {season} Premier League Season"

    io.table(
        title=title,
        headers=["Team", "Half-Time Score", "Full-Time Score", "Comeback Size"],
        colors=["cyan", "magenta", "yellow", "green"],
        data=best_comebacks,
        width=100,
    )


@app.command()
def goals(
    season: str = typer.Option(default=None, help="ex. 2009-10"),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the winrate statistic for the specified team & season.
    If no arguments are found, the statistic will be calculated for all teams and seasons.

    Preconditions
        - team is a valid team
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
        - topx > 0
    """
    if season is not None:
        errors.validate_season(season)
    errors.validate_topx(topx)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")

        most_goals = records.most_goals_scored(league, season, topx)
        if season is None:
            title = f"Top {len(most_goals)} Most Goals Scored Games in the Premier League"
        else:
            title = f"Top {len(most_goals)} Most Goals Scored Games in the {season} Premier League Season"
    io.table(
        title=title, headers=["Team", "Most Goals In a Game"], colors=["cyan", "magenta"], data=most_goals, width=90
    )


@app.command()
def fairplay(
    season: str = typer.Option(default=None, help="ex. 2009-10"),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the topx most fairplay teams for the specified season.
    If no arguments are found, the statistic will be calculated for all teams and seasons.

    Preconditions
        - season is in the format '20XX-XX' between 2009-10 and 2018-19 or season is None
        - topx > 0
    """
    if season is not None:
        errors.validate_season(season)
    errors.validate_topx(topx)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")

        most_fairplay = records.most_fairplay(league, season, topx)

        if season is None:
            title = f"Top {len(most_fairplay)} Most Fairplay Teams in the Premier League"
        else:
            title = f"Top {len(most_fairplay)} Most fairplay teams in the {season} Premier League Season"

    io.table(
        title=title,
        headers=["Team", "Offenses Per Match Ratio"],
        colors=["cyan", "yellow"],
        data=most_fairplay,
        width=120,
    )


@app.command()
def improvement(
    season: str = typer.Option(..., help="ex. 2009-10"),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Output the topx most improved teams in the season.

    Preconditions
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
        - 0 < topx <= 20
    """
    errors.validate_season(season)
    errors.validate_topx(topx, 20)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")

        most_improved = records.most_improved_teams(league, season, topx)
        title = f"Top {len(most_improved)} Most Improved Teams in the {season} Premier League Season"

    io.table(
        title=title,
        headers=["Team", "Lowest Win (%)", "Final Winrate (%)", "Winrate Improvement (%)"],
        colors=["cyan", "magenta", "cyan", "magenta"],
        data=most_improved,
        width=80,
    )


@app.command()
def optimalfouls(
    team: str = typer.Option(default=None),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the optimal fouls for the provided team.

    Preconditions
        - team is a valid team
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
        - topx > 0
    """
    if team is not None:
        errors.validate_team(league, team)
    errors.validate_topx(topx)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")
        optimal_fouls = optimization.calculate_optimal_fouls(league, team, topx)

        if team is None:
            title = f"Top {len(optimal_fouls)} Optimal Foul Ranges for all Premier League Teams"
        else:
            title = f"Top {len(optimal_fouls)} Optimal Foul Ranges for {team}"
    io.table(
        title=title,
        headers=["Foul Range", "Number of Wins Recorded", "Win Percentage (%)"],
        colors=["cyan", "magenta", "green"],
        data=optimal_fouls,
        width=90,
    )


@app.command()
def predict(
    home: str = typer.Option(...),
    away: str = typer.Option(...),
    season: str = typer.Option(..., help="ex. 2009-10"),
) -> None:
    """Predict the outcome of a match in the 2019-20 season
    between the home and away team based on data from the 2018-19 season.

    Preconditions:
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
        - home team took part in the season
        - away team took part in the season
    """
    errors.validate_team(league, home)
    errors.validate_team(league, away)
    errors.validate_team_in_season(league, home, season)
    errors.validate_team_in_season(league, away, season)
    errors.validate_season(season)
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")
        prediction = round(predictions.predict(home, away, season, league), 2)

        prefix = "[yellow]Prediction: [/yellow]"
        if prediction < 0:
            display_str = (
                prefix
                + f"[cyan]{home}[/cyan] loses against [magenta]{away}[/magenta] with a {-prediction} goal difference."
            )
        else:
            display_str = (
                prefix
                + f"[cyan]{home}[/cyan] wins against [magenta]{away}[/magenta] with a {prediction} goal difference."
            )

    io.info(message=display_str, color="white")


def highestwinrates(
    season: str = typer.Option(default=None, help="ex. 2009-10"),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the topx teams with the highest win rate for the specified season.
    If season is not found, the statistic will be calculated across all seasons.

    Preconditions:
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
        - topx > 0
    """
    if season is not None:
        errors.validate_season(season)
    errors.validate_topx(topx)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")
        top_win_rates = records.highest_win_rate(league, season, topx)

        if season is None:
            title = "Highest Win Rates in the Premier League"
        else:
            title = f"Top {len(top_win_rates)} Highest Win Rates in the {season} Premier League Season"

    io.table(title=title, headers=["Team", "Winrate (%)"], colors=["cyan", "yellow"], data=top_win_rates, width=100)


def optimalyellowcards(
    team: str = typer.Option(default=None),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the optimal yellow cards for the provided team.

    Preconditions
        - team is a valid team
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
        - topx > 0
    """
    if team is not None:
        errors.validate_team(league, team)
    errors.validate_topx(topx)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")
        optimal_yellows = optimization.calculate_optimal_yellow_cards(league, team, topx)

        if team is None:
            title = f"Top {len(optimal_yellows)} Optimal Yellow Card Ranges for all Premier League Teams"
        else:
            title = f"Top {len(optimal_yellows)} Optimal Yellow Card Ranges for {team}"
    io.table(
        title=title,
        headers=["Yellow Card Range", "Number of Wins Recorded", "Win Percentage (%)"],
        colors=["cyan", "magenta", "green"],
        data=optimal_yellows,
        width=90,
    )


@app.command()
def optimalreferees(
    team: str = typer.Option(...),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the optimal referee for the provided team.

    Preconditions
        - team is a valid team
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
        - topx > 0
    """
    errors.validate_team(league, team)
    errors.validate_topx(topx)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")
        optimal_referees = optimization.calculate_optimal_referees(league, team, topx)

        title = f"Top {len(optimal_referees)} Optimal Referees for {team} in the Premier League"
    io.table(
        title=title,
        headers=["Referee Name", "Number of Wins Recorded", "Games Refereed", "Win Percentage (%)"],
        colors=["cyan", "magenta", "green", "yellow"],
        data=optimal_referees,
        width=90,
    )


@app.command()
def fairestreferees(
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the topx fairest referees for the whole league.

    Preconditions
        - team is a valid team
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
        - topx > 0
    """
    errors.validate_topx(topx)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")
        fairest_referees = optimization.calculate_fairest_referees(league, topx)

        title = f"Top {len(fairest_referees)} Fairest Referees for all Premier League Teams"
    io.table(
        title=title,
        headers=["Referee Name", "Number of Games Refereed", "Winrate Discrepancy"],
        colors=["cyan", "magenta", "yellow"],
        data=fairest_referees,
        width=90,
    )


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(
        config={
            "extra-imports": ["typer", "utils.constants"],
            "allowed-io": [],
            "max-line-length": 120,
        }
    )
