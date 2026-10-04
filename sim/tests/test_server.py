import asyncio
import json

from labsim.server import make_server
from labsim.world import World
from websockets.asyncio.client import connect


def talk(world: World, messages: list[str]) -> list[dict]:
    """Helper, not a test: start a real server on a free port, connect as a
    client, send each message, and return every reply as a dict. The first
    reply is the snapshot the server sends on connect."""

    async def scenario() -> list[dict]:
        async with make_server(world, port=0) as server:
            port = server.sockets[0].getsockname()[1]
            async with connect(f"ws://127.0.0.1:{port}") as client:
                replies = [json.loads(await client.recv())]
                for message in messages:
                    await client.send(message)
                    replies.append(json.loads(await client.recv()))
        return replies

    return asyncio.run(scenario())



def test_sends_snapshot_on_connect():
    replies = talk(World(), [])
    assert replies == [{"type": "snapshot", "t": 0, "objects": {}}]



def test_intent_gets_snapshot_reply():
    tick = json.dumps({"type": "intent", "action": "tick", "args": {"steps": 1}})
    replies = talk(World(), [tick])
    assert replies[1]["type"] == "snapshot"
    assert replies[1]["t"] == 1



def test_bad_message_gets_error_and_connection_survives():
    tick = json.dumps({"type": "intent", "action": "tick"})
    replies = talk(World(), ["not json", tick])
    assert replies[1] == {"type": "error", "message": "invalid JSON"}
    assert replies[2]["t"] == 1