from typing import TYPE_CHECKING, List

from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule

if TYPE_CHECKING:
    from . import SpireWorld, CharacterConfig


class SpireLogic(LogicMixin):
    def _spire_has_relics(self, player: int, prefix, amount: int) -> bool:
        count: int = self.count(f"{prefix} Relic", player) + self.count(f"{prefix} Boss Relic", player)
        return count >= amount

    def _spire_has_cards(self, player: int, prefix, amount: int) -> bool:
        count = self.count(f"{prefix} Card Draw", player) + self.count(f"{prefix} Rare Card Draw", player)
        return count >= amount

    def _spire_has_victories(self, player: int, configs: List['CharacterConfig']):
        for config in configs:
            if not self.has(f"{config.name} Victory", player):
                return False
        return True


def set_rules(world: 'SpireWorld', player: int):
    from . import character_list
    multiworld = world.multiworld
    for config in world.characters:
        _set_rules(world, player, config)

    multiworld.completion_condition[player] = lambda state: state._spire_has_victories(player, world.characters)

def _set_rules(world: 'SpireWorld', player: int, config: 'CharacterConfig'):
    multiworld = world.multiworld
    prefix = config.name
    # Act 1 Card Draws
    set_rule(multiworld.get_location(f"{prefix} Card Draw 1", player), lambda state: True)
    set_rule(multiworld.get_location(f"{prefix} Card Draw 2", player), lambda state: True)
    set_rule(multiworld.get_location(f"{prefix} Card Draw 3", player), lambda state: True)
    set_rule(multiworld.get_location(f"{prefix} Card Draw 4", player), lambda state: state._spire_has_relics(player, prefix, 1))
    set_rule(multiworld.get_location(f"{prefix} Card Draw 5", player), lambda state: state._spire_has_relics(player, prefix, 1))

    # Act 1 Relics
    set_rule(multiworld.get_location(f"{prefix} Relic 1", player), lambda state: state._spire_has_cards(player, prefix, 1))
    set_rule(multiworld.get_location(f"{prefix} Relic 2", player), lambda state: state._spire_has_cards(player, prefix, 2))
    set_rule(multiworld.get_location(f"{prefix} Relic 3", player), lambda state: state._spire_has_cards(player, prefix, 2))

    set_rule(multiworld.get_entrance(f"{prefix} Late Act 1", player), lambda state: state._spire_has_cards(player, prefix, 2))

    # Act 1 Boss Event
    set_rule(multiworld.get_entrance(f"{prefix} Act 1 Boss Arena", player),lambda state: state._spire_has_cards(player, prefix, 3) and
                                                                                         state._spire_has_relics(player, prefix, 2))

    # Act 1 Boss Rewards
    set_rule(multiworld.get_location(f"{prefix} Rare Card Draw 1", player), lambda state: state.has(f"{prefix} Beat Act 1 Boss", player))
    set_rule(multiworld.get_location(f"{prefix} Boss Relic 1", player), lambda state: state.has(f"{prefix} Beat Act 1 Boss", player))

    set_rule(multiworld.get_entrance(f"{prefix} Early Act 2", player), lambda state: state.has(f"{prefix} Beat Act 1 Boss", player))

    # Act 2 Card Draws
    set_rule(multiworld.get_location(f"{prefix} Card Draw 6", player), lambda state: state.has(f"{prefix} Beat Act 1 Boss", player))
    set_rule(multiworld.get_location(f"{prefix} Card Draw 7", player), lambda state: state.has(f"{prefix} Beat Act 1 Boss", player))
    set_rule(multiworld.get_location(f"{prefix} Card Draw 8", player), lambda state: state.has(f"{prefix} Beat Act 1 Boss", player) and
                                                                                     state._spire_has_cards(player, prefix, 6) and state._spire_has_relics(player, prefix, 3))
    set_rule(multiworld.get_location(f"{prefix} Card Draw 9", player), lambda state: state.has(f"{prefix} Beat Act 1 Boss", player) and
                                                                                     state._spire_has_cards(player, prefix, 6) and state._spire_has_relics(player, prefix, 4))
    set_rule(multiworld.get_location(f"{prefix} Card Draw 10", player), lambda state: state.has(f"{prefix} Beat Act 1 Boss", player) and
                                                                                      state._spire_has_cards(player, prefix, 7) and state._spire_has_relics(player, prefix, 4))

    # Act 2 Relics
    set_rule(multiworld.get_location(f"{prefix} Relic 4", player), lambda state: state.has(f"{prefix} Beat Act 1 Boss", player) and
                                                                                 state._spire_has_cards(player, prefix, 7) and state._spire_has_relics(player, prefix, 2))
    set_rule(multiworld.get_location(f"{prefix} Relic 5", player), lambda state: state.has(f"{prefix} Beat Act 1 Boss", player) and
                                                                                 state._spire_has_cards(player, prefix, 7) and state._spire_has_relics(player, prefix, 2))
    set_rule(multiworld.get_location(f"{prefix} Relic 6", player), lambda state: state.has(f"{prefix} Beat Act 1 Boss", player) and
                                                                                 state._spire_has_cards(player, prefix, 7) and state._spire_has_relics(player, prefix, 3))

    set_rule(multiworld.get_entrance(f"{prefix} Mid Act 2", player), lambda state: state._spire_has_cards(player, prefix, 6) and
                                                                                   state._spire_has_relics(player, prefix, 2))

    set_rule(multiworld.get_entrance(f"{prefix} Late Act 2", player), lambda state: state._spire_has_cards(player, prefix, 6) and
                                                                                    state._spire_has_relics(player, prefix, 3))

    # Act 2 Boss Event
    set_rule(multiworld.get_entrance(f"{prefix} Act 2 Boss Arena", player), lambda state: state.has(f"{prefix} Beat Act 1 Boss", player) and state._spire_has_cards(player, prefix, 7) and state._spire_has_relics(player, prefix, 4) and state.has(f"{prefix} Boss Relic", player))

    # Act 2 Boss Rewards
    set_rule(multiworld.get_location(f"{prefix} Rare Card Draw 2", player), lambda state: state.has(f"{prefix} Beat Act 2 Boss", player))
    set_rule(multiworld.get_location(f"{prefix} Boss Relic 2", player), lambda state: state.has(f"{prefix} Beat Act 2 Boss", player))

    set_rule(multiworld.get_entrance(f"{prefix} Early Act 3", player), lambda state: state.has(f"{prefix} Beat Act 2 Boss", player))

    # Act 3 Card Draws
    set_rule(multiworld.get_location(f"{prefix} Card Draw 11", player), lambda state: state.has(f"{prefix} Beat Act 2 Boss", player))
    set_rule(multiworld.get_location(f"{prefix} Card Draw 12", player), lambda state: state.has(f"{prefix} Beat Act 2 Boss", player))
    set_rule(multiworld.get_location(f"{prefix} Card Draw 13", player), lambda state: state.has(f"{prefix} Beat Act 2 Boss", player) and state._spire_has_relics(player, prefix, 4))
    set_rule(multiworld.get_location(f"{prefix} Card Draw 14", player), lambda state: state.has(f"{prefix} Beat Act 2 Boss", player) and state._spire_has_relics(player, prefix, 4))
    set_rule(multiworld.get_location(f"{prefix} Card Draw 15", player), lambda state: state.has(f"{prefix} Beat Act 2 Boss", player) and state._spire_has_relics(player, prefix, 4))

    # Act 3 Relics
    set_rule(multiworld.get_location(f"{prefix} Relic 7", player), lambda state: state.has(f"{prefix} Beat Act 2 Boss", player) and state._spire_has_relics(player, prefix, 4))
    set_rule(multiworld.get_location(f"{prefix} Relic 8", player), lambda state: state.has(f"{prefix} Beat Act 2 Boss", player) and state._spire_has_relics(player, prefix, 5))
    set_rule(multiworld.get_location(f"{prefix} Relic 9", player), lambda state: state.has(f"{prefix} Beat Act 2 Boss", player) and state._spire_has_relics(player, prefix, 5))
    set_rule(multiworld.get_location(f"{prefix} Relic 10", player), lambda state: state.has(f"{prefix} Beat Act 2 Boss", player) and state._spire_has_relics(player, prefix, 5))

    set_rule(multiworld.get_entrance(f"{prefix} Mid Act 3", player), lambda state: state._spire_has_relics(player, prefix, 4))

    # Act 3 Boss Event
    set_rule(multiworld.get_entrance(f"{prefix} Act 3 Boss Arena", player), lambda state: state.has(f"{prefix} Beat Act 2 Boss", player) and state._spire_has_relics(player, prefix, 7) and state.has(f"{prefix} Boss Relic", player, 2))

    set_rule(multiworld.get_entrance(f"{prefix} Act 4", player), lambda state: state.has(f"{prefix} Beat Act 3 Boss", player))
