from worlds.spire.Options import CharacterOptions
from worlds.spire.test import SpireTestBase


class TestDefault(SpireTestBase):

    def test_validate_default(self):
        world = self.world
        self.assertEquals(1,len(world.options.characters))
        CharacterOptions.schema.validate(world.options.characters.value)

class TestMultiCharsValid(SpireTestBase):

    options = {
        "multi_char": 1,
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

class TestNoFloorChecks(SpireTestBase):

    options = {
        "include_floor_checks": 0
    }

    def test_no_floors(self):
        for loc in self.world.get_locations():
            self.assertFalse("Reached" in loc.name, loc.name)
