from dataclasses import dataclass

from schema import Schema, Optional, And

from Options import TextChoice, Range, Toggle, PerGameCommonOptions, Visibility, OptionDict


class Character(TextChoice):
    """Enter the internal ID of the character to use.

      if you don't know the exact ID to enter with the mod installed go to
     `Mods -> Archipelago Multi-world -> config` to view a list of installed modded character IDs.

     the downfall characters will only work if you have downfall installed.

     Spire Take the Wheel will have your client pick a random character from the list of all your installed characters
     including custom ones.

     if the chosen character mod is not installed it will default back to 'The Ironclad'
     """
    display_name = "Character"
    option_The_Ironclad = 0
    option_The_Silent = 1
    option_The_Defect = 2
    option_The_Watcher = 3
    option_The_Hermit = 4
    option_The_Slime_Boss = 5
    option_The_Guardian = 6
    option_The_Hexaghost = 7
    option_The_Champ = 8
    option_The_Gremlins = 9
    option_The_Automaton = 10
    option_The_Snecko = 11
    # TODO: Spire Takes the wheel doesn't work with the current setup
    # option_spire_take_the_wheel = 12


class Ascension(Range):
    """What Ascension do you wish to play with."""
    display_name = "Ascension"
    range_start = 0
    range_end = 20
    default = 0


class FinalAct(Toggle):
    """Whether you will need to collect the 3 keys and beat the final act to complete the game."""
    display_name = "Final Act"
    option_true = 1
    option_false = 0
    default = 0


class Downfall(Toggle):
    """When Downfall is Installed this will switch the played mode to Downfall"""
    display_name = "Downfall"
    option_true = 1
    option_false = 0
    default = 0


class DeathLink(Range):
    """Percentage of health to lose when a death link is received."""
    display_name = "Death Link %"
    range_start = 0
    range_end = 100
    default = 0

class IncludeFloorChecks(Toggle):
    """Whether to include reaching new floors as a location.  Adds small amounts of gold as items."""
    display_name = "Include Floor Checks"
    option_true = 1
    option_false = 0
    default = 1

class CampfireSanity(Toggle):
    """Whether to shuffle being able to rest and smith at each campsite per act.  Also adds
    new locations at campsites per act."""
    display_name = "Campfire Sanity"
    option_true = 1
    option_false = 0
    default = 0

class ShopSanity(Toggle):
    """Whether to shuffle shop slots into the pool.  Also adds new locations at the shop per slot shuffled."""
    display_name = "Shop Sanity"
    option_true = 1
    option_false = 0
    default = 0

class ShopCardSlots(Range):
    """When shop_sanity is enabled, the number of colored card slots to shuffle."""
    display_name = "Shop Card Slots"
    range_start = 0
    range_end = 5
    default = 2

class ShopNeutralSlots(Range):
    """When shop_sanity is enabled, the number of neutral card slots to shuffle."""
    display_name = "Shop Neutral Card Slots"
    range_start = 0
    range_end = 2
    default = 1

class ShopRelicSlots(Range):
    """WHen shop_sanity is enabled, the number of relic slots to shuffle."""
    display_name = "Shop Relic Slots"
    range_start = 0
    range_end = 3
    default = 2

class ShopPotionSlots(Range):
    """When shop_sanity is enabled, the number of potion slots to shuffle"""
    display_name = "Shop Potion Slots"
    range_start = 0
    range_end = 3
    default = 2

class ShopRemoveSlot(Toggle):
    """When shop_sanity is enabled, whether to shuffle the ability to remove cards at the shop.
    Progressive based on Act; i.e. you'll gain the ability to remove cards per Act, starting from Act 1.
    Act 4 will be treated as Act 3."""
    display_name = "Shop Remove Slot"
    option_true = 1
    option_false = 0
    default = 0

class MultiChar(Toggle):
    """Whether to enable a multi character run. "Spire Take the Wheel" does not work with this feature,
    and the normal options for character, ascension, etc. are ignored. See the "characters" option."""
    visibility = Visibility.template
    display_name = "Multiple Character Run"
    option_true = 1
    option_false = 0
    default = 0

class CharacterOptions(OptionDict):
    """The configuration for multicharacter.  Each character's options can be configured
    independently of each other.  No validation is done on the character name, so use carefully.
    """
    visibility = Visibility.template
    default = {
        "the_ironclad": {
            "ascension": 0,
            "final_act": False,
            "downfall": False,
        }
    }
    schema = Schema({
        str: {
            Optional("ascension", default=0): And(int,lambda n: 0 <= n <= 20),
            Optional("final_act", default=False): bool,
            Optional("downfall", default=False): bool,
        }
    })

@dataclass
class SpireOptions(PerGameCommonOptions):
    character: Character
    ascension: Ascension
    final_act: FinalAct
    downfall: Downfall
    death_link: DeathLink
    include_floor_checks: IncludeFloorChecks
    multi_char: MultiChar
    characters: CharacterOptions
    campfire_sanity: CampfireSanity
    shop_sanity: ShopSanity
    shop_card_slots: ShopCardSlots
    shop_neutral_card_slots: ShopNeutralSlots
    shop_relic_slots: ShopRelicSlots
    shop_potion_slots: ShopPotionSlots
    shop_remove_slots: ShopRemoveSlot
