from character import Character, Spell, Ability, StatModifier
from typing import List

def mageOnKill(char: Character):
    pass

def mageOnHit(char: Character, target: Character):
    pass

def mageOnMissedHit(char: Character, target: Character):
    pass

@PendingDeprecationWarning
def mageOnDamage(char: Character, target: Character):
    pass

def mageOnAbility(char: Character, ability: Ability, targets: List[Character] = None):
    pass

def mageOnSpell(char: Character, spell: Spell, targets: List[Character] = None):
    pass

def mageOnTakeDamage(character: Character, damager: Character, type: str, element: str, damage: float, critical: bool, ignore_armor: bool):
    pass

def mageOnDeath(character: Character, killer: Character, type: str, element: str):
    pass

def mageOnCritical(character: Character, damager: Character, didHit: bool):
    pass

def mageOnBattleWon(character: Character, allies: List[Character], enemies: List[Character]):
    pass

def mageOnBattleLost(character: Character, allies: List[Character], enemies: List[Character]):
    pass

def mageOnBattleStart(character: Character, allies: List[Character], enemies: List[Character]):
    pass

def mageOnDodge(character: Character, attacker: Character):
    pass

def mageOnHeal(character: Character, healer: Character, heal_amount: float):
    pass

def mageOnApplyModifier(character: Character, modifier: StatModifier, source: Character = None):
    pass

def mageOnRemoveModifier(character: Character, modifier: StatModifier, source: Character = None):
    pass

def mageOnTurnStart(character: Character):
    pass

def mageOnTurnEnd(character: Character):
    pass

def mageOnAllyDeath(character: Character, ally: Character, killer: Character):
    pass

def mageOnEnemyDeath(character: Character, enemy: Character, killer: Character):
    pass