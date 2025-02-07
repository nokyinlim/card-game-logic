from typing import List

from character import StatModifier, Character, Ability, Spell, Equipment
import defaults

new_character = Character(
    name = "Character",
    character_class = "Class",
    team = "Team",
    element = "Element",
    base_stats = {
        "health": 0,
        "max_health": 0,
        "mp": 0,
        "max_mp": 0,
        "spell_damage": 0,
        "attack_damage": 0,
        "critical_chance": 0,
        "defense": 0,
        "magic_defense": 0,
        "skill_points": 0,
        "max_skill_points": 0,
        "accuracy": 0,
        "agility": 0
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

def onHit(char: Character, target: Character):
    pass

def onMissedHit(char: Character, target: Character):
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
