import hashlib


def check_water_levels(zone_name: str) -> dict:
    """Get a simulated water level reading for a lake/river zone.

    Args:
        zone_name: Name of the lake or river zone, e.g. "North Kawishiwi River".
    """
    seed = int(hashlib.sha256(zone_name.encode()).hexdigest(), 16)
    level_pct_of_normal = 70 + (seed % 50)
    trend = ["rising", "steady", "falling"][seed % 3]
    return {
        "zone_name": zone_name,
        "level_pct_of_normal": level_pct_of_normal,
        "trend": trend,
        "advisory": "low water, expect extra portaging" if level_pct_of_normal < 80 else "normal conditions",
    }
