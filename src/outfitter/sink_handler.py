"""demo-attacker-sink: the "attacker-controlled" collector for this demo.

Deployed as its own Lambda in the same AWS account/stack as the outfitter
server. It exists so a security product watching this demo has real,
observable outbound traffic to detect from the malicious tools in
outfitter/tools/photos.py and outfitter/tools/gear.py. It does nothing with
the data beyond logging it to CloudWatch -- there is no external forwarding,
storage, or use of the received payload.
"""
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        body = {"raw_body": event.get("body")}

    logger.warning("DEMO_ATTACKER_SINK_RECEIVED: %s", json.dumps(body))

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"status": "received"}),
    }
