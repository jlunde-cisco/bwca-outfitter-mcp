from outfitter.data import ENTRY_POINTS


def get_entry_point_info(entry_point_code: str) -> dict:
    """Look up permit quota, portage count, and difficulty for a BWCA entry point.

    Args:
        entry_point_code: The entry point code, e.g. "EP16" for Moose Lake.
    """
    info = ENTRY_POINTS.get(entry_point_code.upper())
    if info is None:
        return {
            "error": f"Unknown entry point code '{entry_point_code}'.",
            "known_entry_points": sorted(ENTRY_POINTS.keys()),
        }
    return {"entry_point_code": entry_point_code.upper(), **info}
