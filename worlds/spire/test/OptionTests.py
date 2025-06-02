from worlds.spire.Options import CharacterOptions
from worlds.spire.test import SpireTestBase


class TestDefault(SpireTestBase):

    def test_validate_default(self):
        world = self.world
        self.assertEquals(1, len(world.options.advanced_characters))
        CharacterOptions.schema.validate(world.options.advanced_characters.value)

class TestMultiCharsValid(SpireTestBase):

    options = {
        "character": [
            "ironclad",
            "silent",
        ]
    }

    def test_valid(self):
        CharacterOptions.schema.validate(self.world.options.advanced_characters.value)

class TestAdvancedMultiCharsValid(SpireTestBase):

    options = {
        "use_advanced_characters": 1,
        "advanced_characters": {
            "ironclad": {
                "ascension": 1
            },
            "silent": {
                "final_act": 1
            }
        }
    }

    def test_valid(self):
        CharacterOptions.schema.validate(self.world.options.advanced_characters.value)

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

class TestNoCharLocked(SpireTestBase):

    def no_items(self):
        for item in self.world.multiworld.get_items():
            self.assertFalse("Unlock" in item.name)


    def no_locations(self):
        for loc in self.world.get_locations():
            self.assertFalse("Press Start" in loc.name)

class TestAcension20(SpireTestBase):
    options = {
        "use_advanced_characters": 1,
        "advanced_characters": {
            "foobar": {
                "ascension": 20,
            },
            "barfoo": {
                "ascension": 20,
            }
        }
    }

class TestCharLocked(SpireTestBase):

    options = {
        "character": "the_ironclad",
        "use_advanced_characters": 1,
        "lock_characters": 2,
        "unlocked_character": "ironclad",
        "advanced_characters": {
            "ironclad": {
                "ascension": 1
            },
            "silent": {
                "final_act": 1
            }
        }
    }

    def test_silent_locked(self):
        self.assertTrue("Silent Unlock" in [ i.name for i in self.world.multiworld.get_items()])
        start = self.world.get_location("Silent Press Start")
        self.assertTrue( start is not None)
        state = self.multiworld.state.copy()
        self.assertFalse(start.can_reach(state))
        state.collect(self.get_item_by_name("Silent Unlock"))
        self.assertTrue(start.can_reach(state))

