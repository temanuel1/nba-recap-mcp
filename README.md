# nba-recap-mcp

An MCP server that generates AI-powered NBA game recaps by combining live game data, play-by-play stats, and real-time fan reactions from Reddit.

## Setup

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

Add this to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "nba-recap": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/temanuel1/nba-recap-mcp", "nba-recap-mcp"]
    }
  }
}
```

Restart Claude Desktop. No cloning or local install needed.

## Usage

In Claude Desktop, just type:

```
recap Lakers
```

The server will fetch the live game data, box score, play-by-play, and fan comments from Reddit, then generate a narrative recap.

## Tools

| Tool | Description |
|------|-------------|
| `game_initializer` | Finds today's game for a given team |
| `box_score` | Fetches live box score stats |
| `play_by_play` | Fetches play-by-play action log |
| `subreddit_content` | Scrapes Reddit game thread comments for fan reactions |
