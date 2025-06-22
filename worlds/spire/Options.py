from dataclasses import dataclass
from typing import List

from schema import Schema, Optional, And

from Options import TextChoice, Range, Toggle, PerGameCommonOptions, Visibility, OptionDict, Choice, OptionSet, \
    FreeText, OptionGroup

NUM_CUSTOM = 5

class Character(OptionSet):
    """Enter the list of characters to play as.  Valid characters are:
        'Ironclad'
        'Silent'
        'Defect'
        'Watcher'
        'Hermit'
        'SlimeBoss'
        'Guardian'
        'Hexaghost'
        'Champ'
        'Gremlins'
        'Automaton'
        'Snecko'
        'Collector'"""
    display_name = "Character"
    valid_keys = [
        "Ironclad",
        "Silent",
        "Defect",
        "Watcher",
        "Hermit",
        "SlimeBoss",
        "Guardian",
        "Hexaghost",
        "Champ",
        "Gremlins",
        "Automaton",
        "Snecko",
        "Collector",
    ]
    default = ["Ironclad"]
    valid_keys_casefold = False
    # TODO: Spire Takes the wheel doesn't work with the current setup
    # option_spire_take_the_wheel = 12

class GoalNumChar(Range):
    """How many characters you need to complete a run with before you goal. 0 means all characters"""
    display_name = "Number of Characters to Goal"
    range_start = 0
    range_end = 13 + NUM_CUSTOM
    default = 0

class Ascension(Range):
    """What Ascension do you wish to play with."""
    display_name = "Ascension"
    range_start = 0
    range_end = 20
    default = 0

class PickNumberCharacters(Range):
    """Randomly select from the configured characters this many characters to generate for.
    0 disables."""
    display_name = "Pick Number of Characters"
    range_start = 0
    range_end = 13 + NUM_CUSTOM - 1
    default = 0

class FinalAct(Toggle):
    """Whether you will need to collect the 3 keys and beat the final act to complete the game."""
    display_name = "Final Act"
    default = 0


class Downfall(Toggle):
    """When Downfall is Installed this will switch the played mode to Downfall"""
    display_name = "Downfall"
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
    default = 1

class CampfireSanity(Toggle):
    """Whether to shuffle being able to rest and smith at each campsite per act.  Also adds
    new locations at campsites per act."""
    display_name = "Campfire Sanity"
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

class ShopRemoveSlots(Toggle):
    """When shop_sanity is enabled, whether to shuffle the ability to remove cards at the shop.
    Progressive based on Act; i.e. you'll gain the ability to remove cards per Act, starting from Act 1.
    Act 4 will be treated as Act 3."""
    display_name = "Shop Remove Slots"
    default = 0

class ShopSanityCosts(Choice):
    """How expensive the AP shop items should be. Tiered means costs map to typical costs rarity for the slot.
    Progression = Rare, Useful = Uncommon, Filler = Common
    Logic does not take this option into account.
    Fixed=15 gold each
    Super_Discount_Tiered=20% of tiered costs
    Discount_Tiered=50% of tiered costs
    Tiered=Vanilla price for slot
    """
    display_name = "Shop Sanity Costs"
    option_Fixed = 0
    option_Super_Discount_Tiered = 1
    option_Discount_Tiered = 2
    option_Tiered = 3
    default = 2

class GoldSanity(Toggle):
    """Whether to enable shuffling gold rewards into the multiworld. Adds 27 locations per character"""
    display_name = "Gold Sanity"
    default = 0

class PotionSanity(Toggle):
    """Whether to enable shuffling potion drops into the multiworld; adds 9 locations per character."""
    display_name = "Potion Sanity"
    default = 0

class SeededRun(Toggle):
    """Whether each character should have a fixed seed to climb the spire with or not."""
    display_name = "Seeded Run"
    default = 0

class ChattyMC(Toggle):
    """Whether the MC should talk about AP events."""
    display_name = "Chatty MC"
    default = 1

class AdvancedChar(Toggle):
    """Whether to use the advanced characters feature. The normal options for character, ascension, etc. are ignored.
    See the "advanced_characters" option.
    """
    visibility = Visibility.template
    display_name = "Multiple Character Run"
    option_true = 1
    option_false = 0
    default = 0

class LockCharacters(Choice):
    """Whether in a multi character run "Unlock [Char]" items should be shuffled in.
    locked_fixed means the unlocked_character option is used to determine which character to start with
    locked_random means which character you start with is randomized
    unlocked means you start with all characters available"""
    visibility = Visibility.template
    display_name = "Lock Characters"
    option_unlocked = 0
    option_locked_random = 1
    option_locked_fixed = 2
    default = 1

class UnlockedCharacter(FreeText):
    """Which character to start unlocked, if lock_characters is set to 2"""

class CharacterOptions(OptionDict):
    """The configuration for advanced characters.  Each character's options can be configured
    independently of each other.  No validation is done on the character name, so use carefully.
    Format is:
        <char name>:
            ascension:
            downfall:
            final_act:

    If using a non-downfall modded character:
    Enter the internal ID of the character to use.

     if you don't know the exact ID to enter with the mod installed go to
    `Mods -> Archipelago Multi-world -> config` to view a list of installed modded character IDs.

    the downfall characters will only work if you have downfall installed.
    If the chosen character mod is not installed, checks will be sent when another character
    sends them.  If none of the chosen character mods are installed, you will be playing
    a very boring Ironclad run.
    """
    visibility = Visibility.template
    default = {
        "ironclad": {
            "ascension": 0,
            "final_act": 1,
            "downfall": 1,
        }
    }
    schema = Schema({
        str: {
            Optional("ascension", default=0): And(int,lambda n: 0 <= n <= 20),
            Optional("final_act", default=0): And(int, lambda n: 0 <= n <= 1),
            Optional("downfall", default=0): And(int, lambda n: 0 <= n <= 1),
        }
    })

@dataclass
class SpireOptions(PerGameCommonOptions):
    character: Character
    num_chars_goal: GoalNumChar
    ascension: Ascension
    final_act: FinalAct
    downfall: Downfall
    death_link: DeathLink
    include_floor_checks: IncludeFloorChecks
    use_advanced_characters: AdvancedChar
    lock_characters: LockCharacters
    unlocked_character: UnlockedCharacter
    advanced_characters: CharacterOptions
    pick_num_characters: PickNumberCharacters
    campfire_sanity: CampfireSanity
    gold_sanity: GoldSanity
    potion_sanity: PotionSanity
    seeded: SeededRun
    chatty_mc: ChattyMC
    shop_sanity: ShopSanity
    shop_card_slots: ShopCardSlots
    shop_neutral_card_slots: ShopNeutralSlots
    shop_relic_slots: ShopRelicSlots
    shop_potion_slots: ShopPotionSlots
    shop_remove_slots: ShopRemoveSlots
    shop_sanity_costs: ShopSanityCosts

option_groups: List[OptionGroup] = [
    OptionGroup("Sanities", [
        IncludeFloorChecks,
        CampfireSanity,
        GoldSanity,
        PotionSanity,
        ShopSanity,
        ShopCardSlots,
        ShopNeutralSlots,
        ShopRelicSlots,
        ShopPotionSlots,
        ShopRemoveSlots,
        ShopSanityCosts,
    ]),
    OptionGroup("Misc", [
        ChattyMC,
    ])
]