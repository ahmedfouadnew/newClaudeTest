import httpx
import os

TBA_BASE = "https://www.thebluealliance.com/api/v3"


def _headers():
    return {"X-TBA-Auth-Key": os.getenv("TBA_API_KEY", "")}


def get_team_info(team_number: int) -> dict:
    """Basic info about an FRC team."""
    with httpx.Client() as client:
        r = client.get(f"{TBA_BASE}/team/frc{team_number}", headers=_headers())
        if r.status_code != 200:
            return {"error": f"Team {team_number} not found"}
        d = r.json()
        return {
            "team_number": d.get("team_number"),
            "nickname": d.get("nickname"),
            "name": d.get("name"),
            "city": d.get("city"),
            "state_prov": d.get("state_prov"),
            "country": d.get("country"),
            "rookie_year": d.get("rookie_year"),
            "website": d.get("website"),
        }


def get_team_events(team_number: int, year: int) -> list:
    """Events an FRC team attended in a given year."""
    with httpx.Client() as client:
        r = client.get(f"{TBA_BASE}/team/frc{team_number}/events/{year}/simple", headers=_headers())
        if r.status_code != 200:
            return [{"error": f"No events found for team {team_number} in {year}"}]
        events = r.json()
        return [
            {
                "key": e.get("key"),
                "name": e.get("name"),
                "event_type_string": e.get("event_type_string"),
                "city": e.get("city"),
                "state_prov": e.get("state_prov"),
                "start_date": e.get("start_date"),
                "end_date": e.get("end_date"),
                "week": e.get("week"),
            }
            for e in events
        ]


def get_team_event_status(team_number: int, event_key: str) -> dict:
    """A team's status/ranking at a specific event."""
    with httpx.Client() as client:
        r = client.get(f"{TBA_BASE}/team/frc{team_number}/event/{event_key}/status", headers=_headers())
        if r.status_code != 200:
            return {"error": f"Status not found for team {team_number} at {event_key}"}
        d = r.json()
        if not d:
            return {"error": "No status data available"}
        result = {}
        if d.get("qual"):
            result["qual_ranking"] = d["qual"].get("ranking", {}).get("rank")
            result["qual_num_teams"] = d["qual"].get("num_teams")
            result["record"] = d["qual"].get("ranking", {}).get("record")
        if d.get("alliance"):
            result["alliance"] = d["alliance"].get("name")
            result["alliance_pick"] = d["alliance"].get("pick")
        if d.get("playoff"):
            result["playoff_status"] = d["playoff"].get("status")
            result["playoff_level"] = d["playoff"].get("level")
        result["overall_status"] = d.get("overall_status_str", "")
        return result


def get_event_rankings(event_key: str) -> list:
    """Full rankings at an event."""
    with httpx.Client() as client:
        r = client.get(f"{TBA_BASE}/event/{event_key}/rankings", headers=_headers())
        if r.status_code != 200:
            return [{"error": f"Rankings not found for event {event_key}"}]
        d = r.json()
        if not d or not d.get("rankings"):
            return [{"error": "No rankings data available"}]
        return [
            {
                "rank": row.get("rank"),
                "team_number": int(row["team_key"].replace("frc", "")),
                "record": row.get("record"),
                "ranking_points": row.get("extra_stats", [None])[0],
            }
            for row in d["rankings"][:20]  # top 20
        ]


def get_event_teams(event_key: str) -> list:
    """Teams attending an event."""
    with httpx.Client() as client:
        r = client.get(f"{TBA_BASE}/event/{event_key}/teams/simple", headers=_headers())
        if r.status_code != 200:
            return [{"error": f"Teams not found for event {event_key}"}]
        teams = r.json()
        return sorted(
            [{"team_number": t["team_number"], "nickname": t["nickname"]} for t in teams],
            key=lambda x: x["team_number"],
        )


def get_team_awards(team_number: int, year: int) -> list:
    """Awards a team won in a given year."""
    with httpx.Client() as client:
        r = client.get(f"{TBA_BASE}/team/frc{team_number}/awards/{year}", headers=_headers())
        if r.status_code != 200:
            return [{"error": f"Awards not found for team {team_number} in {year}"}]
        awards = r.json()
        return [{"award": a.get("name"), "event": a.get("event_key")} for a in awards]


def get_team_season_summary(team_number: int, year: int) -> dict:
    """Full summary of a team's performance in a specific season: events attended, ranking/record at each, and awards."""
    summary = {"team_number": team_number, "year": year, "events": [], "awards": []}

    with httpx.Client() as client:
        # Basic info
        r = client.get(f"{TBA_BASE}/team/frc{team_number}", headers=_headers())
        if r.status_code == 200:
            d = r.json()
            summary["nickname"] = d.get("nickname")
            summary["location"] = f"{d.get('city')}, {d.get('state_prov')}, {d.get('country')}"
            summary["rookie_year"] = d.get("rookie_year")

        # Events this season
        r = client.get(f"{TBA_BASE}/team/frc{team_number}/events/{year}/simple", headers=_headers())
        events = r.json() if r.status_code == 200 else []

        for e in events:
            event_key = e.get("key")
            event_entry = {
                "key": event_key,
                "name": e.get("name"),
                "type": e.get("event_type_string"),
                "location": f"{e.get('city')}, {e.get('state_prov')}",
                "week": e.get("week"),
                "start_date": e.get("start_date"),
            }

            # Status/ranking at this event
            r2 = client.get(f"{TBA_BASE}/team/frc{team_number}/event/{event_key}/status", headers=_headers())
            if r2.status_code == 200 and r2.json():
                s = r2.json()
                if s.get("qual") and s["qual"].get("ranking"):
                    event_entry["qual_rank"] = s["qual"]["ranking"].get("rank")
                    event_entry["qual_num_teams"] = s["qual"].get("num_teams")
                    event_entry["record"] = s["qual"]["ranking"].get("record")
                if s.get("alliance"):
                    event_entry["alliance"] = s["alliance"].get("name")
                    event_entry["alliance_pick"] = s["alliance"].get("pick")
                if s.get("playoff"):
                    event_entry["playoff_status"] = s["playoff"].get("status")
                    event_entry["playoff_level"] = s["playoff"].get("level")
                event_entry["overall_status"] = s.get("overall_status_str", "")

            summary["events"].append(event_entry)

        # Awards this season
        r = client.get(f"{TBA_BASE}/team/frc{team_number}/awards/{year}", headers=_headers())
        if r.status_code == 200:
            summary["awards"] = [{"award": a.get("name"), "event": a.get("event_key")} for a in r.json()]

    if not summary["events"]:
        summary["note"] = f"No events found for team {team_number} in {year}. They may not have competed yet or data isn't available."

    return summary


# Map tool names to functions
TOOL_HANDLERS = {
    "get_team_info": lambda args: get_team_info(args["team_number"]),
    "get_team_events": lambda args: get_team_events(args["team_number"], args["year"]),
    "get_team_event_status": lambda args: get_team_event_status(args["team_number"], args["event_key"]),
    "get_event_rankings": lambda args: get_event_rankings(args["event_key"]),
    "get_event_teams": lambda args: get_event_teams(args["event_key"]),
    "get_team_awards": lambda args: get_team_awards(args["team_number"], args["year"]),
    "get_team_season_summary": lambda args: get_team_season_summary(args["team_number"], args["year"]),
}
