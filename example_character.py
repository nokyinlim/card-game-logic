
from typing import List
from character import StatModifier, Character, Ability, Spell, Equipment
import defaults
# from shared_game_data import characters, playerCharacters
# import shared_game_data 
import json




def celestialSeerOnKill(char: Character):
    print(f"Fortitude Passive Activated:\nGains Fortitude upon killing a target")
    # Implement the passive effect for the celestialSeer on kill
    char.base_stats["fortitude"] += 3  # Example of gaining Fortitude

def celestialSeerOnHit(char: Character, target: Character):
    # print(f"{char.name} hit {target.name}")

    if char.base_stats["opening"] == 1:
        bonusFortitudeDamage = char.base_stats["fortitude"] * 3
        bonusDamage = 40 + bonusFortitudeDamage
        print(f"Counterstrike: Dealt {bonusDamage} extra damage to {target.name}!")

    # Implement effects related to being hit
    pass

def celestialSeerOnMissedHit(char: Character, target: Character):
    print(f"{char.name} missed {target.name}")
    # Implement effects related to missed hits
    pass

@DeprecationWarning
def celestialSeerOnDamage(char: Character, target: Character):
    print(f"celestialSeer is damaging a target")

def celestialSeerOnAbility(char: Character, ability: Ability, targets: List[Character] = None):
    # Implement effects related to ability usage
    match ability.name:
        case "Divine Radiance":
            for target in targets:
                if target.element != "shadow":
                    continue
                shouldInstaKill = defaults.chance_to_be_true(10)
                if not shouldInstaKill:
                    target.damage_character(50, "true", "light", False, False, char)

                    continue
                
                print("Critical!")
                target.damage_character(1000, "true", "light", False, False, char)


    pass

def celestialSeerOnSpell(char: Character, spell: Spell, targets: List[Character] = None):
    # Implement effects related to spell usage
    pass

def celestialSeerOnTakeDamage(character: Character, damager: Character, type: str, element: str, damage: float, critical: bool, ignore_armor: bool):
    pass

def celestialSeerOnDeath(character: Character, killer: Character, type: str, element: str):
    
    pass

def celestialSeerOnCritical(character: Character, damager: Character, didHit: bool):
    pass

def celestialSeerOnBattleWon(character: Character, allies: List[Character], enemies: List[Character]):
    pass

def celestialSeerOnBattleLost(character: Character, allies: List[Character], enemies: List[Character]):
    pass

def celestialSeerOnBattleStart(character: Character, allies: List[Character], enemies: List[Character]):
    pass

def celestialSeerOnDodge(character: Character, attacker: Character):
    pass

def celestialSeerOnHeal(character: Character, healer: Character, heal_amount: float):
    pass

def celestialSeerOnApplyModifier(character: Character, modifier: StatModifier, source: Character = None):
    pass

def celestialSeerOnRemoveModifier(character: Character, modifier: StatModifier, source: Character = None):
    pass

def celestialSeerOnTurnStart(character: Character):
    pass

def celestialSeerOnTurnEnd(character: Character):
    pass

def celestialSeerOnAllyDeath(character: Character, ally: Character, killer: Character):
    pass

def celestialSeerOnEnemyDeath(character: Character, enemy: Character, killer: Character):
    pass



seraphine = Character(
    name = "celestialSeer",
    character_class = "celestialSeer",
    team = "player",
    element = "air",
    base_stats = {
        "health": 60,
        "max_health": 60,
        "mp": 20,
        "max_mp": 20,
        "attack_damage": 25,
        "critical_chance": 0.35,
        "defense": 5,
        "magic_defense": 5,
        "skill_points": 40,
        "max_skill_points": 40,
        "accuracy": 90,
        "agility": 30,
        "weight": 10
    },
    stat_modifiers=[],
    activeEffects={},
    effects=[],
    abilities=[],
    spells=[],
    passives={
        "onKill": celestialSeerOnKill,
        "onHit": celestialSeerOnHit,
        "onMissedHit": celestialSeerOnMissedHit,
        "onAbility": celestialSeerOnAbility,
        "onSpell": celestialSeerOnSpell,
        "onTakeDamage": celestialSeerOnTakeDamage,
        "onDeath": celestialSeerOnDeath,
        "onCritical": celestialSeerOnCritical,
        "onBattleWon": celestialSeerOnBattleWon,
        "onBattleLost": celestialSeerOnBattleLost,
        "onBattleStart": celestialSeerOnBattleStart,
        "onDodge": celestialSeerOnDodge,
        "onHeal": celestialSeerOnHeal,
        "onApplyModifier": celestialSeerOnApplyModifier,
        "onRemoveModifier": celestialSeerOnRemoveModifier,
        "onTurnStart": celestialSeerOnTurnStart,
        "onTurnEnd": celestialSeerOnTurnEnd,
        "onAllyDeath": celestialSeerOnAllyDeath,
        "onEnemyDeath": celestialSeerOnEnemyDeath
    },
    equipment=[],
    inventory=[],
    description="""
The celestialSeer is a stealthy and agile class that excels in dealing high burst damage through surprise attacks, utilizing cunning
tactics and powerful self-buffs while relying on evasion and clever positioning to outmaneuver enemies and strike from the shadows.
                    
Passives:
    Bloodlust: Regain a small amount of HP after each kill, increased if the enemy is killed within one hit.
    Shadow's Embrace: When the celestialSeer dies, they leave behind a shadowy afterimage that can redirect one hit from nearby enemies
    Killer Instinct: Critical Hits will restore Mana
    

Abilities:
    Surprise Strike: Deals massive damage to one enemy. Damage enhanced if user is Vanished.
    Blade of Death: A strike with a shadow-infused Blade deals low damage, and applies a bleeding
                    damage over time effect, increasing Critical Hit chance against that target
    Smoke Bomb: Launches a projectile towards the enemy, creating a blinding area that envelopes
                the enemy, reducing their accuracy and applying the Marked effect to the target
    Marked Effect: Reduces the effectiveness of Marked targets' armor against physical attacks

Spells:
    Vanish: Disappear into the shadows, making you invisible to enemies. Your next hit or
            Surprise Strike within 3 rounds will backstab the enemy, dealing +50% damage
    Spin Attack: Slashes rapidly around you, damaging all enemies in the process. Hit enemies
                    have their damage reduced by 15% for 3 turns.
    Summon Clone: Summons a controllable clone of yourself. The clone can attract enemy hits,
                    apply debuffs, and deal damage at a reduced rate. Disappears when killed or
                    after 3 rounds.
                    """
)

chardictionary = Character(
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
    effects=[],
    spells=[],
    equipment=[],
    inventory=[]
).character_to_json()

if input("confirm? y/n") == "y":
    with open("/Users/nokyinlim/Desktop/Card Game Test/characters.json", "r") as f:
        json_object = json.load(f)
        f.close()

    json_object["seraphine"] = chardictionary


    json_in = json.dumps(json_object)
    with open("/Users/nokyinlim/Desktop/Card Game Test/characters.json", "w") as f:
        f.write(json_in)
        f.close()
    
