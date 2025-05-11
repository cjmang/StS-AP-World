from typing import TYPE_CHECKING, List, Union

from BaseClasses import Region

if TYPE_CHECKING:
    from . import SpireWorld


def create_regions(world: 'SpireWorld', player: int):
    from . import create_region

    multiworld = world.multiworld

    menu = create_region(multiworld, player, None, 'Menu', None)
    multiworld.regions.append(menu)
    neow = create_region(multiworld, player, None, "Neow's Room", None )
    multiworld.regions.append(neow)
    menu.connect(neow)
    # multiworld.regions.append(create_region(multiworld, player, "Neow's Room", None, ["Early Act 1"]))
    _create_regions(world, player, world.options.character.value, neow)

    # link up our region with the entrance we just made
    # multiworld.get_entrance("Neow's Room", player).connect(multiworld.get_region('Early Act 1', player))
    for region in multiworld.get_regions(player):
        if region.name == 'Menu' or region.name == "Neow's Room":
            continue
        entrance = world.get_entrance(region.name)
        entrance.connect(region)


def _create_regions(world: 'SpireWorld', player: int, character: Union[str,int], neow: Region):
    from . import create_region, character_list
    # TODO: prefix here needs to include index of custom character
    prefix = character_list[character] if type(character) == int else "Custom Character 1"
    multiworld = world.multiworld
    first_char_region  =create_region(multiworld, player, prefix, 'Early Act 1',
                                            [
                                                "Card Draw 1",
                                                "Card Draw 2",
                                                "Card Draw 3",
                                                *_create_floor_check(1,5)
                                            ],
                                            ["Mid Act 1"])
    neow.connect(first_char_region, first_char_region.name)
    multiworld.regions.append(first_char_region)

    multiworld.regions.append(create_region(multiworld, player, prefix, 'Mid Act 1',
                                            [
                                                'Card Draw 4',
                                                'Card Draw 5',
                                                'Relic 1',
                                                'Relic 2',
                                                *_create_floor_check(6, 10)
                                            ],["Late Act 1"]))

    multiworld.regions.append(create_region(multiworld, player, prefix, 'Late Act 1',
                                            [
                                                'Relic 3',
                                                *_create_floor_check(11, 15)
                                            ], ['Act 1 Boss Arena']))

    multiworld.regions.append(create_region(multiworld, player, prefix, 'Act 1 Boss Arena',
                                            [
                                                'Act 1 Boss',
                                                'Rare Card Draw 1',
                                                'Boss Relic 1',
                                                * _create_floor_check(16, 17)
                                            ], ['Early Act 2']))

    multiworld.regions.append(create_region(multiworld, player, prefix, 'Early Act 2',
                                            [
                                                "Card Draw 6",
                                                "Card Draw 7",
                                                *_create_floor_check(18, 22)
                                            ], ["Mid Act 2"]))

    multiworld.regions.append(create_region(multiworld, player, prefix, 'Mid Act 2',
                                            [
                                                'Card Draw 8',
                                                'Relic 4',
                                                'Relic 5',
                                                * _create_floor_check(23, 27)
                                            ], ["Late Act 2"]))

    multiworld.regions.append(create_region(multiworld, player, prefix, 'Late Act 2',
                                            [
                                                'Card Draw 9',
                                                'Card Draw 10',
                                                'Relic 6',
                                                *_create_floor_check(28, 32),
                                            ], ['Act 2 Boss Arena']))

    multiworld.regions.append(create_region(multiworld, player, prefix, 'Act 2 Boss Arena',
                                            [
                                                'Act 2 Boss',
                                                'Rare Card Draw 2',
                                                'Boss Relic 2',
                                                *_create_floor_check(33, 34),
                                            ], ['Early Act 3']))

    multiworld.regions.append(create_region(multiworld, player, prefix, 'Early Act 3',
                                            [
                                                "Card Draw 11",
                                                "Card Draw 12",
                                                *_create_floor_check(35, 39),
                                            ], ["Mid Act 3"]))

    multiworld.regions.append(create_region(multiworld, player, prefix, 'Mid Act 3',
                                            [
                                                "Card Draw 13",
                                                "Relic 7",
                                                "Relic 8",
                                                *_create_floor_check(40, 44),
                                            ], ["Late Act 3"]))

    multiworld.regions.append(create_region(multiworld, player, prefix, 'Late Act 3',
                                            [
                                                "Card Draw 14",
                                                "Card Draw 15",
                                                "Relic 9",
                                                "Relic 10",
                                                *_create_floor_check(45, 49),
                                            ], ['Act 3 Boss Arena']))

    acension_mod = 1 if world.options.ascension >= 20 else 0

    multiworld.regions.append(create_region(multiworld, player, prefix, 'Act 3 Boss Arena',
                                            [
                                                "Act 3 Boss",
                                                *_create_floor_check(50, 51 + acension_mod),
                                            ], ["Act 4"]))

    multiworld.regions.append(create_region(multiworld, player, prefix, 'Act 4',
                                            [
                                                "Heart Room",
                                                *(_create_floor_check(52 + acension_mod,55 + acension_mod) if world.options.final_act else [])
                                            ]))


def _create_floor_check(start: int, end: int) -> List[str]:
    return [f"Reached Floor {i}" for i in range(start, end + 1)]
