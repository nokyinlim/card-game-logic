from typing import Any, Dict, List

from character import StatModifier, Character, Ability, Spell, Equipment
import defaults

new_character = Character(
    name = "Character",
    character_class = "Class",
    team = "Team",
    element = "Element",
    base_stats = {
        "health": 100,
        "max_health": 100,
        "mp": 30,
        "max_mp": 30,
        "spell_damage": 30,
        "attack_damage": 30,
        "critical_chance": 0.3,
        "defense": 30,
        "magic_defense": 30,
        "skill_points": 30,
        "max_skill_points": 30,
        "accuracy": 100,
        "agility": 30
    },
    stat_modifiers = [],
    activeEffects = [],
    effects = [],
    abilities = [],
    spells = [],
    passives="character",
    equipment=[],
    inventory=[],
    description="Character Description"
)

char_json = {
    "name": "Character",
    "character_class": "Class",
    "team": "",
    "element": "neutral",
    "base_stats": {
        "health": 100,
        "max_health": 100,
        "mp": 30,
        "max_mp": 30,
        "spell_damage": 30,
        "attack_damage": 30,
        "critical_chance": 0.3,
        "defense": 30,
        "magic_defense": 30,
        "skill_points": 30,
        "max_skill_points": 30,
        "accuracy": 100,
        "agility": 30
    },
    "stat_modifiers": [],
    "activeEffects": [],
    "effects": [],
    "abilities": [],
    "spells": [],
    "passives": "character",
    "equipment": [],
    "inventory": [],
    "description": "Character Description"
}

def onHit(char: Character, target: Character, damage: float, damage_type: str, element: str, critical: bool, ignore_armor: bool):
    
    pass

def onMissedHit(char: Character, target: Character, damage: float, damage_type: str, element: str, critical: bool, ignore_armor: bool):
    pass

def onKill(char: Character):
    pass

def onAbility(char: Character, ability: Ability, targets: List[Character] = None):
    pass

def onSpell(char: Character, spell: Spell, targets: List[Character] = None):
    pass

def onTakeDamage(character: Character, damager: Character, type: str, element: str, damage: float, critical: bool, ignore_armor: bool):
    pass

def onDeath(character: Character, killer: Character, type: str, element: str):
    pass

def onCritical(character: Character, damager: Character, didHit: bool):
    pass

def onBattleWon(character: Character, allies: List[Character], enemies: List[Character]):
    pass

def onBattleLost(character: Character, allies: List[Character], enemies: List[Character]):
    pass

def onBattleStart(character: Character, allies: List[Character], enemies: List[Character]):
    pass

def onDodge(character: Character, attacker: Character):
    pass

def onHeal(character: Character, healer: Character, heal_amount: float):
    pass

def onApplyModifier(character: Character, modifier: StatModifier, source: Character = None):
    pass

def onRemoveModifier(character: Character, modifier: StatModifier, source: Character = None):
    pass

def onTurnStart(character: Character):
    pass

def onTurnEnd(character: Character):
    pass

def onAllyDeath(character: Character, ally: Character, killer: Character):
    pass

def onEnemyDeath(character: Character, enemy: Character, killer: Character):
    pass

def beforeAttack(damage_amount: float, char: Character, target: Character, type: str, element: str, critical: bool, ignore_armor: bool, didHit: bool) -> Dict[str, Any]:
    print("Damage will be added by 20!")
    return {"damage": damage_amount + 20, "ignore_armor": ignore_armor, "critical": critical, "didHit": didHit}

def beforeHeal():
    pass

def beforeDamage():
    return 50

passives = {
    "onHit": onHit,
    "onMissedHit": onMissedHit,
    "onKill": onKill,
    "onAbility": onAbility,
    "onSpell": onSpell,
    "onTakeDamage": onTakeDamage,
    "onDeath": onDeath,
    "onCritical": onCritical,
    "onBattleWon": onBattleWon,
    "onBattleLost": onBattleLost,
    "onBattleStart": onBattleStart,
    "onDodge": onDodge,
    "onHeal": onHeal,
    "onApplyModifier": onApplyModifier,
    "onRemoveModifier": onRemoveModifier,
    "onTurnStart": onTurnStart,
    "onTurnEnd": onTurnEnd,
    "onAllyDeath": onAllyDeath,
    "onEnemyDeath": onEnemyDeath,
    "beforeAttack": beforeAttack,
    "beforeHeal": beforeHeal,
    "beforeDamage": beforeDamage
}
