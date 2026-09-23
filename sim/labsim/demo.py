from labsim.actions import apply
from labsim.world import World


# Run a seeded world for 10 ticks and print each snapshot.


def main() -> None:

    """Build World(seed=1), add "a" at 0.0 then "b" at 10.0, then tick 10
    times, printing the snapshot after each tick."""

    # TODO: Implement using only World, set_value, tick, and print.

    example_world = World(seed = 1)

    apply(example_world, "set_value", {"name": "a", "value": 0.0})
    apply(example_world, "set_value", {"name": "b", "value": 10.0})

    for i in range(10):
        apply(example_world, "tick", {"steps": 1})
        snap = example_world.snapshot()
        print(snap)


if __name__ == "__main__":
    main()

