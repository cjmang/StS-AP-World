from typing import List, Optional

from typing_extensions import NamedTuple, Iterable

from BaseClasses import CollectionState
from worlds.spire.test import SpireTestBase

class PowerLevel(NamedTuple):
    draw: int = 0
    relic: int = 0
    boss_relic: int = 0

def _create_floor_check(start: int, end: int) -> List[str]:
    return [f"Reached Floor {i}" for i in range(start, end + 1)]

logic_map: dict[PowerLevel, List[str]] = {
    PowerLevel(): [
        "Card Draw 1",
        "Card Draw 2",
        "Card Draw 3",
        *_create_floor_check(1,10)
    ],
    PowerLevel(1): [
        "Relic 1",
    ],
    PowerLevel(0,1): [
        "Card Draw 4",
        "Card Draw 5",
    ],
    PowerLevel(2): [
        "Relic 2",
        "Relic 3",
        *_create_floor_check(11, 15)
    ],
    PowerLevel(3,2): [
        "Act 1 Boss",
        "Rare Card Draw 1",
        "Boss Relic 1",
        "Card Draw 6",
        "Card Draw 7",
        *_create_floor_check(16, 22)
    ],
    PowerLevel(6,2): [
        *_create_floor_check(23, 27)
    ],
    PowerLevel(6, 3): [
        "Card Draw 8",
        *_create_floor_check(28, 32)
    ],
    PowerLevel(6, 4): [
        "Card Draw 9",
    ],
    PowerLevel(7, 2): [
        "Relic 4",
        "Relic 5",
    ],
    PowerLevel(7, 3): [
        "Relic 6",
    ],
    PowerLevel(7, 4): [
        "Card Draw 10",
    ],
    PowerLevel(7, 3, 1): [
        "Act 2 Boss",
        "Rare Card Draw 2",
        "Boss Relic 2",
        "Card Draw 11",
        "Card Draw 12",
        "Card Draw 13",
        "Card Draw 14",
        "Card Draw 15",
        "Relic 7",
        *_create_floor_check(33, 49)
    ],
    PowerLevel(7,4,1): [
        "Relic 8",
        "Relic 9",
        "Relic 10",
    ],
    PowerLevel(7,5,2): [
        "Act 3 Boss",
        "Heart Room",
        * _create_floor_check(50, 55)
    ],
}

def setup_power_map(map: dict[PowerLevel, List[str]], prefix: str) -> dict[PowerLevel, List[str]]:
    return {key: [f"{prefix} {x}" for x in val] for key, val in map.items()}

class LogicTestBase(SpireTestBase):

    def _setup_state_accessible(self, original_state: CollectionState, power: PowerLevel) -> CollectionState:

        state = original_state.copy()

        draw = self.get_item_by_name(f"{self.prefix} Card Draw")
        for _ in range(power.draw):
            state.collect(draw)

        relic = self.get_item_by_name(f"{self.prefix} Relic")
        for _ in range(power.relic):
            state.collect(relic)

        boss_relic = self.get_item_by_name(f"{self.prefix} Boss Relic")
        for _ in range(power.boss_relic):
            state.collect(boss_relic)

        return state

    def _setup_state_inaccessible(self, original_state: CollectionState, power: PowerLevel, type: str):

        state = original_state.copy()

        draw = self.get_item_by_name(f"{self.prefix} Card Draw")
        for _ in range(power.draw - 1):
            state.collect(draw)

        relic = self.get_item_by_name(f"{self.prefix} Relic")
        for _ in range(power.relic - 1):
            state.collect(relic)

        boss_relic = self.get_item_by_name(f"{self.prefix} Boss Relic")
        for _ in range(power.boss_relic - 1):
            state.collect(boss_relic)

        if type == "Card Draw":
            if power.relic > 0:
                state.collect(relic)
            if power.boss_relic > 0:
                state.collect(boss_relic)
        elif type == "Relic":
            if power.draw > 0:
                state.collect(draw)
            if power.boss_relic > 0:
                state.collect(boss_relic)
        elif type == "Boss Relic":
            if power.draw > 0:
                state.collect(draw)
            if power.relic > 0:
                state.collect(relic)

        return state

    def _test_inaccessible(self, power: PowerLevel, locations: Iterable[str]):

        for i, type in enumerate([ f"{self.prefix} {x}" for x in ['Card Draw', 'Relic', 'Boss Relic']]):
            if power[i] == 0:
                continue
            state = self._setup_state_inaccessible(self.multiworld.state, power, type)

            for location in locations:
                with self.subTest(f"Cannot access {location} while missing one {type}", reqs=power):
                    loc = self.world.get_location(location)
                    self.assertFalse(loc.can_reach(state),
                                    f"Location {location} can be reached with power level {power}, but missing one {type}; state {state.prog_items}")

    def _test_accessible(self, power: PowerLevel, locations: Iterable[str]):
        state = self._setup_state_accessible(self.multiworld.state, power)

        for location in locations:
            with self.subTest(f"Can access {location} with all reqs", reqs=power):
                loc = self.world.get_location(location)
                self.assertTrue(loc.can_reach(state),
                                f"Location {location} cannot be reached with power level {power} and state {state.prog_items}")


class LogicTests(LogicTestBase):

    power_map: dict[PowerLevel, List[str]]

    def setUp(self) -> None:
        super().setUp()
        self.power_map = setup_power_map(logic_map, self.prefix)

    def test_accessible(self):
        for key, value in self.power_map.items():
            self._test_accessible(key, value)

    def test_inaccessible(self):
        for key, value in self.power_map.items():
            self._test_inaccessible(key, value)

