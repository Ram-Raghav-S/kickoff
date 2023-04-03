"""Kickoff Project: commands.py

This module sets up various CLI commands that the user can use to interact with our application.
It simply parses user commands and ensures that inputs are acceptable and delegates the actual functionality
to other functions / classes.

This file is Copyright (c) 2023 Ram Raghav Sharma, Harshith Latchupatula, Vikram Makkar and Muhammad Ibrahim.
"""
from typing import Optional
from rich.progress import Progress, SpinnerColumn, TextColumn
import typer

import output as io
import validation as validate
from constants import Constants
from load import load_csv_files
import aggregation
import records
import optimization
import predictions

league = load_csv_files()
app = typer.Typer(help=Constants().retrieve("HELP_COMMAND_INTRO"))


@app.command()
def winrate(
    team: str = typer.Option(...), season: Optional[str] = typer.Option(default=None, help="ex. 2009-10")
) -> None:
    """Outputs the winrate percent of a given team or the whole league.
    If season is specified, the winrate will be calculated only for the given season.

    Preconditions
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
        - league.team_in_league(team)
        - season is None or team in league.get_team_names(season)
    """
    validate.validate_team(league, team)
    if season is not None:
        validate.validate_season(season)
        validate.validate_team_in_season(league, team, season)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")

        winrate_percent = round(aggregation.overall_winrate(league, team, season), 2)

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
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
        - team in league.get_team_names(season)
    """
    validate.validate_team(league, team)
    validate.validate_season(season)
    validate.validate_team_in_season(league, team, season)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")

        updated_data = []
        average_data = [
            [
                "Average Goals Scored / Game",
                round(aggregation.get_team_goals_scored(league, team, season), 2),
                round(aggregation.get_season_goals_scored(league, season), 2),
            ],
            [
                "Average Shot Accuracy (%)",
                round(aggregation.get_team_shot_accuracy(league, team, season), 2),
                round(aggregation.get_season_shot_accuracy(league, season), 2),
            ],
            [
                "Average Fouls Committed / Game",
                round(aggregation.get_team_fouls(league, team, season), 2),
                round(aggregation.get_season_fouls(league, season), 2),
            ],
            [
                "Average Card Offenses / Game",
                round(aggregation.get_team_cards(league, team, season), 2),
                round(aggregation.get_season_cards(league, season), 2),
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
    team: str = typer.Option(...),
    season: str = typer.Option(default=None, help="ex. 2009-10"),
) -> None:
    """Outputs the home vs away winrates for a team / season or for the whole league.
    If team is specified, winrates will be calculated only for the given team.
    If season is specified, winrates will be calculated only for the given season.

    Preconditions:
        - season is in the format '20XX-XX' between 2009-10 and 2018-19 or season is None
        - team is None or league.team_in_league(team)
        - (season is None or team is None) or team in league.get_team_names(season)
    """
    if season is not None:
        validate.validate_season(season)
    if team is not None:
        validate.validate_team(league, team)
    if team is not None and season is not None:
        validate.validate_team_in_season(league, team, season)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")

        home_vs_away = aggregation.home_vs_away(league, team, season)
        if season is not None:
            title = f"Home vs Away Winrates for {team} in the {season} Premier League Season"
        else:
            title = f"Home vs Away Winrates for {team} in the Premier League"

    io.table(
        title=title,
        headers=["Home Win Rate (%)", "Away Win Rate (%)", "Total Draw Rate (%)"],
        colors=["cyan", "magenta", "cyan"],
        data=home_vs_away,
        width=70,
    )


@app.command()
def highestwinrates(
    season: str = typer.Option(default=None, help="ex. 2009-10"),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the topx teams with the highest win rate in the league.
    If season is specified, winrates will be calculated only for the given season.

    Preconditions:
        - season is in the format '20XX-XX' between 2009-10 and 2018-19 or season is None
        - topx > 0
    """
    if season is not None:
        validate.validate_season(season)
    validate.validate_topx(topx)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")
        top_win_rates = records.highest_win_rate(league, season, topx)

        if season is None:
            title = "Highest Win Rates in the Premier League"
        else:
            title = f"Top {len(top_win_rates)} Highest Win Rates in the {season} Premier League Season"

    io.table(title=title, headers=["Team", "Winrate (%)"], colors=["cyan", "yellow"], data=top_win_rates, width=100)


