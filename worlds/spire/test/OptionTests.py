from BaseClasses import CollectionState
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

class TestAcension20Final(SpireTestBase):
    options = {
        "character": {
            "Ironclad", "Defect"
        },
        "ascension": 20,
        "final_act": 1,
        "include_floor_checks": 1,
        "campfire_sanity":1,
        "shop_sanity":1,
    }


    def test_floor_56_has_address(self):
        self.assertEquals(56, self.multiworld.get_location("Ironclad Reached Floor 56", self.player).address)
        self.assertEquals((200*2)+56, self.multiworld.get_location("Defect Reached Floor 56", self.player).address)


class TestOfficialNamesRecognized(SpireTestBase):
    options = {
        "use_advanced_characters": 1,
        "advanced_characters": {
            "tHe_SnEcKo": {}
        }
    }

    def test_has_snecko_location(self):
        self.world.get_location("Snecko Reached Floor 1")


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
        state = CollectionState(self.multiworld)
        self.assertFalse(start.can_reach(state))
        state.collect(self.get_item_by_name("Silent Unlock"))
        self.assertTrue(start.can_reach(state))

class GoldSanityOff(SpireTestBase):

    def test_ensure_no_gold(self):
        locations = self.multiworld.get_unfilled_locations(self.player)
        self.assertTrue("Silent Combat Gold 1" not in locations)
        self.assertTrue("Silent Elite Gold 1" not in locations)
        self.assertTrue("Silent Boss Gold 1" not in locations)

class NoUnlockedChar(SpireTestBase):

    options = {
        "lock_characters": 0
    }

class PickTwoCharacters(SpireTestBase):
    options = {
        "character": {
            "Silent",
            "Ironclad",
            "Watcher",
            "Defect",
        },
        "pick_num_characters": 2
    }

    def test_has_two(self):
        self.assertEqual(2, len(self.world.characters))

class PickTwoAdvancedCharacters(SpireTestBase):
    options = {
        "use_advanced_characters": 1,
        "advanced_characters": {
            "Silent": {},
            "Ironclad": {},
            "Watcher": {},
            "Defect": {},
        },
        "pick_num_characters": 2
    }

    def test_has_two(self):
        self.assertEqual(2, len(self.world.characters))

class GoalWithTwoChars(SpireTestBase):

    options = {
        "character": {
            "Silent",
            "Ironclad",
            "Watcher",
            "Defect",
        },
        "num_chars_goal": 2
    }

    def test_goal_with_two(self):
        items = ["Ironclad Victory", "Watcher Victory"]
        state = CollectionState(self.multiworld)
        for name in items:
            item = self.get_item_by_name(name)
            state.collect(item)
        self.assertTrue(self.multiworld.completion_condition[self.player](state))

    def test_goal_with_three(self):
        items = ["Ironclad Victory", "Watcher Victory", "Defect Victory"]
        state = CollectionState(self.multiworld)
        for name in items:
            item = self.get_item_by_name(name)
            state.collect(item)
        self.assertTrue(self.multiworld.completion_condition[self.player](state))

    def test_goal_with_four(self):
        items = ["Ironclad Victory", "Watcher Victory", "Defect Victory", "Silent Victory"]
        state = CollectionState(self.multiworld)
        for name in items:
            item = self.get_item_by_name(name)
            state.collect(item)
        self.assertTrue(self.multiworld.completion_condition[self.player](state))

    def test_no_goal_with_one(self):
        items = ["Silent Victory"]
        state = CollectionState(self.multiworld)
        for name in items:
            item = self.get_item_by_name(name)
            state.collect(item)
        self.assertFalse(self.multiworld.completion_condition[self.player](state))

    def test_no_goal_with_nothing(self):
        state = CollectionState(self.multiworld)
        self.assertFalse(self.multiworld.completion_condition[self.player](state))

class GoalWithAllChars(SpireTestBase):

    options = {
        "character": {
            "Silent",
            "Ironclad",
            "Watcher",
            "Defect",
        },
        "num_chars_goal": 0
    }

    def test_no_goal_with_two(self):
        items = ["Ironclad Victory", "Watcher Victory"]
        state = CollectionState(self.multiworld)
        for name in items:
            item = self.get_item_by_name(name)
            state.collect(item)
        self.assertFalse(self.multiworld.completion_condition[self.player](state))

    def test_no_goal_with_three(self):
        items = ["Ironclad Victory", "Watcher Victory", "Defect Victory"]
        state = CollectionState(self.multiworld)
        for name in items:
            item = self.get_item_by_name(name)
            state.collect(item)
        self.assertFalse(self.multiworld.completion_condition[self.player](state))

    def test_goal_with_four(self):
        items = ["Ironclad Victory", "Watcher Victory", "Defect Victory", "Silent Victory"]
        state = CollectionState(self.multiworld)
        for name in items:
            item = self.get_item_by_name(name)
            state.collect(item)
        self.assertTrue(self.multiworld.completion_condition[self.player](state))

    def test_no_goal_with_one(self):
        items = ["Silent Victory"]
        state = CollectionState(self.multiworld)
        for name in items:
            item = self.get_item_by_name(name)
            state.collect(item)
        self.assertFalse(self.multiworld.completion_condition[self.player](state))

    def test_no_goal_with_nothing(self):
        state = CollectionState(self.multiworld)
        self.assertFalse(self.multiworld.completion_condition[self.player](state))
