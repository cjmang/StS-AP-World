from collections import defaultdict
from typing import Optional, List, Tuple, Union

from worlds.spire import character_list
from worlds.spire.Characters import NUM_CUSTOM

CHAR_OFFSET = 200

base_location_table: dict[str, Optional[int]] = {
    'Card Draw 1': 101,
    'Card Draw 2': 102,
    'Card Draw 3': 103,
    'Card Draw 4': 104,
    'Card Draw 5': 105,
    'Card Draw 6': 106,
    'Card Draw 7': 107,
    'Card Draw 8': 108,
    'Card Draw 9': 109,
    'Card Draw 10': 110,
    'Card Draw 11': 111,
    'Card Draw 12': 112,
    'Card Draw 13': 113,
    'Card Draw 14': 114,
    'Card Draw 15': 115,
    'Rare Card Draw 1': 131,
    'Rare Card Draw 2': 132,
    'Relic 1': 141,
    'Relic 2': 142,
    'Relic 3': 143,
    'Relic 4': 144,
    'Relic 5': 145,
    'Relic 6': 146,
    'Relic 7': 147,
    'Relic 8': 148,
    'Relic 9': 149,
    'Relic 10': 150,
    'Boss Relic 1': 161,
    'Boss Relic 2': 162,
    'Heart Room': None,
    'Act 1 Boss': None,
    'Act 2 Boss': None,
    'Act 3 Boss': None,
}

for i in range(1, 56):
    base_location_table[f"Reached Floor {i}"] = i

def create_location_tables(vanilla_chars: List[str], extras: int) -> Tuple[dict[str, int], dict[
    Union[str, int],dict[str,int]]]:
    loc_name_to_data = dict()
    characters_to_locs: dict[Union[str, int],dict[str, int]] = defaultdict(lambda: dict())
    char_num = 0

    for char in vanilla_chars:
        for key, data in base_location_table.items():

            newkey = f"{char} {key}"
            newval = data + char_num*CHAR_OFFSET if data is not None else data
            loc_name_to_data[newkey] = newval
            characters_to_locs[char][newkey] = newval
        char_num += 1

    for i in range(extras):
        for key, data in base_location_table.items():
            newkey = f"Custom Character {i+1} {key}"
            newval = data + char_num * CHAR_OFFSET if data is not None else data
            loc_name_to_data[newkey] = newval
            characters_to_locs[i+1][newkey] = newval
        char_num += 1

    return loc_name_to_data, characters_to_locs

location_table, characters_to_locs = create_location_tables(character_list, NUM_CUSTOM)