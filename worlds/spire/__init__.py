import logging
import string
from logging import Logger
from typing import Optional, List, Set

from BaseClasses import Item, ItemClassification, Location, MultiWorld, Region, Tutorial
from Options import OptionError
from .Characters import character_list, CharacterConfig, character_option_map, character_offset_map, NUM_CUSTOM
from .Items import event_item_pairs, item_table, ItemType, chars_to_items, base_event_item_pairs, item_groups
from .Locations import location_table, loc_ids_to_data, LocationData, LocationType, CARD_DRAW_COUNT, location_groups
from .Options import SpireOptions, option_groups
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
    option_groups = option_groups

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
    required_client_version = (0, 6, 1)
    mod_version = 2
    location_name_groups = location_groups
    item_name_groups = item_groups

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table
    logger = logging.getLogger("SlayTheSpire")

    def __init__(self, mw: MultiWorld, player: int):
        super().__init__(mw, player)
        self.characters: List[CharacterConfig] = []
        self.modded_num = 0
        self.modded_chars: List[CharacterConfig] = []
        self.total_shop_locations = 0
        self.total_shop_items = 0

    def generate_early(self):
        if self.options.use_advanced_characters.value == 0:
            char_options = self.options.character.value
            num_rand_chars = self.options.pick_num_characters.value
            if num_rand_chars != 0 and num_rand_chars < len(char_options):
                char_options = self.random.sample(list(char_options), k=num_rand_chars)
            unlocked_char = self._get_unlocked_char(char_options)
            self.logger.info("Generating with characters %s", char_options)
            for char_val in char_options:
                option_name = char_val
                char_offset = character_offset_map[option_name.lower()]
                name = character_list[char_offset]
                if self.options.seeded:
                    seed = "".join(self.random.choice(string.ascii_letters) for i in range(16))
                else:
                    seed = ""
                locked = False if unlocked_char is None or unlocked_char.lower() == option_name.lower() else True

                config = CharacterConfig(name,
                                         option_name,
                                         char_offset,
                                         0,
                                         seed,
                                         locked,
                                         ascension=self.options.ascension.value,
                                         final_act=self.options.final_act.value==1,
                                         downfall=self.options.downfall.value==1)
                self.characters.append(config)
        else:
            advanced_chars = self.options.advanced_characters.keys()
            num_rand_chars = self.options.pick_num_characters.value
            if num_rand_chars != 0 and num_rand_chars < len(advanced_chars):
                advanced_chars = self.random.sample(list(advanced_chars), k=num_rand_chars)
            unlocked_char = self._get_unlocked_char(advanced_chars)
            self.logger.info("Generating with characters %s", advanced_chars)
            for option_name in advanced_chars:
                options = self.options.advanced_characters[option_name]
                mod_num = 0
                char_offset = character_offset_map.get(option_name.lower(), None)
                if char_offset is None:
                    self.modded_num += 1
                    mod_num = self.modded_num
                    char_offset = mod_num + len(character_list) - 1
                    name = f"Custom Character {mod_num}"
                else:
                    name = character_list[char_offset]
                if self.options.seeded:
                    seed = "".join(self.random.choice(string.ascii_letters) for i in range(16))
                else:
                    seed = ""
                locked = False if unlocked_char is None or unlocked_char.lower() == option_name.lower() else True
                config = CharacterConfig(name,
                                         option_name,
                                         char_offset,
                                         mod_num,
                                         seed,
                                         locked,
                                         **options)
                self.characters.append(config)
                if config.mod_num > 0:
                    self.modded_chars.append(config)
        names = set()
        for config in self.characters:
            self.logger.info("StS: Got character configuration" + str(config))
            names.add(config.official_name)
        if len(names) != len(self.characters):
            raise OptionError(f"Found duplicate characters: {names}")
        for config in self.characters:
            if not config.locked:
                break
        else:
            raise OptionError("No character started unlocked!")
        self.total_shop_items = (self.options.shop_card_slots.value + self.options.shop_neutral_card_slots.value +
                                     self.options.shop_relic_slots.value + self.options.shop_potion_slots.value)
        self.total_shop_locations = self.total_shop_items + (3 if self.options.shop_remove_slots else 0)
        if self.total_shop_locations <= 0:
            self.options.shop_sanity.value = 0
        if len(self.modded_chars) > NUM_CUSTOM:
            raise OptionError(f"StS only supports {NUM_CUSTOM} modded characters; got {len(self.modded_chars)}: {[x.option_name for x in self.modded_chars]}")
        num_chars_goal = self.options.num_chars_goal.value
        if num_chars_goal != 0:
            if num_chars_goal > len(self.characters):
                self.options.num_chars_goal.value = 0

    def _get_unlocked_char(self, characters: Set[str]) -> Optional[str]:
        if len(characters) <= 0:
            raise OptionError("At least one character must be selected.")
        locked_opt = self.options.lock_characters.value
        unlocked_char = None
        if locked_opt == 1:
            unlocked_char = self.random.choice([x for x in characters])
        elif locked_opt == 2:
            unlocked_char = self.options.unlocked_character.value
            if unlocked_char not in characters:
                raise OptionError(
                    f"Configured {unlocked_char} as the first unlocked character, but was not one of: {characters}")
        return unlocked_char

    def create_items(self):
        # Fill out our pool with our items from item_pool, assuming 1 item if not present in item_pool
        pool = []
        for config in self.characters:
            char_lookup = config.name if config.mod_num == 0 else config.mod_num
            for name, data in chars_to_items[char_lookup].items():
                amount = 0
                if ItemType.DRAW == data.type:
                    amount = CARD_DRAW_COUNT
                elif ItemType.RARE_DRAW == data.type or ItemType.BOSS_RELIC == data.type:
                    amount = 2
                elif ItemType.RELIC == data.type:
                    amount = 10
                elif ItemType.CAMPFIRE == data.type and self.options.campfire_sanity.value != 0:
                    amount = 3
                elif ItemType.CHAR_UNLOCK == data.type and self.options.lock_characters.value != 0 and config.locked:
                    amount = 1
                elif ItemType.GOLD == data.type and self.options.gold_sanity.value != 0:
                    if '15 Gold' in name:
                        amount = 18
                    elif '30 Gold' in name:
                        amount = 7
                    elif 'Boss Gold' in name:
                        amount = 2
                elif ItemType.POTION == data.type and self.options.potion_sanity:
                    amount = 9
                elif self.options.shop_sanity.value != 0:
                    if ItemType.SHOP_CARD == data.type:
                        amount = self.options.shop_card_slots.value
                    elif ItemType.SHOP_NEUTRAL == data.type:
                        amount = self.options.shop_neutral_card_slots.value
                    elif ItemType.SHOP_RELIC == data.type:
                        amount = self.options.shop_relic_slots.value
                    elif ItemType.SHOP_POTION == data.type:
                        amount = self.options.shop_potion_slots.value
                    elif ItemType.SHOP_REMOVE == data.type and self.options.shop_remove_slots.value != 0:
                        amount = 3
                for _ in range(amount):
                    pool.append(SpireItem(name, self.player))

            if self.options.include_floor_checks.value:
                remaining_checks = 51

                if config.final_act:
                    remaining_checks += 4
                if config.ascension >= 20:
                    remaining_checks += 1
                for name in self.random.choices([key for key, val in chars_to_items[char_lookup].items()
                                                 if ItemType.GOLD == val.type and ItemClassification.filler == val.classification], weights=[40,60],k=remaining_checks):
                    pool.append(SpireItem(name, self.player))
            # Pair up our event locations with our event items
            for base_event, base_item in base_event_item_pairs.items():
                event = f"{config.name} {base_event}"
                item = f"{config.name} {base_item}"
                event_item = SpireItem(item, self.player)
                self.multiworld.get_location(event, self.player).place_locked_item(event_item)

        self.multiworld.itempool += pool

    def set_rules(self):
        set_rules(self, self.player)

    def create_item(self, name: str) -> Item:
        return SpireItem(name, self.player)

    def create_regions(self):
        create_regions(self, self.player)

    def fill_slot_data(self) -> dict:
        slot_data = {
            'characters': [
                c.to_dict() for c in self.characters
            ],
            'shop_sanity_options': {
                "card_slots": self.options.shop_card_slots.value,
                "neutral_slots": self.options.shop_neutral_card_slots.value,
                "relic_slots": self.options.shop_relic_slots.value,
                "potion_slots": self.options.shop_potion_slots.value,
                "card_remove": self.options.shop_remove_slots != 0,
                "costs": self.options.shop_sanity_costs.value,
            },
            "mod_version": self.mod_version,
        }
        slot_data.update(self.options.as_dict(
            "character",
            "ascension",
            "final_act",
            "downfall",
            "death_link",
            "include_floor_checks",
            "campfire_sanity",
            "shop_sanity",
            "gold_sanity",
            "potion_sanity",
            "chatty_mc",
            "num_chars_goal",
        ))
        return slot_data

    def get_filler_item_name(self) -> str:
        config = self.characters[0]
        return self.random.choice([f"{config.name} One Gold", f"{config.name} Five Gold"])


    def create_region(self, player: int, prefix: Optional[str], name: str, config: CharacterConfig, locations: List[str] = None, exits: List[str] =None):
        ret = Region(f"{prefix} {name}" if prefix is not None else name, player, self.multiworld)
        if locations:
            locs: dict[str, Optional[int]] = dict()
            for location in locations:
                loc_name = f"{prefix} {location}" if prefix is not None else location
                loc_id = location_table.get(loc_name, 0)
                loc_data = loc_ids_to_data.get(loc_id, None)
                if self._should_include_location(loc_data, config):
                    locs[loc_name] = loc_id
            ret.add_locations(locs, SpireLocation)
        if exits:
            for exit in exits:
                exit_name = f"{prefix} {exit}" if prefix is not None else exit
                ret.create_exit(exit_name)
        return ret

    def _should_include_location(self, data: LocationData, config: CharacterConfig) -> bool:
        if data is None:
            return True
        if data.type == LocationType.Floor and self.options.include_floor_checks == 0:
            return False
        elif data.type == LocationType.Campfire and self.options.campfire_sanity == 0:
            return False
        elif data.type == LocationType.Shop:
            if self.options.shop_sanity.value == 0:
                return False
            total_shop = self.total_shop_locations
            return total_shop >= data.id - 163
        elif data.type == LocationType.Start and (self.options.lock_characters == 0 or not config.locked):
            return False
        elif data.type == LocationType.Gold and self.options.gold_sanity.value == 0:
            return False
        elif data.type == LocationType.Potion and self.options.potion_sanity.value == 0:
            return False
        return True


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
