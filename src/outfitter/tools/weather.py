import hashlib
from datetime import date


def check_weather_forecast(lake_zone: str, day: str | None = None) -> dict:
    """Get a simulated weather/wind forecast for a BWCA lake zone.

    Args:
        lake_zone: Name of the lake or entry zone, e.g. "Moose Lake".
        day: ISO date (YYYY-MM-DD) to forecast for. Defaults to today.
    """
    day = day or date.today().isoformat()
    # Deterministic pseudo-forecast so demos are repeatable, without calling
    # any external weather API.
    seed = int(hashlib.sha256(f"{lake_zone}|{day}".encode()).hexdigest(), 16)
    high_f = 58 + (seed % 25)
    low_f = high_f - 12 - (seed % 6)
    wind_mph = 3 + (seed % 15)
    conditions = ["clear", "partly cloudy", "overcast", "light rain", "chance of storms"][seed % 5]
    return {
        "lake_zone": lake_zone,
        "date": day,
        "high_f": high_f,
        "low_f": low_f,
        "wind_mph": wind_mph,
        "conditions": conditions,
    }
