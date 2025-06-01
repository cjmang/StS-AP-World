from collections import defaultdict
from enum import Enum, auto
from typing import Optional, List, Tuple, Union, NamedTuple

from worlds.spire import character_list
from worlds.spire.Characters import NUM_CUSTOM

CARD_DRAW_COUNT = 13

CHAR_OFFSET = 200

class LocationType(Enum):
    Draw = auto()
    Rare_Draw = auto()
    Relic = auto()
    Boss_Relic = auto()
    Floor = auto()
    Campfire = auto()
    Event = auto()
    Shop = auto()
    Start = auto()


class LocationData(NamedTuple):
    name: str
    id: Optional[int]
    type: LocationType

def create_location_data() -> List[LocationData]:
    return ([LocationData(f"Reached Floor {j}", j, LocationType.Floor) for j in range(1, 56)] +
            [LocationData(f"Card Draw {j}", j + 100, LocationType.Draw) for j in range(1,CARD_DRAW_COUNT + 1)] +
            [LocationData(f"Relic {j}", j + 140, LocationType.Relic) for j in range(1, 11)] +
            [LocationData(f"Shop Slot {j}", j + 163, LocationType.Shop) for j in range(1,17)] +
            # [LocationData(f"Shop Card Slot {j}", j + 163, LocationType.Shop) for j in range(1,5)] +
            # [LocationData(f"Shop Neutral Card Slot {j}", j + 168, LocationType.Shop) for j in range(1,2)] +
            # [LocationData(f"Shop Relic Slot {j}", j + 170, LocationType.Shop) for j in range(1,3)] +
            # [LocationData(f"Shop Potion Slot {j}", j + 173, LocationType.Shop) for j in range(1,3)] +
            # [LocationData(f"Shop Remove Slot {j}", j + 176, LocationType.Shop) for j in range(1,3)] +
            [LocationData('Act 1 Campfire 1', 121, LocationType.Campfire),
            LocationData('Act 1 Campfire 2', 122, LocationType.Campfire),
            LocationData('Act 2 Campfire 1', 123, LocationType.Campfire),
            LocationData('Act 2 Campfire 2', 124, LocationType.Campfire),
            LocationData('Act 3 Campfire 1', 125, LocationType.Campfire),
            LocationData('Act 3 Campfire 2', 126, LocationType.Campfire),
            LocationData('Rare Card Draw 1', 131, LocationType.Rare_Draw),
            LocationData('Rare Card Draw 2', 132, LocationType.Rare_Draw),
            LocationData('Boss Relic 1', 161, LocationType.Boss_Relic),
            LocationData('Boss Relic 2', 162, LocationType.Boss_Relic),
            LocationData('Press Start', 163, LocationType.Start),
            LocationData('Heart Room', None, LocationType.Event),
            LocationData('Act 1 Boss', None, LocationType.Event),
            LocationData('Act 2 Boss', None, LocationType.Event),
            LocationData('Act 3 Boss', None, LocationType.Event),
    ])

def create_location_tables(vanilla_chars: List[str], extras: int) -> Tuple[dict[str, int], dict[
    Union[str, int],dict[str,LocationData]],dict[int,LocationData]]:
    loc_name_to_id = dict()
    characters_to_locs: dict[Union[str, int],dict[str, LocationData]] = defaultdict(lambda: dict())
    ids_to_data: dict[int, LocationData] = dict()
    char_num = 0

    base_location_data = create_location_data()

    for char in vanilla_chars:
        for data in base_location_data:
            newkey = f"{char} {data.name}"
            newval = data.id + char_num*CHAR_OFFSET if data.type != LocationType.Event else data.id
            loc_name_to_id[newkey] = newval
            characters_to_locs[char][newkey] = data
            if newval is not None:
                ids_to_data[newval] = data
        char_num += 1

    for i in range(extras):
        for data in base_location_data:
            newkey = f"Custom Character {i+1} {data.name}"
            newval = data.id + char_num * CHAR_OFFSET if data.type != LocationType.Event else data.id
            loc_name_to_id[newkey] = newval
            characters_to_locs[i+1][newkey] = data
            if newval is not None:
                ids_to_data[newval] = data
        char_num += 1

    return loc_name_to_id, characters_to_locs, ids_to_data

location_table, characters_to_locs, loc_ids_to_data = create_location_tables(character_list, NUM_CUSTOM)