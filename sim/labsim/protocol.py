import json

from labsim.actions import apply
from labsim.world import World

# This file creates the functions used to define the communication protocol between Unity and the python server.


def make_error(message: str) -> dict:

    """Return an error reply: {"type": "error", "message": message}."""

    return {"type": "error", "message": message}


def handle_message(world: World, text: str) -> dict:
    """Parse one intent from JSON text, apply it to `world`, return the reply.

    A valid intent is a JSON object such as
        {"type": "intent", "action": "tick", "args": {"steps": 1}}
    "args" may be left out, which means no arguments ({}).

    Returns:
        world.snapshot() if the intent was applied.
        make_error(...) otherwise, with these messages:
          - text is not valid JSON: "invalid JSON"
          - the JSON is not an object, "type" is not "intent", or "action"
            is not a string: "expected an intent"
          - "args" is present but is not an object: "args must be an object"
          - apply() raises TypeError or ValueError: str() of that exception

    Never raises. The server must survive any message a client sends.
    """

    try:
        json_text = json.loads(text)
    except json.JSONDecodeError:
        return make_error("invalid JSON")

    # Must be an object
    if not isinstance(json_text, dict):
        return make_error("expected an intent")

    # Must have type="intent"
    if json_text.get("type") != "intent":
        return make_error("expected an intent")

    # Must have an action string
    action = json_text.get("action")
    if not isinstance(action, str):
        return make_error("expected an intent")

    # args must be an object if present
    args = json_text.get("args", {})
    if not isinstance(args, dict):
        return make_error("args must be an object")

    # Apply the intent
    try:
        apply(world, action, args)
    except (TypeError, ValueError) as exc:
        return make_error(str(exc))

    return world.snapshot()