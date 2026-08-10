# nba-recap-mcp

An MCP server that generates AI-powered NBA game recaps by combining live game data, play-by-play stats, and real-time fan reactions from Reddit.

## Requirements

- [Claude Desktop](https://claude.ai/download)
- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Internet access (no API keys required)

## Setup

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

## Limitations

- Works during and around live NBA games — the team must appear on today's NBA scoreboard
- Requires a live game thread to exist in the team's subreddit (usually posted ~1 hour before tipoff)
- Reddit calls are unauthenticated and subject to public rate limits

## Troubleshooting

- **"No game found for X today"** — the team isn't playing today, or the nickname is misspelled
- **Server doesn't appear in Claude Desktop** — fully quit and restart the app; verify the JSON in `claude_desktop_config.json` is valid
- **Reddit returns empty comments** — the game thread hasn't been posted yet, or you're being rate-limited (wait a minute and retry)

## License

[MIT](./LICENSE)
