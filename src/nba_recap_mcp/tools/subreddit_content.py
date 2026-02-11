import json

import requests
from fastmcp import FastMCP

from nba_recap_mcp.utils.reddit import (
    COMMENT_URL,
    REDDIT_HEADER,
    extract_comments,
    find_game_thread,
)


def register_subreddit_content(mcp: FastMCP):
    @mcp.tool()
    def subreddit_content(
        home_team_nickname: str, away_team_nickname: str, subreddit: str
    ) -> str:
        """Fetches fan reactions from a SPECIFIC community perspective.

        IMPORTANT: Reddit game threads are echo chambers.
        - Querying the 'home' team subreddit only gives the home bias.
        - Querying the 'away' team subreddit only gives the away bias.
        - Querying 'nba' gives the neutral bias.

        To provide a comprehensive and objective recap, you should invoke this
        tool multiple times to aggregate differing perspectives.

        Args:
            home_team_nickname: Home team nickname (e.g., "Thunder")
            away_team_nickname: Away team nickname (e.g., "Warriors")
            subreddit: The specific community to query.

        Returns:
            JSON string with fans' comments and replies on success,
            or JSON string with error key on failure.
        """
        try:
            post_id = find_game_thread(
                home_team_nickname, away_team_nickname, subreddit
            )

            if not post_id:
                return json.dumps(
                    {
                        "error": f"No live game thread found for {home_team_nickname} in r/{subreddit}"
                    }
                )

            comments_resp = requests.get(
                COMMENT_URL.format(post_id=post_id),
                params={"sort": "new", "limit": 100, "depth": 3},
                headers=REDDIT_HEADER,
            )
            comments_resp.raise_for_status()

            data = comments_resp.json()
            comments = extract_comments(data[1]["data"]["children"])

            return json.dumps(comments)
        except Exception as e:
            return json.dumps({"error": f"Error fetching live comments: {str(e)}"})
