from nba_api.stats.static import teams


def get_team_id(team_nickname: str) -> int | None:
    """Convert team nickname string to team_id from nba.com."""
    all_teams = teams.get_teams()
    for team in all_teams:
        if team_nickname == team["nickname"]:
            return team["id"]
    return None


def get_team_nickname(team_id: int) -> str:
    """Convert team_id to team nickname from nba.com."""
    all_teams = teams.get_teams()
    team = next((team for team in all_teams if team["id"] == team_id), None)
    if team is None:
        raise ValueError(f"Unknown NBA team_id: {team_id}")
    return team["nickname"]
