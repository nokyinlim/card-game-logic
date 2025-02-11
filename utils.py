from models import PydanticCharacter
from character import Ability, Card, Character, Spell, StatModifier
import json


def pydantic_to_character(pydantic_char: PydanticCharacter) -> Character:
    # Convert stat modifiers
    stat_modifiers = [
        StatModifier(
            id=mod.get('id', ''),
            stat=mod.get('stat', ''),
            value=mod.get('value', 0),
            modifier_type=mod.get('modifier_type', ''),
            duration=mod.get('duration'),
            targetsSelf=mod.get('targetsSelf', True),
            applyer=mod.get('applyer'),
            displayName=mod.get('displayName', '')
        ) for mod in pydantic_char.stat_modifiers
    ]

    # Convert abilities
    abilities = [
        Ability(
            name=ability.get('name', ''),
            lore=ability.get('lore', ''),
            info=ability.get('info', ''),
            cost=ability.get('cost', 0),
            effect=[StatModifier(
                id=effect.get('id', ''),
                stat=effect.get('stat', ''),
                value=effect.get('value', 0),
                modifier_type=effect.get('modifier_type', ''),
                duration=effect.get('duration'),
                targetsSelf=effect.get('targetsSelf', True),
                applyer=effect.get('applyer'),
                displayName=effect.get('displayName', '')
            ) for effect in ability.get('effect', [])],
            type=ability.get('type', ''),
            damage=ability.get('damage', {'damage': 0, 'element': '', 'targets': ''}),
            cooldown=ability.get('cooldown', 0)
        ) for ability in pydantic_char.abilities
    ]

    # Convert spells
    spells = [
        Spell(
            name=spell.get('name', ''),
            lore=spell.get('lore', ''),
            info=spell.get('info', ''),
            mp_cost=spell.get('mp_cost', 0),
            effects=[StatModifier(
                id=effect.get('id', ''),
                stat=effect.get('stat', ''),
                value=effect.get('value', 0),
                modifier_type=effect.get('modifier_type', ''),
                duration=effect.get('duration'),
                targetsSelf=effect.get('targetsSelf', True),
                applyer=effect.get('applyer'),
                displayName=effect.get('displayName', '')
            ) for effect in spell.get('effects', [])],
            type=spell.get('type', ''),
            damage=spell.get('damage', {'damage': 0, 'element': '', 'targets': ''}),
            cooldown=spell.get('cooldown', 0)
        ) for spell in pydantic_char.spells
    ]

    # Convert active effects
    active_effects = [
        StatModifier(
            id=effect.get('id', ''),
            stat=effect.get('stat', ''),
            value=effect.get('value', 0),
            modifier_type=effect.get('modifier_type', ''),
            duration=effect.get('duration'),
            targetsSelf=effect.get('targetsSelf', True),
            applyer=effect.get('applyer'),
            displayName=effect.get('displayName', '')
        ) for effect in pydantic_char.activeEffects
    ]

    # Convert inventory cards
    inventory = [
        Card(
            type=card.get('type', ''),
            name=card.get('name', ''),
            data=card.get('data', {})
        ) for card in pydantic_char.inventory
    ]

    # Create and return Character
    return Character(
        name=pydantic_char.name,
        character_class=pydantic_char.character_class,
        team=pydantic_char.team,
        element=pydantic_char.element,
        base_stats=pydantic_char.base_stats,
        character_data=pydantic_char.character_data,
        stat_modifiers=stat_modifiers,
        activeEffects=active_effects,
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

def dictionary_to_character(char_dict: dict) -> Character:
    """
    :param char_dict: A dictionary containing the character's data

    :return: A Character object created from the dictionary
    """
    # example input
    """{'name': 'Armored Sentinel', 'character_class': 'Knight', 'team': 'string', 'element': 'fire', 'base_stats': {'health': 140, 'max_health': 140, 'mp': 10, 'max_mp': 10, 'attack_damage': 45, 'spell_damage': 10, 'critical_chance': 0.1, 'defense': 30, 'magic_defense': 5, 'skill_points': 24, 'max_skill_points': 24, 'accuracy': 60, 'agility': 10}, 'stat_modifiers': [], 'activeEffects': [], 'effects': [], 'abilities': [{'name': 'Self Defense', 'lore': 'Increases defense for a short time', 'info': '', 'cost': 8, 'effect': [{'id': 'self_defense', 'stat': 'defense', 'value': 1.5, 'modifier_type': 'multiply_base', 'duration': 2, 'targetsSelf': True, 'applyer': None, 'displayName': 'Self Defense Power Up'}, {'id': 'self_magic_defense', 'stat': 'defense', 'value': 1.5, 'modifier_type': 'multiply_base', 'duration': 2, 'targetsSelf': True, 'applyer': None, 'displayName': 'Self Magic Defense Power Up'}], 'type': 'modifier', 'damage': None, 'cooldown': 0}], 'spells': [{'name': 'Self Healing', 'lore': 'Heals the user for a small amount each turn, for 4 turns', 'info': '', 'mp_cost': 5, 'effects': [{'id': 'self_healing', 'stat': 'health', 'value': 20, 'modifier_type': 'turn', 'duration': 4, 'targetsSelf': True, 'applyer': None, 'displayName': 'Continuous Health Increase'}], 'type': 'modifier', 'damage': {}, 'cooldown': 0}], 'passives': 'guardian', 'equipment': [], 'inventory': [], 'active_modifiers': [], 'turns': 0, 'description': ''}"""
    return Character(
        name=char_dict.get('name', ''),
        character_class=char_dict.get('character_class', ''),
        team=char_dict.get('team', ''),
        element=char_dict.get('element', ''),
        base_stats=char_dict.get('base_stats', {}),
        character_data=char_dict.get('character_data', {}),
        stat_modifiers=char_dict.get('stat_modifiers', []),
        activeEffects=[StatModifier(
            id=effect.get('id', ''),
            stat=effect.get('stat', ''),
            value=effect.get('value', 0),
            modifier_type=effect.get('modifier_type', ''),
            duration=effect.get('duration'),
            targetsSelf=effect.get('targetsSelf', True),
            applyer=effect.get('applyer'),
            displayName=effect.get('displayName', '')
        ) for effect in char_dict.get('activeEffects', [])],
        effects=char_dict.get('effects', []),
        abilities=[Ability(
            name=ability.get('name', ''),
            lore=ability.get('lore', ''),
            info=ability.get('info', ''),
            cost=ability.get('cost', 0),
            effect=[StatModifier(
                id=effect.get('id', ''),
                stat=effect.get('stat', ''),
                value=effect.get('value', 0),
                modifier_type=effect.get('modifier_type', ''),
                duration=effect.get('duration'),
                targetsSelf=effect.get('targetsSelf', True),
                applyer=effect.get('applyer'),
                displayName=effect.get('displayName', '')
            ) for effect in ability.get('effect', [])],
            type=ability.get('type', ''),
            damage=ability.get('damage', {'damage': 0, 'element': '', 'targets': ''}),
            cooldown=ability.get('cooldown', 0)
        ) for ability in char_dict.get('abilities', [])],
        spells=[Spell(
            name=spell.get('name', ''),
            lore=spell.get('lore', ''),
            info=spell.get('info', ''),
            mp_cost=spell.get('mp_cost', 0),
            effects=[StatModifier(
                id=effect.get('id', ''),
                stat=effect.get('stat', ''),
                value=effect.get('value', 0),
                modifier_type=effect.get('modifier_type', ''),
                duration=effect.get('duration'),
                targetsSelf=effect.get('targetsSelf', True),
                applyer=effect.get('applyer'),
                displayName=effect.get('displayName', '')
            ) for effect in spell.get('effects', [])],
            type=spell.get('type', ''),
            damage=spell.get('damage', {'damage': 0, 'element': '', 'targets': ''}),
            cooldown=spell.get('cooldown', 0)
        ) for spell in char_dict.get('spells', [])],
        passives=char_dict.get('passives', ''),
        equipment=char_dict.get('equipment', []),
        inventory=char_dict.get('inventory', []),
        description=char_dict.get('description', '')
    )

def getCharacterFromDict(dictionary: dict):
    print(dictionary)
    print(PydanticCharacter(**dictionary))
    return pydantic_to_character(PydanticCharacter(**dictionary))




def getDefaultCharacterFromStr(char_name: str, convert_to_character: bool = False) -> any:
    with open("characters.json", "r") as file:
        try:
            json_obj = json.load(file)[char_name]
        except:
            print("invalid character name")
            return None
        file.close()
    return dictionary_to_character(json_obj) if convert_to_character else json_obj