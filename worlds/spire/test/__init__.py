import typing

from test.bases import WorldTestBase
from worlds.spire import SpireWorld


class SpireTestBase(WorldTestBase):
    game = 'Slay the Spire'
    world = SpireWorld
    prefix: typing.ClassVar[str] = "Silent"

    options = {

        'character': 1,
        'final_act': 1
    }

