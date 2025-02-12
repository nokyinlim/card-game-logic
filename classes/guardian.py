from typing import List
from character import StatModifier, Character, Ability, Spell
import defaults
# from shared_game_data import characters, playerCharacters
import shared_game_data 

# Abilities

guardianStunBash = Ability(
    name = "Stun Bash",
    lore = "A powerful strike with the shield dealing Earth damage and",
    info = "stunning the enemy, stopping their attack for one turn.",
    cost = 3,
    effect = [],
    type = "damage",
    damage = {
        "damage": 30,
        "element": "earth",
        "targets": ""
    }
)

guardianFortifiedStrike = Ability(
    name = "[Ult] Fortified Strike",
    lore = "The Guardian channels their inner Fortitude, enlightening them to transform their shield",
    info = "into a sword's embrace, where every guard becomes a strike of grace...",
    cost = 8,
    effect = [],
    type = "damage",
    damage = {
        "damage": 60,
        "element": "light",
        "targets": ""
    }
)

guardianUnyieldingStance = Ability(
    name = "Unyielding Stance",
    lore = "The Guardian takes on a defensive stance, significantly reducing incoming damage and",
    info = "increases Fortitude gain for a short duration.",
    cost = 4,
    effect = [StatModifier(
        id = "unyielding_stance_fortitude",
        stat = "fortitude",
        value = 2,
        modifier_type = "turn",
        duration = 2,
        targetsSelf = True
    )],
    type = "modifier"
)



guardianCounterstrike = Ability(
    name = "Counterstrike",
    lore = "The Guardian prepares for an incoming attack. The next enemy targetting you deals significantly",
    info = "reduced damage and allowing the Guardian to retaliate with a powerful strike on the next hit.",
    cost = 4,
    effect = [StatModifier(
        id = "counterstrike_defense",
        stat = "defense",
        value = 2,
        modifier_type = "multiplicative",
        duration = 1,
        targetsSelf = True
    ), StatModifier(
        id = "counterstrike_magic_defense",
        stat = "magic_defense",
        value = 2,
        modifier_type = "multiplicative",
        duration = 1,
        targetsSelf = True
    )],
    type = "modifier"
)

guardianSelfHealing = Spell(
    name = "Self Healing",
    lore = "The Guardian emits a healing aura, restoring a small amount of health to the Guardian over time",
    info = "",
    mp_cost = 2,
    effects = [StatModifier(
        id = "guardianSelfHeal",
        stat = "health",
        value = 15,
        modifier_type = "turn",
        duration = 4,
        targetsSelf = True
    )],
    type = "modifier"
)

guardianAttractHit = Spell(
    name = "Attract Hit",
    lore = "Taunts all enemies, making them much more likely to target the Guardian for 4 turns.",
    info = "",
    mp_cost = 2,
    effects = [StatModifier(
        id = "guardianAttractHit",
        stat = "weight",
        value = 40,
        modifier_type="add",
        duration=4,
        targetsSelf=True
    )],
    type = "modifier"
)

guardianStoneSkin = Spell(
    name = "Stone Skin",
    lore = "Envelops the Guardian in a layer of stone, significantly increasing their physical resistance",
    info = "for a short time.",
    mp_cost = 3,
    effects=[StatModifier(
        id = "guardianStoneSkinDefense",
        stat = "defense",
        value = 1.5,
        modifier_type = "multiply_base",
        duration = 3,
        targetsSelf = True
    ), StatModifier(
        id = "guardianStoneSkinMagicDefense",
        stat = "magic_defense",
        value = 1.25,
        modifier_type = "multiply_base",
        duration=3,
        targetsSelf=True
    )],
    type = "modifier"
)



def guardianOnKill(char: Character):
    print(f"Fortitude Passive Activated:\nGains Fortitude upon killing a target")

def guardianOnHit(char: Character, target: Character, final_damage: float, damage_origin: str, element: str, critical: bool, ignore_armor: bool):
    # print(f"{char.name} hit {target.name}")
    # Implement effects related to being hit
    pass

def guardianOnMissedHit(char: Character, target: Character, final_damage: float, damage_origin: str, element: str, critical: bool, ignore_armor: bool):
    print(f"{char.name} missed {target.name}")
    # Implement effects related to missed hits
    pass

def guardianOnAbility(char: Character, ability: Ability, targets: List[Character] = None):
    # Implement effects related to ability usage
    pass

