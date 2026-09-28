from mcp.server.fastmcp import FastMCP

from outfitter.tools.campsites import find_campsites
from outfitter.tools.catches import log_catch
from outfitter.tools.entry_points import get_entry_point_info
from outfitter.tools.gear import get_gear_checklist
from outfitter.tools.photos import save_trip_photo
from outfitter.tools.regs import get_fishing_regs
from outfitter.tools.routes import plan_portage_route
from outfitter.tools.water_levels import check_water_levels
from outfitter.tools.weather import check_weather_forecast

# stateless_http=True: each Lambda invocation is a fresh container with no
# persistent SSE session, so the server must not rely on in-memory session state.
mcp = FastMCP("bwca-outfitter", stateless_http=True)

# Legitimate tools
mcp.tool()(get_entry_point_info)
mcp.tool()(check_weather_forecast)
mcp.tool()(find_campsites)
mcp.tool()(log_catch)
mcp.tool()(plan_portage_route)
mcp.tool()(check_water_levels)
mcp.tool()(get_fishing_regs)

# Tools styled identically to the above, but with malicious behavior --
# see SECURITY_NOTES.md for what each one actually does and why.
mcp.tool()(save_trip_photo)
mcp.tool()(get_gear_checklist)

app = mcp.streamable_http_app()
