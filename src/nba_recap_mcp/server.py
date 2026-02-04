from fastmcp import FastMCP

mcp = FastMCP("nba-recap")

from nba_recap_mcp.tools.game_initializer import register_game_initializer
from nba_recap_mcp.tools.box_score import register_box_score
from nba_recap_mcp.tools.play_by_play import register_play_by_play
from nba_recap_mcp.tools.subreddit_content import register_subreddit_content

register_game_initializer(mcp)
register_box_score(mcp)
register_play_by_play(mcp)
register_subreddit_content(mcp)

if __name__ == "__main__":
    mcp.run()
