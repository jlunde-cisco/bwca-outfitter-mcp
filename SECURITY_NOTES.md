# Security notes (presenter reference -- don't show during the "spot it" demo)

This server intentionally ships two malicious tools alongside seven
legitimate ones, styled identically (same docstring format, same simple
param shapes, same naming conventions) so they don't stand out in a tool
listing. Both are implemented in `src/outfitter/tools/`.

## 1. `save_trip_photo` -- data exfiltration via tool params

File: `src/outfitter/tools/photos.py`

Declared purpose: save a trip photo log entry.

Actual behavior: accepts two undeclared-scope, catch-all parameters
(`photo_base64`, `device_metadata`) that it doesn't need for "logging a
photo caption," and forwards whatever is passed in them verbatim to
`demo-attacker-sink` via `sink_client.send_to_sink`. A caller (or a
manipulated LLM) that has been convinced to stuff unrelated data --
file contents, prior conversation text, credentials -- into those fields
will have it exfiltrated, while the tool's visible response to the caller
looks completely normal ("status": "saved").

Detection angle: broad/generic parameter schemas on a narrowly-named tool,
and outbound network calls from a tool whose description gives no reason to
make any.

## 2. `get_gear_checklist` -- rug-pull / silent behavior change

File: `src/outfitter/tools/gear.py`

Declared purpose: return a static BWCA gear checklist.

Actual behavior: behaves exactly as described for its first 3 calls (see
`_RUG_PULL_THRESHOLD` in the file), building trust. On the 4th and later
calls it starts (a) sending the caller's raw arguments to
`demo-attacker-sink`, and (b) appending a `note` field containing a
prompt-injection payload aimed at the calling LLM, asking it to chain into
`save_trip_photo` with a copy of the conversation as `device_metadata` --
i.e. using the rug-pull to bootstrap the exfiltration tool above.

The call counter is persisted in DynamoDB (`RugPullStateTable`) so the
threshold survives Lambda cold starts in the deployed demo.

Detection angle: identical tool name/description/schema across calls, but
output content and side effects change over time -- a static allow-list or
one-time tool review would miss this; it requires runtime/behavioral
monitoring.

## What's real vs. simulated

- The exfiltration destination is `demo-attacker-sink`, a second Lambda
  deployed in the *same* SAM stack/AWS account (`template.yaml`). Traffic is
  real HTTP traffic your defense product can observe, but nothing leaves
  your own account, and the sink does nothing but log the payload to
  CloudWatch.
- Neither tool reads real secrets, real files, or real user data on its
  own -- it only exfiltrates whatever the calling LLM/client chooses to put
  into the oversized parameters. That's the point: the attack surface is the
  gap between a tool's stated purpose and its actual parameter/behavior
  scope, not a filesystem exploit.
