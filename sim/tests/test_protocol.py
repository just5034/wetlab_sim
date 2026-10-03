import json

import pytest
from labsim.protocol import handle_message, make_error
from labsim.world import World


def intent(action: str, args: dict | None = None) -> str:
    """Helper, not a test: build intent JSON text the way Unity will."""
    message = {"type": "intent", "action": action}
    if args is not None:
        message["args"] = args
    return json.dumps(message)


# Provided
def test_make_error_shape():
    assert make_error("boom") == {"type": "error", "message": "boom"}


# Provided
def test_tick_intent_returns_snapshot():
    world = World()
    reply = handle_message(world, intent("tick", {"steps": 2}))
    assert reply["t"] == 2
    assert reply == world.snapshot()


# Provided
def test_args_can_be_left_out():
    world = World()
    reply = handle_message(world, intent("tick"))
    assert reply["t"] == 1


# Provided
def test_invalid_json_is_an_error():
    world = World()
    assert handle_message(world, "{not json") == make_error("invalid JSON")


# Provided
@pytest.mark.parametrize(
    "text",
    [
        "[]",
        '"hello"',
        '{"type": "snapshot"}',
        '{"type": "intent"}',
        '{"type": "intent", "action": 5}',
    ],
)
def test_not_an_intent_is_an_error(text):
    world = World()
    assert handle_message(world, text) == make_error("expected an intent")


# Provided
def test_unknown_action_is_an_error_and_world_unchanged():
    world = World()
    reply = handle_message(world, intent("fly"))
    assert reply["type"] == "error"
    assert world.t == 0


def test_args_must_be_an_object():

    """Sending "args": [1, 2] gives make_error("args must be an object")."""

    world = World()
    assert handle_message(world, intent("tick", args=[1, 2])) == make_error("args must be an object")


def test_bad_argument_is_an_error_and_world_unchanged():

    """tick with steps 0 gives an error reply, and world.t stays 0."""

    world = World()
    reply = handle_message(world, intent("tick", args={"steps": 0}))

    assert reply == {'type': 'error', 'message': 'steps must be at least 1'}
    assert world.t == 0


