import pytest
from labsim.actions import apply, set_value, tick
from labsim.world import World


# Test for the set_value() function
def test_set_value_creates_and_overwrites():
    world = World()
    set_value(world, "a", 1.0)
    set_value(world, "b", 1.0)
    set_value(world, "b", 2.5)
    assert world.objects == {
        "a": 1.0, 
        "b": 2.5,
        }

# Test for the tick() function
def test_tick_advances_clock():

    world = World()
    tick(world, 3)
    assert world.t == 3

    tick(world, 2)
    assert world.t == 5

# Tests the apply function runs properly
def test_apply_runs_tick():

    world = World()
    apply(world, "tick", {"steps": 2})
    
    assert world.t == 2


# Helper function to run five ticks with a given seed
def _run_five_ticks(seed):
    """Helper, not a test: same actions every time, only the seed varies."""
    world = World(seed=seed)
    set_value(world, "a", 0.0)
    set_value(world, "b", 10.0)
    tick(world, 5)
    return world.snapshot()


# Tests for matching world states after an equal number of ticks across the same seed
def test_same_seed_same_snapshots():
    assert _run_five_ticks(42) == _run_five_ticks(42)


# Test for the apply() function rejecting unknown actions
def test_apply_rejects_unknown_action():

    # Checks that the code in the 'with' block raises a ValueError when an unknown action is applied.
    with pytest.raises(ValueError):
        apply(World(), "fly", {})



def test_set_value_rejects_non_numbers():

    world = World()

    with pytest.raises(TypeError):
        apply(world, "set_value", {"name": "a", "value": "some random shit"})
    with pytest.raises(TypeError):
        apply(world, "set_value", {"name": "b", "value": True})


@pytest.mark.parametrize("bad_steps", [0, -1])
def test_tick_rejects_steps_below_one(bad_steps):
    
    world = World()

    with pytest.raises(ValueError):
        apply(world, "tick", {"steps": bad_steps})



def test_tick_rejects_non_whole_steps():

    world = World()

    with pytest.raises(TypeError):
        apply(world, "tick", {"steps": 2.5})


def test_different_seed_different_snapshots():

    world42 = World(42)
    world43 = World(43)

    apply(world42, "set_value", {"name": "a", "value": 4.0})
    apply(world43, "set_value", {"name": "a", "value": 4.0})
    apply(world42, "tick", {"steps": 1})
    apply(world43, "tick", {"steps": 1})

    snap42 = world42.snapshot()
    snap43 = world43.snapshot()

    assert snap42 != snap43

