import json

from fastmcp import FastMCP
from nba_api.live.nba.endpoints import PlayByPlay


def register_play_by_play(mcp: FastMCP):
    @mcp.tool()
    def play_by_play(game_id: str) -> str:
        """Get live play-by-play data for NBA game specified by game_id.

        Args:
            game_id: nba.com game ID (e.g. 0022500670)

        Returns:
            JSON array of raw action objects from the NBA live API.
            Returns JSON with error key on failure.
        """
        try:
            pbp = PlayByPlay(game_id=game_id)
            data = pbp.get_dict()
            actions = data.get("game", {}).get("actions", [])

            return json.dumps(actions)

        except Exception as e:
            return json.dumps(
                {"error": f"Error fetching play-by-play data: {str(e)}"}
            )
