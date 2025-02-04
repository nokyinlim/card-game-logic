from typing import List
from character import StatModifier, Character, Ability, Spell, Equipment
import defaults
from shared_game_data import characters, playerCharacters 

def assassinOnKill(char: Character):
    print(f"Bloodlust Passive Activated:\nHeals HP upon killing a target")
    health = char.base_stats["health"]
    char.base_stats["health"] = health + 10

def assassinOnHit(char: Character, target: Character):

    print(f"{char.name} hit {target.name}")

    instance_list = char.stat_modifiers

    removal_property = "id"
    value_to_remove = "vanish_attack_bonus"

    # Remove the Vanish Attack Bonus
    char.stat_modifiers = defaults.remove_instance_with_property(instance_list, removal_property, value_to_remove)

    removal_property = "id"
    value_to_remove = "vanish_invisibility"

    instance_list = char.stat_modifiers

    # Remove the Vanish Invisibility
    char.stat_modifiers = defaults.remove_instance_with_property(instance_list, removal_property, value_to_remove)


    pass

def assassinOnMissedHit(char: Character, target: Character):

    print(f"{char.name} missed {target.name}")

    instance_list = char.stat_modifiers

    removal_property = "id"
    value_to_remove = "vanish_attack_bonus"

    # Remove the Vanish Attack Bonus
    char.stat_modifiers = defaults.remove_instance_with_property(instance_list, removal_property, value_to_remove)

    removal_property = "id"
    value_to_remove = "vanish_invisibility"

    instance_list = char.stat_modifiers

    # Remove the Vanish Invisibility
    char.stat_modifiers = defaults.remove_instance_with_property(instance_list, removal_property, value_to_remove)


    pass

@DeprecationWarning
def assassinOnDamage(char: Character, target: Character):
    print(f"Assassin is damaging a target")

def assassinOnAbility(char: Character, ability: Ability, targets: List[Character] = None):
    instance_list = char.stat_modifiers

    removal_property = "id"
    value_to_remove = "vanish_attack_bonus"

    # Remove the Vanish Attack Bonus
    char.stat_modifiers = defaults.remove_instance_with_property(instance_list, removal_property, value_to_remove)

    removal_property = "id"
    value_to_remove = "vanish_invisibility"

    instance_list = char.stat_modifiers

    # Remove the Vanish Invisibility
    char.stat_modifiers = defaults.remove_instance_with_property(instance_list, removal_property, value_to_remove)



def assassinOnSpell(char: Character, spell: Spell, targets: List[Character] = None):
    if spell == assassinSummonClone:
        print("Summoning Clone")
        global characters, playerCharacters
        characters.insert(0, assassinCloneCharacter)
        print("A new Assassin has spawned!")
        pass
    pass

def assassinOnTakeDamage(character: Character, damager: Character, type: str, element: str, damage: float, critical: bool, ignore_armor: bool):
    pass

def assassinOnDeath(character: Character, killer: Character, type: str, element: str):
    pass

def assassinOnCritical(character: Character, damager: Character, didHit: bool):
    if didHit:
        print("Killer Instinct Passive Activated:\nRestores Mana when dealing a Critical Hit.")
        character.base_stats["mp"] += 5
    pass

def assassinOnBattleWon(character: Character, allies: List[Character], enemies: List[Character]):
    print("Assassin has won the battle!")
    pass

def assassinOnBattleLost(character: Character, allies: List[Character], enemies: List[Character]):
    pass

def assassinOnBattleStart(character: Character, allies: List[Character], enemies: List[Character]):
    pass

def assassinOnDodge(character: Character, attacker: Character):
    pass

def assassinOnHeal(character: Character, healer: Character, heal_amount: float):
    pass

def assassinOnApplyModifier(character: Character, modifier: StatModifier, source: Character = None):
    pass

def assassinOnRemoveModifier(character: Character, modifier: StatModifier, source: Character = None):
    pass

def assassinOnTurnStart(character: Character):
    pass

def assassinOnTurnEnd(character: Character):
    pass

def assassinOnAllyDeath(character: Character, ally: Character, killer: Character):
    pass

def assassinOnEnemyDeath(character: Character, enemy: Character, killer: Character):
    pass
