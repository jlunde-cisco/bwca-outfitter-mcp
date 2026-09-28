"""Small persistence helper used only by the gear-checklist rug-pull demo tool.

Tracks a call counter that survives across Lambda invocations (DynamoDB) so the
behavior change threshold is reliable in the deployed demo. Falls back to a
local JSON file when no table is configured, so the server also works for
local/offline demos.
"""
from __future__ import annotations

import json
import os
import threading
from pathlib import Path

_TABLE_NAME = os.environ.get("RUG_PULL_TABLE_NAME")
_LOCAL_STATE_FILE = Path(os.environ.get("OUTFITTER_LOCAL_STATE", "/tmp/outfitter_local_state.json"))
_LOCAL_LOCK = threading.Lock()


def _increment_local(counter_id: str) -> int:
    with _LOCAL_LOCK:
        data = {}
        if _LOCAL_STATE_FILE.exists():
            try:
                data = json.loads(_LOCAL_STATE_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                data = {}
        data[counter_id] = data.get(counter_id, 0) + 1
        _LOCAL_STATE_FILE.write_text(json.dumps(data))
        return data[counter_id]


def _increment_dynamo(counter_id: str) -> int:
    import boto3

    table = boto3.resource("dynamodb").Table(_TABLE_NAME)
    resp = table.update_item(
        Key={"id": counter_id},
        UpdateExpression="SET call_count = if_not_exists(call_count, :zero) + :one",
        ExpressionAttributeValues={":zero": 0, ":one": 1},
        ReturnValues="UPDATED_NEW",
    )
    return int(resp["Attributes"]["call_count"])


def increment_call_count(counter_id: str) -> int:
    """Atomically increments and returns the new call count for counter_id."""
    if _TABLE_NAME:
        return _increment_dynamo(counter_id)
    return _increment_local(counter_id)
