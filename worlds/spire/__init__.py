import string
from typing import Optional, List

from BaseClasses import Item, ItemClassification, Location, MultiWorld, Region, Tutorial
from .Characters import character_list
from .Items import event_item_pairs, item_table, ItemType, chars_to_items
from .Locations import location_table
from .Options import SpireOptions
from .Regions import create_regions
from .Rules import set_rules
from ..AutoWorld import WebWorld, World


class SpireWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Slay the Spire for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "slay-the-spire_en.md",
        "slay-the-spire/en",
        ["Phar"]
    )]


class SpireWorld(World):
    """
    A deck-building roguelike where you must craft a unique deck, encounter bizarre creatures, discover relics of
    immense power, and Slay the Spire!
    """

    options_dataclass = SpireOptions
    options: SpireOptions
    game = "Slay the Spire"
    topology_present = False
    web = SpireWeb()
    required_client_version = (0, 3, 7)

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    def create_items(self):
        char_val = self.options.character.value
        if type(char_val) is int:
            character = character_list[char_val]
        else:
            # TODO: update to be offset
            character = 1 #character_list[1]
        # Fill out our pool with our items from item_pool, assuming 1 item if not present in item_pool
        pool = []
        for name, data in chars_to_items[character].items():
            amount = 0
            if ItemType.DRAW == data.type:
                amount = 15
            elif ItemType.RARE_DRAW == data.type or ItemType.BOSS_RELIC == data.type:
                amount = 2
            elif ItemType.RELIC == data.type:
                amount = 10
            for _ in range(amount):
                pool.append(SpireItem(name, self.player))


        remaining_checks = 51

        if self.options.final_act:
            remaining_checks += 4
        if self.options.ascension >= 20:
            remaining_checks += 1

        for name in self.random.choices([key for key, val in chars_to_items[character].items()
                                         if ItemType.GOLD == val.type and ItemClassification.filler == val.classification], weights=[40,60],k=remaining_checks):
            pool.append(SpireItem(name, self.player))

        self.multiworld.itempool += pool
        # Pair up our event locations with our event items
        for event, item in event_item_pairs.items():
            event_item = SpireItem(item, self.player)
            try:
                # TODO: UGLY
                self.multiworld.get_location(event, self.player).place_locked_item(event_item)
            except:
                # Expected since no one's running a full squad
                continue

    def set_rules(self):
        set_rules(self, self.player)

    def create_item(self, name: str) -> Item:
        return SpireItem(name, self.player)

    def create_regions(self):
        create_regions(self, self.player)

    def fill_slot_data(self) -> dict:
        slot_data = {
            'seed': "".join(self.random.choice(string.ascii_letters) for i in range(16))
        }
        slot_data.update(self.options.as_dict("character", "ascension", "final_act", "downfall", "death_link"))
        return slot_data

    def get_filler_item_name(self) -> str:
        return self.random.choice(['One Gold', 'Five Gold'])


def create_region(world: MultiWorld, player: int, prefix: Optional[str], name: str, locations: List[str] = None, exits: List[str] =None):
    ret = Region(f"{prefix} {name}" if prefix is not None else name, player, world)
    if locations:
        locs: dict[str, Optional[int]] = dict()
        for location in locations:
            loc_name = f"{prefix} {location}" if prefix is not None else location
            loc_id = location_table.get(loc_name, 0)
            locs[loc_name] = loc_id
        ret.add_locations(locs, SpireLocation)
    if exits:
        for exit in exits:
            exit_name = f"{prefix} {exit}" if prefix is not None else exit
            ret.create_exit(exit_name)
    return ret


class SpireLocation(Location):
    game: str = "Slay the Spire"


class SpireItem(Item):
    game = "Slay the Spire"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(SpireItem, self).__init__(
            name,
            item_data.classification,
            item_data.code, player
        )