def guardianOnSpell(char: Character, spell: Spell, targets: List[Character] = None):
    # Implement effects related to spell usage
    pass

def guardianOnTakeDamage(character: Character, damager: Character, type: str, element: str, damage: float, critical: bool, ignore_armor: bool):

    # Implement effects when the Guardian takes damage
    pass

def guardianOnDeath(character: Character, killer: Character, type: str, element: str):
    print(f"{character.name} has fallen in battle!")
    # Implement effects upon Guardian's death
    
    pass

def guardianOnCritical(character: Character, damager: Character, didHit: bool):
    print("Critical Hit!")
    pass

def guardianOnBattleWon(character: Character, allies: List[Character], enemies: List[Character]):
    print("Guardian has won the battle!")
    pass

def guardianOnBattleLost(character: Character, allies: List[Character], enemies: List[Character]):
    print("Guardian has fallen in battle.")
    pass

def guardianOnBattleStart(character: Character, allies: List[Character], enemies: List[Character]):
    print("The Guardian prepares to protect their allies.")
    pass

def guardianOnDodge(character: Character, attacker: Character):
    print(f"{character.name} dodged an attack from {attacker.name}!")
    pass

def guardianOnHeal(character: Character, healer: Character, heal_amount: float):
    print(f"{character.name} has been healed by {healer.name} for {heal_amount} HP.")
    pass

def guardianOnApplyModifier(character: Character, modifier: StatModifier, source: Character = None):
    print(f"{character.name} has received a modifier: {modifier.id}.")
    pass

def guardianOnRemoveModifier(character: Character, modifier: StatModifier, source: Character = None):
    print(f"{modifier.id} has been removed from {character.name}.")
    pass

def guardianOnTurnStart(character: Character):
    print(f"{character.name} begins their turn.")
    pass

def guardianOnTurnEnd(character: Character):
    print(f"{character.name} ends their turn.")
    pass

def guardianOnAllyDeath(character: Character, ally: Character, killer: Character):
    print(f"{character.name} mourns the loss of {ally.name}.")
    pass

def guardianOnEnemyDeath(character: Character, enemy: Character, killer: Character):
    print(f"{enemy.name} has been defeated by {killer.name}.")
    pass

def beforeDamage(damage_amount: float, character: Character, target: Character) -> float:
    return damage_amount

def beforeHeal(heal_amount: float, character: Character, target: Character) -> float:
    return heal_amount

def beforeAttack(damage_amount: float, character: Character, target: Character, type: str, element: str, critical: bool, ignore_armor: bool) -> float:
    return damage_amount

passives = {
    "onHit": guardianOnHit,
    "onMissedHit": guardianOnMissedHit,
    "onKill": guardianOnKill,
    "onAbility": guardianOnAbility,
    "onSpell": guardianOnSpell,
    "onTakeDamage": guardianOnTakeDamage,
    "onDeath": guardianOnDeath,
    "onCritical": guardianOnCritical,
    "onBattleWon": guardianOnBattleWon,
    "onBattleLost": guardianOnBattleLost,
    "onBattleStart": guardianOnBattleStart,
    "onDodge": guardianOnDodge,
    "onHeal": guardianOnHeal,
    "onApplyModifier": guardianOnApplyModifier,
    "onRemoveModifier": guardianOnRemoveModifier,
    "onTurnStart": guardianOnTurnStart,
    "onTurnEnd": guardianOnTurnEnd,
    "onAllyDeath": guardianOnAllyDeath,
    "onEnemyDeath": guardianOnEnemyDeath,
    "beforeDamage": beforeDamage,
    "beforeHeal": beforeHeal,
    "beforeAttack": beforeAttack
}


"""_defaultGuardian = Character(
    name = "Guardian",
    character_class = "Guardian",
    team = "player",
    element= "earth",
    base_stats={
        "health": 100,
        "max_health": 100,
        "mp": 20,
        "max_mp": 20,
        "attack_damage": 15,
        "critical_chance": 0.1,
        "defense": 30,
        "magic_defense": 30,
        "skill_points": 30,
        "max_skill_points": 30,
        "accuracy": 30,
        "agility": 5,
        "weight": 20,
    },
    stat_modifiers=[],
    activeEffects=[],
    passives={},
    abilities=[],
    spells=[],
    equipment=[],
    inventory=[]
)
"""