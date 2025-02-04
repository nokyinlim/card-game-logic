from typing import List
from character import StatModifier, Character, Ability, Spell, Equipment
import defaults
from shared_game_data import characters, playerCharacters
import shared_game_data 

# Modifiers
warriorBattleCryEffect = StatModifier(
	id="warriorBattleCry",
    duration=3,
    modifier_type="multiply_base",
    stat="attack_damage",
    value=0.2
)

tauntEffect = None


# Abilities



heavyAttack = Ability(name="",
					lore="-",
                    info="",
                    cost=10,
                    type="damage",
                    effect=None,
                    damage=50
)

# Spells
airSpell1 = Spell(name="Way of the Tempest", 
                       lore="There is a storm in you. Filled with strikes of lightning and crashing thunder. Unleash it.",
                       info="Deals low air damage to one enemy.", 
                       mp_cost=5, effects=None, type="damage", damage={"damage": 60, "element": "air", "targets": ""})
    
fireSpell1 = Spell(name="Way of the Flames", 
                       lore="Consume.",
                       info="Deals low fire damage to one enemy.", 
                       mp_cost=5, effects=None, type="damage", damage={"damage": 60, "element": "fire", "targets": ""})
    
earthSpell1 = Spell(name="Way of the Wild", 
                       lore="Run free, live free, die free.",
                       info="Deals low earth damage to one enemy.", 
                       mp_cost=5, effects=None, type="damage", damage={"damage": 60, "element": "earth", "targets": ""})
    
waterSpell1 = Spell(name="Way of the Lethal Stream", 
                       lore="Move like a current.",
                       info="Deals low water damage to one enemy.", 
                		   mp_cost=5, effects=None, type="damage", damage={"damage": 60, "element": "water", "targets": ""})
                        

tankAttractHit = Ability(
	name="Taunt",
    lore="",
    info="Taunt all enemies, making them much more likely to target you for 4 turns.",
    cost=4,
    effect=[StatModifier(
        id = "tauntEffect",
        stat = "weight",
        value = 90,
        modifier_type = "add",
        duration = 4
    )],
    type="modifier"
)

debugInstaKill = Ability(
    name = "instakill",
    lore = "For Debugging Purposes Only", info = "",
    cost = 0,
    type = "damage",
    effect = [],
    damage = {"damage": 9999, "element": "neutral"}
)

debugFullHeal = Ability(
    name = "fullheal",
    lore = "For Debugging Purposes Only", info = "",
    cost = 0,
    type = "damage",
    effect = [],
    damage = {"damage": -9999, "element": "neutral"}
)

# Assassin

assassinSurpriseStrike = Ability(
    name = "Surprise Strike",
    lore = "",
    info = "A quick blow deals massive damage to one enemy. Damage further enhanced if user is Vanished.",
    cost = 5,
    type = "damage",
    effect = [],
    damage = {
        "damage": 80,
        "element": "neutral"
    }
)

assassinCloneSurpriseStrike = Ability(
    name = "Surprise Strike",
    lore = "",
    info = "A quick blow deals high damage to one enemy. Damage enhanced if the clone is Vanished.",
    cost = 10,
    type = "damage",
    effect = [],
    damage = {
        "damage": 50,
        "element": "neutral"
    }
)

@PendingDeprecationWarning
def assassinSurpriseStrikeFunction(vanished: bool = False) -> Ability:
    bonus = 1.5 if vanished else 1
    return Ability(
        name = "Surprise Strike",
        lore = "",
        info = "A quick blow deals massive damage to one enemy. Damage further enhanced if user is Vanished.",
        cost = 5,
        type = "damage",
        effect = [],
        damage = {
            "damage": 80 * bonus,
            "element": "neutral"
        }
    )

assassinShadowRequiem = Ability(
    name = "[Ult] Shadow Requiem",
    lore = "Unleash the full power of the shadows, striking down all foes in a breathtaking",
    info = "dance of death that echoes through the night...",
    cost = 20,
    effect = [StatModifier(
        id = "shadowRequiemInvisibility",
        stat = "weight",
        value = -1,
        modifier_type = "add",
        duration = 2,
        targetsSelf = True
    )],
    type = "damage",
    damage = {
        "damage": 150,
        "element": "neutral",
        "targets": "enemies"
    }
)

assassinVanish = Spell(name = "Vanish",
                       lore = "Disappear into thin air, making you invisible to enemies.",
                       info = "Your next hit or Surprise Strike within 3 rounds will backstab the enemy, dealing +50% damage.",
                       mp_cost = 4,
                       type="modifier",
                       effects = [StatModifier(
                           id="vanish_attack_bonus",
                           stat="attack_damage",
                           value=0.5,
                           modifier_type="multiply_base",
                           duration=3
                        ), StatModifier(
                            id="vanish_invisibility",
                            stat="weight",
                            value=-1,
                            modifier_type="multiply_base",
                            duration=3
                        )])

assassinCloneVanish = Spell(name = "Vanish",
                       lore = "Disappear into thin air, making the clone less visible to enemies. The clone's next",
                       info = "hit or Surprise Strike within 2 rounds will backstab the enemy, dealing +30% damage.",
                       mp_cost = 4,
                       type="modifier",
                       effects = [StatModifier(
                           id="vanish_attack_bonus",
                           stat="attack_damage",
                           value=0.3,
                           modifier_type="multiply_base",
                           duration=2
                        ), StatModifier(
                            id="vanish_invisibility",
                            stat="weight",
                            value=-0.8,
                            modifier_type="multiply_base",
                            duration=2
                        )])