@app.command()
def higheststreaks(
    season: str = typer.Option(..., help="ex. 2009-10"),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the topx longest win streaks for the specified season.

    Preconditions:
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
    """
    validate.validate_season(season)
    validate.validate_topx(topx)

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
def bestcomebacks(
    season: str = typer.Option(default=None, help="ex. 2009-10"),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the topx comebacks in the league.
    If season is specified, comebacks will be calculated only for the given season.

    Preconditions
        - season is in the format '20XX-XX' between 2009-10 and 2018-19 or season is None
        - topx > 0
    """
    if season is not None:
        validate.validate_season(season)
    validate.validate_topx(topx)

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
def mostgoals(
    season: str = typer.Option(default=None, help="ex. 2009-10"),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the topx highest goals scored in a game.
    If season is specified, the highest goals will be calculated only for the given season.

    Preconditions
        - season is in the format '20XX-XX' between 2009-10 and 2018-19 or season is None
        - topx > 0
    """
    if season is not None:
        validate.validate_season(season)
    validate.validate_topx(topx)

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
def topfairplay(
    season: str = typer.Option(default=None, help="ex. 2009-10"),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the topx most fairplaying teams in the league.
    If season is specified, fairplay will be calculated only for the given season.

    Preconditions
        - season is in the format '20XX-XX' between 2009-10 and 2018-19 or season is None
        - topx > 0
    """
    if season is not None:
        validate.validate_season(season)
    validate.validate_topx(topx)

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
def mostimproved(
    season: str = typer.Option(..., help="ex. 2009-10"),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Output the topx most improved teams in the given season.

    Preconditions
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
        - 0 < topx <= 20
    """
    validate.validate_season(season)
    validate.validate_topx(topx, 20)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Compiling results...")

        most_improved = records.most_improved_teams(league, season, topx)
        title = f"Top {len(most_improved)} Most Improved Teams in the {season} Premier League Season"

    io.table(
        title=title,
        headers=["Team", "Lowest Winrate (%)", "Final Winrate (%)", "Winrate Improvement (%)"],
        colors=["cyan", "magenta", "cyan", "magenta"],
        data=most_improved,
        width=80,
    )


@app.command()
def optimalfouls(
    team: str = typer.Option(default=None),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the optimal fouls to win a game.
    If team is specified, optimal fouls will be calculated only for the given team.
    If season is specified, optimal fouls will be calculated only for the given season.

    Preconditions
        - team is None or league.team_in_league(team)
        - topx > 0
    """
    if team is not None:
        validate.validate_team(league, team)
    validate.validate_topx(topx)

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
def optimalyellowcards(
    team: str = typer.Option(default=None),
    topx: int = typer.Option(default=4, help="Enter the top x values to output"),
) -> None:
    """Outputs the optimal yellow cards for the league.
    If team is specified, optimal yellow cards will be calculated only for the given team.

    Preconditions
        - team is None or league.team_in_league(team)
        - topx > 0
    """
    if team is not None:
        validate.validate_team(league, team)
    validate.validate_topx(topx)

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
    """Outputs the optimal referee for the provided team based on referee winrate.

    Preconditions
        - league.team_in_league(team)
        - topx > 0
    """
    validate.validate_team(league, team)
    validate.validate_topx(topx)

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
        - topx > 0
    """
    validate.validate_topx(topx)

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


@app.command()
def predict(
    home: str = typer.Option(...),
    away: str = typer.Option(...),
    season: str = typer.Option(..., help="ex. 2009-10"),
) -> None:
    """Predict the outcome of a match in the 2019-20 season
    between the home and away team based on data from the given season.

    Preconditions:
        - season is in the format '20XX-XX' between 2009-10 and 2018-19
        - home in league.get_team_names(season)
        - away in league.get_team_names(season)
    """
    if home == away:
        io.error("Home and away teams cannot be the same.")
    validate.validate_team(league, home)
    validate.validate_team(league, away)
    validate.validate_season(season)
    validate.validate_team_in_season(league, home, season)
    validate.validate_team_in_season(league, away, season)

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
