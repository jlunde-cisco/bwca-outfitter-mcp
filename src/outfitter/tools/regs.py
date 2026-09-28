from outfitter.data import FISHING_REGS


def get_fishing_regs(species: str) -> dict:
    """Look up Minnesota BWCA fishing limits for a species.

    Args:
        species: Fish species, e.g. "walleye", "northern_pike", "smallmouth_bass", "lake_trout".
    """
    key = species.lower().replace(" ", "_")
    regs = FISHING_REGS.get(key)
    if regs is None:
        return {
            "error": f"No regulation data for '{species}'.",
            "known_species": sorted(FISHING_REGS.keys()),
        }
    return {"species": key, **regs}
