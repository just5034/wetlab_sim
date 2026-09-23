from labsim.world import World


def set_value(world: World, name: str, value: float) -> None:

    """
    Create object `name` holding `value`, or overwrite it if it exists.

    The value is stored as a float, so 3 is stored as 3.0.

    Raises:
        TypeError: if value is not an int or a float. Booleans are rejected
            too, even though Python treats True as the int 1.
    """


    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError("value must be an int or float, not bool")

    world.objects[name] = float(value)





def tick(world: World, steps: int = 1) -> None:

    """
    Advance the world by `steps` ticks.

    Each tick: add 1 to world.t, then add a random float between -1.0 and 1.0
    to every object's value. This "random walk" is a placeholder rule until
    the team picks a domain. Visit objects in sorted name order so a given
    seed always hands the same object the same random draw.

    Raises:
        TypeError: if steps is not an int. Booleans are rejected too.
        ValueError: if steps is less than 1.
    """



    if not isinstance(steps, int) or isinstance(steps, bool):
        raise TypeError("steps must be an int")
    if steps < 1:
        raise ValueError("steps must be at least 1")

    for n in range(steps):

        world.t += 1
        for name in sorted(world.objects):
            world.objects[name] += world.rng.uniform(-1.0, 1.0)


# ACTIONS maps action names to their corresponding functions.
# Unity can only use the actions listed in this dictionary.
ACTIONS = {
    "set_value": set_value,
    "tick": tick,
}


def apply(world: World, action: str, args: dict) -> None:

    """
    Run the action called `action`, passing `args` as keyword arguments.

    Example: apply(world, "tick", {"steps": 2}) runs tick(world, steps=2).
    The M2 server calls this for every intent Unity sends.

    Raises:
        ValueError: if `action` is not a key in ACTIONS.
    """
    # Reject unknown names, then look up the function and call it.
    # Hint: `**some_dict` unpacks a dict into keyword arguments.

    if action not in ACTIONS:
        raise ValueError(f"Unknown action: {action}")

    ACTIONS[action](world, **args)

