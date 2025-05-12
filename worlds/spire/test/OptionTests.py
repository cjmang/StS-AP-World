from worlds.spire.Options import CharacterOptions
from worlds.spire.test import SpireTestBase


class TestDefault(SpireTestBase):

    def test_validate_default(self):
        world = self.world
        self.assertEquals(1,len(world.options.characters))
        CharacterOptions.schema.validate(world.options.characters.value)

class TestMultiCharsValid(SpireTestBase):

    options = {
        "characters": {
            "the_ironclad": {
                "ascension": 1
            },
            "the_silent": {
                "final_act": True
            }
        }
    }

    def test_valid(self):
        CharacterOptions.schema.validate(self.world.options.characters.value)
