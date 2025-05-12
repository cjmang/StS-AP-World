from typing import List, Optional, Any

from worlds.spire.Options import Character

NUM_CUSTOM = 5

character_list: List[str] = [
    "Ironclad",
    "Silent",
    "Defect",
    "Watcher",
    "Hermit",
    "Slime Boss",
    "Guardian",
    "Hexaghost",
    "Champ",
    "Gremlins",
    "Automaton",
    "Snecko",
]

official_names: List[str] = [
    "IRONCLAD",
    "THE_SILENT",
    "DEFECT",
    "WATCHER",
    "HERMIT",
    "SLIMEBOUND",
    "GUARDIAN",
    "THE_SPIRIT",
    "THE_CHAMP",
    "GREMLIN",
    "THE_AUTOMATON",
    "THE_SNECKO"
]

character_option_map = {
    value: key.lower()
    for key, value in Character.options.items() if key != "spire_take_the_wheel"
}

character_offset_map = {
    value: key
    for key, value in character_option_map.items()
}

class CharacterConfig:
    # name: str
    # option_name: str
    # official_name: str
    # char_offset: int
    # mod_num: int
    # ascension: int
    # final_act: bool
    # downfall: bool

    def __init__(self, name: str, option_name: str, char_offset: int, mod_num: int, **kwargs):
        self.name: str = name
        self.option_name: str = option_name
        self.char_offset: int = char_offset
        self.mod_num: int = mod_num
        if self.mod_num > 0:
            self.official_name: str = self.option_name
        else:
            self.official_name: str = official_names[char_offset]
        self.ascension: int = kwargs['ascension']
        self.final_act: bool = kwargs['final_act']
        self.downfall: bool = kwargs['downfall']

    def to_dict(self) -> dict[str, Any]:
        return {
            'name': self.name,
            'option_name': self.option_name,
            'char_offset': self.char_offset,
            'official_name': self.official_name,
            'mod_num': self.mod_num,
            'ascension': self.ascension,
            'final_act': self.final_act,
            'downfall': self.downfall,
        }

    def __repr__(self):
        return self.to_dict().__repr__()
