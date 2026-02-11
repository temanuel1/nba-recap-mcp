import json
from datetime import datetime

from fastmcp import FastMCP
from nba_api.stats.endpoints import ScoreboardV2

from nba_recap_mcp.utils.nba import get_team_id, get_team_nickname
from nba_recap_mcp.resources.mappings import SUBREDDIT_MAPPING


def register_game_initializer(mcp: FastMCP):
    @mcp.tool()
    def game_initializer(team_name: str) -> str:
        """Initialize game info and identify available diverse data sources.

        Args:
            team_name: NBA team nickname (case-sensitive), e.g. Lakers, Warriors, Celtics

        Returns:
            JSON string containing game metadata and a 'perspectives_available' menu.

            The 'perspectives_available' object outlines the different subreddit
            communities (home bias, away bias, neutral) that should be queried
            to form a complete picture.

            example response:
            {
                "game_info": {
                    "game_id": "0022500670",
                    "matchup": "Spurs vs Hornets"
                },
                "perspectives_available": {
                    "home_bias": { "team": "Spurs", "subreddit": "NBASpurs" },
                    "away_bias": { "team": "Hornets", "subreddit": "CharlotteHornets" },
                    "neutral": { "subreddit": "nba" }
                }
            }
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

            # Return a "Menu" of perspectives rather than a flat list
            return json.dumps(
                {
                    "game_info": {
                        "game_id": game["GAME_ID"],
                        "matchup": f"{home_team_nickname} vs {away_team_nickname}",
                    },
                    # This structure hints to the LLM that there are 3 distinct buckets of info
                    "perspectives_available": {
                        "home_bias": {
                            "team": home_team_nickname,
                            "subreddit": SUBREDDIT_MAPPING.get(home_team_nickname),
                        },
                        "away_bias": {
                            "team": away_team_nickname,
                            "subreddit": SUBREDDIT_MAPPING.get(away_team_nickname),
                        },
                        "neutral": {"subreddit": "nba"},
                    },
                }
            )

        except Exception as e:
            return json.dumps({"error": f"Error fetching NBA games: {str(e)}"})