assassinSpinAttack = Spell(name = "Spin Attack",
                           lore = "Slashes rapidly around you, damaging all enemies in the process.",
                           info = "Hit enemies have their damage reduced by 15% for 3 turns",
                           mp_cost = 6,
                           type = "damage",
                           effects = [StatModifier(
                               id = "spinAttackDamageReduction",
                               stat = "attack_damage",
                               value = -0.15,
                               modifier_type = "multiply_base",
                               duration = 3,
                               targetsSelf = True
                           )],
                           damage = {
                               "damage": 40,
                               "element": "neutral",
                               "targets": "enemies"
                           })

assassinCloneSpinAttack = Spell(name = "Spin Attack",
                           lore = "Slashes around you, damaging all enemies for a little damage.",
                           info = "Hit enemies have their damage reduced by 10% for 2 turns",
                           mp_cost = 5,
                           type = "damage",
                           effects = [StatModifier(
                               id = "spinAttackDamageReduction",
                               stat = "attack_damage",
                               value = -0.10,
                               modifier_type = "multiply_base",
                               duration = 2,
                               targetsSelf = True
                           )],
                           damage = {
                               "damage": 20,
                               "element": "neutral",
                               "targets": "enemies"
                           })

assassinSummonClone = Spell(name = "Summon Clone",
                            lore = "The Assassin creates a controllable shadow doppelgänger, which can",
                            info = "debuff enemies, redirect enemy hits, and attack at reduced damage.",
                            mp_cost = 10,
                            effects = [],
                            type = "other")

assassinSmokeBomb = Spell(
    name = "Smoke Bomb",
    lore = "A blinding area of smoke envelopes the enemy, dealing minor damage and reducing their accuracy",
    info = "and applying the Marked effect to the target for 3 turns\nMarked: Armor Effectiveness is reduced on target",
    mp_cost = 5,
    effects=[StatModifier(
        id = "smoke_bomb_accuracy",
        stat = "accuracy",
        value = -20,
        modifier_type = "add",
        duration = 3,
        targetsSelf = True
    ), StatModifier(
        id = "smoke_bomb_armor_penetration",
        stat = "defense",
        value = -0.3, modifier_type = "add",
        duration = 3, targetsSelf = True
    )], type = "damage",
    damage = {
        "damage": 15,
        "element": "neutral", 
        "targets": ""
    }
)

assassinCloneSmokeBomb = Spell(
    name = "Smoke Bomb",
    lore = "A blinding area of smoke envelopes the enemy, reducing their accuracy",
    info = "and applying the Marked effect to the target for 2 turns\nMarked: Armor Effectiveness is reduced on target",
    mp_cost = 5,
    effects=[StatModifier(
        id = "smoke_bomb_accuracy",
        stat = "accuracy",
        value = -15,
        modifier_type = "add",
        duration = 2,
        targetsSelf = True
    ), StatModifier(
        id = "smoke_bomb_armor_penetration",
        stat = "defense",
        value = -0.2, modifier_type = "add",
        duration = 2, targetsSelf = True
    )], type = "damage",
    damage = {
        "damage": 0,
        "element": "neutral", 
        "targets": ""
    }
)

assassinCloneCharacter = Character(
    name = "Assassin [Clone]",
    character_class = "Assassin",
    team = "player",
    element = "air",
    base_stats = {
        "health": 25,
        "max_health": 25,
        "mp": 10,
        "max_mp": 10,
        "attack_damage": 20,
        "critical_chance": 0.25,
        "defense": 0,
        "magic_defense": 0,
        "skill_points": 20,
        "max_skill_points": 20,
        "accuracy": 75,
        "agility": 20,
        "weight": 15
    },
    stat_modifiers=[],
    activeEffects={},
    effects=[],
    abilities=[assassinCloneSurpriseStrike, assassinCloneSmokeBomb],
    spells=[assassinCloneVanish, assassinCloneSpinAttack],
    passives={},
    equipment=[],
    inventory=[],
    description="An Assassin... or is it?"
)

assassinBladeOfDeath = Ability(name = "Blade of Death",
                               lore = "A quick strike with a shadow-infused Blade",
                               info = "deals low damage, and applies a bleed effect",
                               cost = 3,
                               type = "damage",
                               effect = [StatModifier(
                                   id = "assassinBleed",
                                   stat = "health",
                                   value = -10,
                                   modifier_type = "turn",
                                   duration = 3,
                                   targetsSelf = False
                               )],
                               damage = {
                                   "damage": 20,
                                   "element": "neutral"
                               })



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
        shared_game_data.characters.insert(0, assassinCloneCharacter)
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



_defaultAssassin = Character(
    name = "Assassin",
    character_class = "Assassin",
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
        "magic_defense": 10,
        "skill_points": 40,
        "max_skill_points": 40,
        "accuracy": 90,
        "agility": 30,
        "weight": 10
    },
    stat_modifiers=[],
    activeEffects=[],
    effects=[],
    abilities=[],
    spells=[],
    passives={
        "ability": None,
        "onKill": assassinOnKill
    },
    equipment=[],
    inventory=[]
)

