from outfitter.data import CAMPSITES


def find_campsites(lake_name: str) -> dict:
    """List known designated campsites on a given BWCA lake.

    Args:
        lake_name: Name of the lake, e.g. "Basswood Lake".
    """
    sites = CAMPSITES.get(lake_name)
    if sites is None:
        return {
            "error": f"No campsite data for '{lake_name}'.",
            "known_lakes": sorted(CAMPSITES.keys()),
        }
    return {"lake_name": lake_name, "campsites": sites}
