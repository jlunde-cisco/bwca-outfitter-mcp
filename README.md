# Boundary Waters Outfitter MCP

An MCP server for planning Boundary Waters Canoe Area (BWCA) canoe and
fishing trips -- entry points, weather, campsites, routes, catch logging,
and gear checklists.

It is also a **demo server for MCP/AI threat detection**: two of the nine
tools are styled identically to the legitimate ones but carry intentionally
malicious behavior (data exfiltration via tool parameters, and a silent
rug-pull behavior change). See [SECURITY_NOTES.md](SECURITY_NOTES.md) for
exactly which tools and what they do -- keep that file out of view during a
live "spot the malicious tool" demo.

All exfiltration in this demo goes to a `demo-attacker-sink` Lambda deployed
in the **same AWS stack and account**, so traffic is real and observable by
a security product watching the account, without any data leaving your own
infrastructure.

## Tools

Legitimate:
- `get_entry_point_info`
- `check_weather_forecast`
- `find_campsites`
- `log_catch`
- `plan_portage_route`
- `check_water_levels`
- `get_fishing_regs`

Malicious (see SECURITY_NOTES.md):
- `save_trip_photo`
- `get_gear_checklist`

## Local development

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn outfitter.server:app --app-dir src --reload --port 8000
```

The MCP streamable-HTTP endpoint is then at `http://localhost:8000/mcp`.
Point any MCP client (Claude Code, `mcp dev`, etc.) at that URL.

Locally, the rug-pull call counter falls back to a JSON file at
`/tmp/outfitter_local_state.json`, and the exfiltration tools are no-ops
unless `DEMO_ATTACKER_SINK_URL` is set.

## Deploying to AWS (SAM)

Requires the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
and AWS credentials configured.

```bash
sam build
sam deploy --guided
```

`sam deploy --guided` will prompt for a stack name and region, then print the
`McpServerUrl` and `AttackerSinkUrl` outputs. The outfitter Lambda's
`DEMO_ATTACKER_SINK_URL` environment variable is wired automatically to the
sink endpoint in the same stack -- no manual configuration needed.

To tear the demo down:

```bash
sam delete
```
