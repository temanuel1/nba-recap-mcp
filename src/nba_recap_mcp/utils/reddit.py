import requests

COMMENT_URL = "https://www.reddit.com/comments/{post_id}.json"
REDDIT_HEADER = {"User-Agent": "nba_recap_agent/0.1"}


def extract_comments(children: list) -> list[str]:
    """Recursively extract all comments including replies."""
    comments = []
    for c in children:
        if c["kind"] != "t1":
            continue
        body = c["data"].get("body")
        if body and "[removed]" not in body and "I am a bot" not in body:
            comments.append(body)
        replies = c["data"].get("replies")
        if replies and isinstance(replies, dict):
            comments.extend(extract_comments(replies["data"]["children"]))
    return comments


def find_game_thread(
    home_team_nickname: str, away_team_nickname: str, subreddit: str
) -> str | None:
    """Search for live game thread in the specified subreddit."""
    search_url = f"https://www.reddit.com/r/{subreddit}/search.json"
    search_params = {
        "q": f"game thread {home_team_nickname} {away_team_nickname}",
        "restrict_sr": "on",
        "sort": "new",
        "limit": 5,
    }

    try:
        resp = requests.get(search_url, params=search_params, headers=REDDIT_HEADER)
        resp.raise_for_status()

        for post in resp.json()["data"]["children"]:
            data = post["data"]
            title = data["title"]
            if (
                (title.startswith("GAME THREAD:") or title.startswith("Game Thread:"))
                and home_team_nickname in title
                and away_team_nickname in title
            ):
                return data["id"]
    except Exception:
        pass

    return None
