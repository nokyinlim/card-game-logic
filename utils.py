

from models import PydanticCharacter
from character import Ability, Card, Character, Spell, StatModifier
import json


def pydantic_to_character(pydantic_char: PydanticCharacter) -> Character:
    # Convert stat modifiers to StatModifier objects
    stat_modifiers = []
    for mod in pydantic_char.stat_modifiers:
        stat_modifier = StatModifier(
            id=mod.get('id', ''),
            stat=mod.get('stat', ''),
            value=mod.get('value', 0),
            modifier_type=mod.get('modifier_type', ''),
            duration=mod.get('duration'),
            targetsSelf=mod.get('targetsSelf', True),
            applyer=mod.get('applyer'),
            displayName=mod.get('displayName', '')
        )
        stat_modifiers.append(stat_modifier)

    # Convert abilities to Ability objects
    abilities = []
    for ability in pydantic_char.abilities:
        # Convert effects for each ability
        ability_effects = []
        for effect in ability.get('effect', []):
            effect_mod = StatModifier(
                id=effect.get('id', ''),
                stat=effect.get('stat', ''),
                value=effect.get('value', 0),
                modifier_type=effect.get('modifier_type', ''),
                duration=effect.get('duration'),
                targetsSelf=effect.get('targetsSelf', True),
                applyer=effect.get('applyer'),
                displayName=effect.get('displayName', '')
            )
            ability_effects.append(effect_mod)

        abilities.append(Ability(
            name=ability.get('name', ''),
            lore=ability.get('lore', ''),
            info=ability.get('info', ''),
            cost=ability.get('cost', 0),
            effect=ability_effects,
            type=ability.get('type', ''),
            damage=ability.get('damage', {'damage': 0, 'element': '', 'targets': ''}),
            cooldown=ability.get('cooldown', 0)
        ))

    # Convert spells to Spell objects
    spells = []
    for spell in pydantic_char.spells:
        # Convert effects for each spell
        spell_effects = []
        for effect in spell.get('effects', []):
            effect_mod = StatModifier(
                id=effect.get('id', ''),
                stat=effect.get('stat', ''),
                value=effect.get('value', 0),
                modifier_type=effect.get('modifier_type', ''),
                duration=effect.get('duration'),
                targetsSelf=effect.get('targetsSelf', True),
                applyer=effect.get('applyer'),
                displayName=effect.get('displayName', '')
            )
            spell_effects.append(effect_mod)

        spells.append(Spell(
            name=spell.get('name', ''),
            lore=spell.get('lore', ''),
            info=spell.get('info', ''),
            mp_cost=spell.get('mp_cost', 0),
            effects=spell_effects,
            type=spell.get('type', ''),
            damage=spell.get('damage', {'damage': 0, 'element': '', 'targets': ''}),
            cooldown=spell.get('cooldown', 0)
        ))

    inventory = []

    for card in pydantic_char.inventory:
        inventory.append(Card(
            type = card.get('type', ''),
            name = card.get('name', ''),
            data = card.get('data', {})
        ))

    # Create and return the Character object
    return Character(
        name=pydantic_char.name,
        character_class=pydantic_char.character_class,
        team=pydantic_char.team,
        element=pydantic_char.element,
        base_stats=pydantic_char.base_stats,
        stat_modifiers=stat_modifiers,
        activeEffects=pydantic_char.activeEffects,
        effects=pydantic_char.effects,
        abilities=abilities,
        spells=spells,
        passives=pydantic_char.passives,
        equipment=pydantic_char.equipment,
        inventory=inventory,
        description=pydantic_char.description
    )


def readGames() -> dict[str, dict[str, list]]:
    with open("games.json", "r") as file:
        json_object = json.load(file)
        file.close()
    return json_object

def writeGames(games: dict[str, dict[str, list[Character]]]):
    json_object = json.dumps(games)
    with open("games.json", "w") as file:
        file.write(json_object)
        file.close()



def getCharacterFromDict(dict):
    return pydantic_to_character(PydanticCharacter(**dict))


def getDefaultCharacterFromStr(char_name: str, convert_to_character: bool = False) -> any:
    with open("characters.json", "r") as file:
        try:
            json_obj = json.load(file)[char_name]
        except:
            print("invalid character name")
            return None
        file.close()
    return getCharacterFromDict(json_obj) if convert_to_character else json_obj