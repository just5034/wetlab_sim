"""This file defines the websocket server that Unity connects to. Unity will send its requests here and get snapshots from here.

Run it with:  python -m labsim.server
Stop it with: Ctrl+C
"""

import asyncio
import json
import logging

from websockets.asyncio.server import ServerConnection, serve
from websockets.exceptions import ConnectionClosedError

from labsim.actions import set_value
from labsim.protocol import handle_message
from labsim.world import World

HOST = "127.0.0.1"  # This machine only. Other computers cannot connect.
PORT = 8765

logger = logging.getLogger(__name__)


# This function gracefully handles a single client's connection until it either properly closes
# or suddenly disconnects.
async def handle_connection(connection: ServerConnection, world: World) -> None:
    """
    Serve one client until it disconnects.

    First send world.snapshot() as JSON, so the client can draw right away.
    Then, for every message received: log it at INFO level, pass it to
    handle_message, and send the reply back as JSON.
    Returns when the client disconnects. If the client vanishes without
    closing properly (Unity does this when you stop Play mode), log
    "client left without closing" at INFO level and return normally.
    """

    # I moved snapshot() into the try block to gracefully handle the rare chance that
    # immediately after a client connects to a server, the connection improperly terminates and we can't send the snapshot() data
    # because there is no longer a connection (can happen with faulty network).
    try:

        snap = world.snapshot()
        data_string = json.dumps(snap)
        await connection.send(data_string)

        async for message in connection:

            logger.info(" <- %s", message)
            reply = handle_message(world, message)
            reply_string = json.dumps(reply)
            await connection.send(reply_string)

    except ConnectionClosedError:

        logger.info("client left without closing")


# This function instantiates / builds a python websocket server object that will be used to communicate with the client(s).
def make_server(world: World, host: str = HOST, port: int = PORT) -> serve:
    """
    Return a server, not yet started, that serves `world` to every client.

    Start it with:  async with make_server(world) as server: ...
    Every connection shares the same `world`.
    Port 0 asks the operating system for any free port. The tests use that.
    """

    async def handler(connection: ServerConnection) -> None:

        await handle_connection(connection, world)

    return serve(handler, host, port)


# This function switches / turns on the server made by 'make_server()'
# The server is turned on indefinitely by parking the make_server(world) function in place
# using an await server.serv_forever method in an async with block.
async def serve_forever(world: World) -> None:
    """Start the server on HOST:PORT and keep it running until stopped."""

    async with make_server(world) as server:
        await server.serve_forever()


def main() -> None:
    """Turn on INFO logging, build World(seed=1) holding "a" at 0.0, and run
    serve_forever until Ctrl+C. On Ctrl+C, log "server stopped" and return
    without a traceback."""

    logging.basicConfig(level=logging.INFO)

    world = World(seed=1)
    set_value(world=world, name='a', value=0.0)

    try:

        asyncio.run(serve_forever(world))

    except KeyboardInterrupt:

        logger.info("server stopped")




if __name__ == "__main__":
    main()