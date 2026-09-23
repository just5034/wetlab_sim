import random
from dataclasses import dataclass, field

# This module defines the World class, which represents the state of a simulation world.
# It includes a random number generator seeded for reproducibility, a time counter, and a collection of objects with associated values.
# The World class provides a method to take a snapshot of its current state.

@dataclass
class World:
    seed: int = field(default = 0)
    t: int = field(default = 0)
    objects: dict[str, float] = field(default_factory=dict)
    rng: random.Random = field(init=False, repr=False)

    def __post_init__(self):
        self.rng = random.Random(self.seed)


    def snapshot(self) -> dict:

        return {
            "type": "snapshot",
            "t": self.t,
            "objects": {
                name: {"value": value} for name, value in self.objects.items()
            }
        }