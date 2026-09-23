from labsim.world import World


# This tests the World class defaults.
def test_new_world_defaults():
    w = World()
    assert w.seed == 0
    assert w.t == 0
    assert w.objects == {}
    assert isinstance(w.rng, type(World().rng))


# This tests the snapshot method of the World class.
def test_snapshot_shape_single_object():
    w = World()
    w.objects["a"] = 1.5

    snap = w.snapshot()

    assert snap == {
        "type": "snapshot",
        "t": 0,
        "objects": {
            "a": {"value": 1.5}
        }
    }


# This tests that mutating the snapshot doesn't affect the actual world state.
# We guarantee this by creating a fresh dictionary for the snapshot each time we make one.
def test_snapshot_is_immutable_view():
    w = World()
    w.objects["a"] = 1.5

    snap = w.snapshot()
    snap["t"] = 999 #try mutating the snapshot

    # the world state must not change
    assert w.t == 0
    assert w.snapshot()["t"] == 0


# This tests that worlds with the same seed produce the same first random number, and differently seeded worlds produce different first random numbers.
def test_rng_same_seed_same_first_random():
    w1 = World(seed=123)
    w2 = World(seed=123)

    w3 = World(seed=999)

    r1 = w1.rng.random()
    r2 = w2.rng.random()
    r3 = w3.rng.random()

    assert r1 == r2
    assert r1 != r3