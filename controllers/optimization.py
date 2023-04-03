"""Kickoff Project: controllers / records.py

This module contains functionality for finding various records in the datasets.

This file is Copyright (c) 2023 Ram Raghav Sharma, Harshith Latchupatula, Vikram Makkar and Muhammad Ibrahim.
"""

from models.league import League
from models.match import Match
from utils.league import get_all_matches
from controllers.basic import overall_winrate


def _compile_statistic_to_win_data(attr_name: str, matches: list[Match], team: str = None) -> dict[int, int]:
    """Returns a dictionary of specific statistic counts to the number of wins that they amass.

    Preconditions
        - team is a valid team
    """
    stat_wins = {}
    for match in matches:
        if match.result is not None and (match.result.name == team or team is None):
            if team is None:
                stat = getattr(match.details[match.result.name], attr_name)
            else:
                stat = getattr(match.details[team], attr_name)
            if stat not in stat_wins:
                stat_wins[stat] = 0
            stat_wins[stat] += 1

    return stat_wins


def _generate_optimal_range_data(
    matches: list[Match], stat_wins: dict[int, int], width: int
) -> list[tuple[str, int, float]]:
    """Returns an unsorted list of tuples of foul ranges, their corresponding number of wins
    and the % of total wins they account for.

    Preconditions:
        - 1 <= width < max(list(stat_wins.keys()))
    """
    max_stat = max(list(stat_wins.keys()))

    range_mappings = {}
    for i in range(0, max_stat + 1, width):
        range_str = str(i) + " - " + str(i + (width - 1))
        for j in range(width):
            range_mappings[i + j] = range_str

    stat_range_wins = {}
    for stat in stat_wins:
        range_mapping = range_mappings[stat]
        if range_mapping not in stat_range_wins:
            stat_range_wins[range_mapping] = 0
        stat_range_wins[range_mapping] += stat_wins[stat]

    optimal_ranges = [
        (
            stat_range,
            stat_range_wins[stat_range],
            round((stat_range_wins[stat_range] / len(matches)) * 100, 2),
        )
        for stat_range in stat_range_wins
    ]
    return optimal_ranges


def calculate_optimal_fouls(league: League, team: str = None, topx: int = 4) -> list[tuple[str, int, float]]:
    """Returns a list of the topx optimal foul ranges and the % of wins they account for.

    Preconditions
        - team is a valid team
        - 00 < topx
    """
    if team is None:
        matches = get_all_matches(league)
    else:
        matches = league.get_team(team).matches

    stat_wins = _compile_statistic_to_win_data(attr_name="fouls", matches=matches, team=team)
    optimal_ranges = _generate_optimal_range_data(matches, stat_wins, width=4)

    sorted_optimal_ranges = sorted(optimal_ranges, key=lambda a: a[1], reverse=True)
    return sorted_optimal_ranges[:topx]


def calculate_optimal_yellow_cards(league: League, team: str = None, topx: int = 4) -> list[tuple[str, int, float]]:
    """Returns a list of the topx optimal yellow card ranges and the % of wins they account for.

    Preconditions
        - team is a valid team
        - 0 < topx
    """
    if team is None:
        matches = get_all_matches(league)
    else:
        matches = league.get_team(team).matches

    stat_wins = _compile_statistic_to_win_data(attr_name="yellow_cards", matches=matches, team=team)
    optimal_ranges = _generate_optimal_range_data(matches, stat_wins, width=2)

    sorted_optimal_ranges = sorted(optimal_ranges, key=lambda a: a[1], reverse=True)
    return sorted_optimal_ranges[:topx]


def _generate_referee_win_stats(
    league: League, team: str, limit_games_refereed: bool = True
) -> list[tuple[str, int, int, float]]:
    """Returns an unsorted list of tuples of a referee, the number of wins they accounted for,
    the number of games referred and total win percentage.

    Preconditions
        - team is a valid team
    """
    matches = league.get_team(team).matches

    stat_wins = _compile_statistic_to_win_data(attr_name="referee", matches=matches, team=team)
    optimal_referees = []
    for referee in stat_wins:
        games_refereed = 0
        for match in matches:
            if match.details[match.away_team.name].referee == referee:
                games_refereed += 1
        if not limit_games_refereed or games_refereed >= 20:
            optimal_referees.append(
                (
                    referee,
                    stat_wins[referee],
                    games_refereed,
                    round((stat_wins[referee] / games_refereed) * 100, 2),
                )
            )

    return optimal_referees


def calculate_optimal_referees(league: League, team: str, topx: int = 4) -> list[tuple[str, int, int, float]]:
    """Returns a list of the topx optimal referees and their game win percentage.

    Preconditions
        - team is a valid team
        - 0 < topx
    """
    optimal_referees = _generate_referee_win_stats(league, team)
    sorted_optimal_ranges = sorted(optimal_referees, key=lambda a: a[3], reverse=True)
    return sorted_optimal_ranges[:topx]


def calculate_fairest_referees(league: League, topx: int = 4) -> list[tuple[str, int, int, float]]:
    """Returns a list of the topx fairest referees and their game win percentage.

    Preconditions
        - 0 < topx
    """
    team_names = league.get_team_names()

    referee_discrepancies = {}
    for team in team_names:
        team_winrate = overall_winrate(league, team)
        optimal_referees = _generate_referee_win_stats(league, team, limit_games_refereed=False)
        for optimal_referee in optimal_referees:
            if optimal_referee[0] not in referee_discrepancies:
                referee_discrepancies[optimal_referee[0]] = ([], [])
            referee_discrepancies[optimal_referee[0]][0].append(team_winrate - optimal_referee[3])
            referee_discrepancies[optimal_referee[0]][1].append(optimal_referee[2])

    fairest_referees = []
    for referee in referee_discrepancies:
        average_discrepancy = round(sum(referee_discrepancies[referee][0]) / len(referee_discrepancies[referee][0]), 2)
        games_refereed = sum(referee_discrepancies[referee][1])
        if average_discrepancy < 0:
            string_avg_discrepancy = str(average_discrepancy)
        else:
            string_avg_discrepancy = "+" + str(average_discrepancy)

        if games_refereed >= 20:
            fairest_referees.append((referee, games_refereed, string_avg_discrepancy))

    sorted_fairest_referees = sorted(fairest_referees, key=lambda a: abs(0 - float(a[2][1:])))
    return sorted_fairest_referees[:topx]


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(
        config={
            "extra-imports": ["models.league"],
            "allowed-io": [],
            "max-line-length": 120,
        }
    )
