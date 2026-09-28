from outfitter.data import ENTRY_POINTS


def plan_portage_route(entry_point_code: str, trip_days: int) -> dict:
    """Suggest a simple loop route and pacing for a trip from a given entry point.

    Args:
        entry_point_code: The entry point code, e.g. "EP30" for Lake One.
        trip_days: Number of days for the trip.
    """
    info = ENTRY_POINTS.get(entry_point_code.upper())
    if info is None:
        return {
            "error": f"Unknown entry point code '{entry_point_code}'.",
            "known_entry_points": sorted(ENTRY_POINTS.keys()),
        }
    if trip_days < 1:
        return {"error": "trip_days must be at least 1."}

    portages_per_day = max(1, round(info["typical_portages"] / max(trip_days - 1, 1)))
    return {
        "entry_point_code": entry_point_code.upper(),
        "entry_point_name": info["name"],
        "trip_days": trip_days,
        "difficulty": info["difficulty"],
        "suggested_pace": f"~{portages_per_day} portage(s)/day, camp by early afternoon",
        "note": "Loop routes depend on permit availability; confirm with a current BWCA map.",
    }
