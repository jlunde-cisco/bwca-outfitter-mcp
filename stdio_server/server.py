"""Local Mac helper MCP server, speaking MCP over STDIO.

Independent of the `outfitter` package and the AWS deployment. Claude launches
this as a subprocess and talks JSON-RPC over stdin/stdout, so NOTHING may be
printed to stdout -- use stderr (or logging) for diagnostics.
"""
import json
import os
import platform
import shutil
import sys
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("local-mac-helper")

NOTES_FILE = Path.home() / ".local-mac-helper-notes.json"
# File browsing is confined to this directory; override with MAC_HELPER_ROOT.
ROOT = Path(os.environ.get("MAC_HELPER_ROOT", Path.home() / "Documents")).expanduser().resolve()


def _load_notes() -> list[dict]:
    if not NOTES_FILE.exists():
        return []
    return json.loads(NOTES_FILE.read_text())


@mcp.tool()
def get_system_info() -> dict:
    """Return basic information about this Mac: OS, CPU architecture, Python version, disk space, and current time."""
    disk = shutil.disk_usage("/")
    return {
        "hostname": platform.node(),
        "os": f"{platform.system()} {platform.mac_ver()[0] or platform.release()}",
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "disk_total_gb": round(disk.total / 1e9, 1),
        "disk_free_gb": round(disk.free / 1e9, 1),
        "local_time": datetime.now().astimezone().isoformat(timespec="seconds"),
    }


@mcp.tool()
def list_files(subpath: str = "") -> list[dict]:
    """List files and folders under the helper's root directory (default ~/Documents).

    Args:
        subpath: Path relative to the root directory. Empty string lists the root itself.
    """
    target = (ROOT / subpath).resolve()
    if target != ROOT and ROOT not in target.parents:
        raise ValueError(f"Path escapes the allowed root {ROOT}")
    if not target.is_dir():
        raise ValueError(f"Not a directory: {subpath or '.'}")
    entries = []
    for p in sorted(target.iterdir()):
        if p.name.startswith("."):
            continue
        entries.append(
            {
                "name": p.name,
                "type": "dir" if p.is_dir() else "file",
                "size_bytes": p.stat().st_size if p.is_file() else None,
            }
        )
    return entries


@mcp.tool()
def add_note(text: str) -> str:
    """Save a short note to the local notes file.

    Args:
        text: The note content.
    """
    notes = _load_notes()
    notes.append({"id": len(notes) + 1, "created": datetime.now().isoformat(timespec="seconds"), "text": text})
    NOTES_FILE.write_text(json.dumps(notes, indent=2))
    return f"Saved note #{len(notes)}"


@mcp.tool()
def list_notes() -> list[dict]:
    """Return all saved notes."""
    return _load_notes()


if __name__ == "__main__":
    print(f"local-mac-helper starting on stdio (root={ROOT})", file=sys.stderr)
    mcp.run(transport="stdio")
