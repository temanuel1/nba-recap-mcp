import json
from datetime import datetime

from fastmcp import FastMCP
from nba_api.stats.endpoints import ScoreboardV2

from nba_recap_mcp.utils.nba import get_team_id, get_team_nickname
from nba_recap_mcp.resources.mappings import SUBREDDIT_MAPPING


def register_game_initializer(mcp: FastMCP):
    @mcp.tool()
    def game_initializer(team_name: str) -> str:
        """Initialize a game recap session. This is always the first step when a user asks for a game recap.

        After calling this tool, call box_score, play_by_play, and subreddit_content in parallel
        using the returned game_id and subreddit info. Then generate a recap that:
        - Follows chronological game flow (quarter by quarter)
        - Highlights key moments, runs, player performances, and turning points
        - Weaves in fan comments from Reddit to capture the emotional pulse of the game
        - Tells the story through both the action AND how fans are reacting to it

        Args:
            team_name: NBA team nickname (case-sensitive), e.g. Lakers, Warriors, Celtics

        Returns:
            JSON string with game_id, team nicknames, and subreddit names on success,
            or JSON string with error key on failure.
        """
        try:
            team_id = get_team_id(team_nickname=team_name)
            if team_id is None:
                return json.dumps({"error": f"Team '{team_name}' not found"})

            today = datetime.now().strftime("%Y-%m-%d")
            scoreboard = ScoreboardV2(day_offset=0, game_date=today, league_id="00")
            ongoing_games = scoreboard.game_header.get_data_frame()

            requested_game = ongoing_games[
                (ongoing_games["HOME_TEAM_ID"] == team_id)
                | (ongoing_games["VISITOR_TEAM_ID"] == team_id)
            ]

            if requested_game.empty:
                return json.dumps({"error": f"No live game found for {team_name}"})

            game = requested_game.iloc[0]

            home_team_nickname = get_team_nickname(game["HOME_TEAM_ID"])
            away_team_nickname = get_team_nickname(game["VISITOR_TEAM_ID"])

            return json.dumps(
                {
                    "game_id": game["GAME_ID"],
                    "home_team_nickname": home_team_nickname,
                    "away_team_nickname": away_team_nickname,
                    "home_team_subreddit": SUBREDDIT_MAPPING.get(home_team_nickname),
                    "away_team_subreddit": SUBREDDIT_MAPPING.get(away_team_nickname),
                }
            )

        except Exception as e:
            return json.dumps({"error": f"Error fetching NBA games: {str(e)}"})
