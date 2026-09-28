import uuid
from datetime import datetime, timezone


def log_catch(species: str, length_in: float, lake_name: str, notes: str = "") -> dict:
    """Record a fish catch for a trip log.

    Args:
        species: Fish species, e.g. "walleye".
        length_in: Length of the fish in inches.
        lake_name: Lake where the fish was caught.
        notes: Optional free-text notes (e.g. bait used, released or kept).
    """
    record = {
        "catch_id": str(uuid.uuid4()),
        "species": species,
        "length_in": length_in,
        "lake_name": lake_name,
        "notes": notes,
        "logged_at": datetime.now(timezone.utc).isoformat(),
    }
    return {"status": "logged", "catch": record}
