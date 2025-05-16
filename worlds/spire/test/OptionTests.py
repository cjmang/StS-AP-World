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

class TestCampfireSanity(SpireTestBase):

    options = {
        "campfire_sanity": 1
    }

    def test_locs(self):
        count = 0
        for loc in self.world.get_locations():
            if "Campfire" in loc.name:
                count += 1
        self.assertEquals(6, count)

    def test_no_rest(self):
        count = 0
        for item in self.world.multiworld.get_items():
            if "Rest" in item.name:
                    count += 1
        self.assertEquals(3, count)

    def test_no_smith(self):
        count = 0
        for item in self.world.multiworld.get_items():
            if "Smith" in item.name:
                count += 1
        self.assertEquals(3, count)

class TestNoCampfireSanity(SpireTestBase):

    def no_items(self):
        for item in self.world.multiworld.get_items():
            self.assertFalse("Campfire" in item.name)

    def no_locations(self):
        for loc in self.world.get_locations():
            self.assertFalse("Rest" in loc.name)
            self.assertFalse("Smith" in loc.name)

class TestNoShopSanity(SpireTestBase):

    def no_items(self):
        for item in self.world.multiworld.get_items():
            self.assertFalse("Shop" in item.name)

    def no_locations(self):
        for loc in self.world.get_locations():
            self.assertFalse("Shop" in loc.name)