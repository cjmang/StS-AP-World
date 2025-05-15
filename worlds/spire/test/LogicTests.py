from typing import List, Optional

from typing_extensions import NamedTuple, Iterable

from BaseClasses import CollectionState
from worlds.spire.Rules import PowerLevel
from worlds.spire.test import SpireTestBase

def _create_floor_check(start: int, end: int) -> List[str]:
    return [f"Reached Floor {i}" for i in range(start, end + 1)]

logic_map: dict[PowerLevel, List[str]] = {
    PowerLevel(): [
        "Card Draw 1",
        "Card Draw 2",
        "Card Draw 3",
        "Act 1 Campfire 1",
        "Act 1 Campfire 2",
        *_create_floor_check(1,10)
    ],
    PowerLevel(1): [
        "Relic 1",
    ],
    PowerLevel(draw=0,relic=1, rest=1): [
        "Card Draw 4",
        "Card Draw 5",
    ],
    PowerLevel(draw=2,rest=1): [
        "Relic 2",
        "Relic 3",
        *_create_floor_check(11, 15)
    ],
    PowerLevel(draw=3,relic=2, rest=1, smith=1): [
        "Act 1 Boss",
        "Rare Card Draw 1",
        "Boss Relic 1",
        "Card Draw 6",
        "Card Draw 7",
        *_create_floor_check(16, 22)
    ],
    PowerLevel(draw=6,relic=2, rest=2,smith=1): [
        "Act 2 Campfire 1",
        "Act 2 Campfire 2",
        *_create_floor_check(23, 27)
    ],
    PowerLevel(draw=6, relic=3, rest=2, smith=1): [
        "Card Draw 8",
        *_create_floor_check(28, 32)
    ],
    PowerLevel(draw=6, relic=4, rest=2, smith=1): [
        "Card Draw 9",
    ],
    PowerLevel(draw=7, relic=2, rest=2,smith=1): [
        "Relic 4",
        "Relic 5",
    ],
    PowerLevel(draw=7, relic=3, rest=2,smith=1): [
        "Relic 6",
    ],
    PowerLevel(draw=7, relic=4, rest=2, smith=1): [
        "Card Draw 10",
    ],
    PowerLevel(draw=7, relic=3, boss_relic=1, rest=2, smith=2): [
        "Act 2 Boss",
        "Rare Card Draw 2",
        "Boss Relic 2",
        "Card Draw 11",
        "Card Draw 12",
        *_create_floor_check(33, 39)
    ],
    PowerLevel(draw=7,relic=3,boss_relic=1, rest=3,smith=2): [
        "Card Draw 13",
        "Card Draw 14",
        "Card Draw 15",
        "Relic 7",
        "Act 3 Campfire 1",
        "Act 3 Campfire 2",
        *_create_floor_check(40, 49)
    ],
    PowerLevel(draw=7,relic=4,boss_relic=1, rest=3,smith=2): [
        "Relic 8",
        "Relic 9",
        "Relic 10",
    ],
    PowerLevel(draw=7,relic=5,boss_relic=2,rest=3,smith=3): [
        "Act 3 Boss",
        "Heart Room",
        * _create_floor_check(50, 55)
    ],
}

def setup_power_map(map: dict[PowerLevel, List[str]], prefix: str) -> dict[PowerLevel, List[str]]:
    return {key: [f"{prefix} {x}" for x in val] for key, val in map.items()}

class LogicTestBase(SpireTestBase):

    options = {
        'character': 1,
        'final_act': 1,
        'campfire_sanity':1,
    }

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

        rest = self.get_item_by_name(f"{self.prefix} Progressive Rest")
        for _ in range(power.rest):
            state.collect(rest)

        smith = self.get_item_by_name(f"{self.prefix} Progressive Smith")
        for _ in range(power.smith):
            state.collect(smith)

        return state

    def _setup_state_inaccessible(self, original_state: CollectionState, power: PowerLevel, type: str):

        state = original_state.copy()

        draw = self.get_item_by_name(f"{self.prefix} Card Draw")
        draws = [draw for _ in range(power.draw)]

        relic = self.get_item_by_name(f"{self.prefix} Relic")
        relics = [relic for _ in range(power.relic)]

        boss_relic = self.get_item_by_name(f"{self.prefix} Boss Relic")
        boss_relics = [boss_relic for _ in range(power.boss_relic)]

        rest = self.get_item_by_name(f"{self.prefix} Progressive Rest")
        rests = [rest for _ in range(power.rest)]

        smith = self.get_item_by_name(f"{self.prefix} Progressive Smith")
        smiths = [smith for _ in range(power.smith)]
        if type == "Card Draw":
            draws.pop()
        elif type == "Relic":
            relics.pop()
        elif type == "Boss Relic":
            boss_relics.pop()
        elif type == "Progressive Rest":
            rests.pop()
        elif type == "Progressive Smith":
            smiths.pop()

        for list in [draws, relics, boss_relics, rests, smiths]:
            for item in list:
                state.collect(item)

        return state

    def _test_inaccessible(self, power: PowerLevel, locations: Iterable[str]):

        for i, type in enumerate([ x for x in ['Card Draw', 'Relic', 'Boss Relic', 'Progressive Rest', 'Progressive Smith']]):
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

class CustomCharTest(LogicTests):
    prefix = "Custom Character 1"
    options = {
        'character': 'foobar',
        'final_act': 1,
        'campfire_sanity': 1,
    }
