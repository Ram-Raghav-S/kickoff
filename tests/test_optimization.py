"""Test suite for optimization functions"""


from models.match import Match
from models.team import Team
from models.league import League
from utils.data import load_csv_files
from controllers.optimization import _find_all_paths


league = load_csv_files()

liverpool = league.get_team("liverpool")
chelsea = league.get_team("Chelsea")

assert len(_find_all_paths(liverpool, chelsea, 2009-10, 2)) == 1

