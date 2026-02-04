import json

from fastmcp import FastMCP
from nba_api.live.nba.endpoints import BoxScore


def register_box_score(mcp: FastMCP):
    @mcp.tool()
    def box_score(game_id: str) -> str:
        """Get live box score data for NBA game specified by game_id (from nba.com).

        Args:
            game_id: nba.com game ID (e.g. 0022500670)

        Returns:
            JSON string with box score data on success,
            or JSON string with error key on failure.
        """
        try:
            bs = BoxScore(game_id=game_id)
            data = bs.get_dict()

            return json.dumps(data)
        except Exception as e:
            return json.dumps({"error": f"Error fetching box score data: {str(e)}"})
