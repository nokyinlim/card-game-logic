
from character import StatModifier, Character, Ability, Spell, Equipment
from mods import * 

import shared_game_data
from classes import guardian, mage


from game_loop_test_1 import main


# Sample Stat Modifiers
modifier1 = StatModifier(id="mod1", stat="attack_damage", value=5, modifier_type="add")
modifier2 = StatModifier(id="mod2", stat="defense", value=1.2, modifier_type="multiply_base")

# Sample Abilities and Spells
ability1 = Ability(
    name="Warrior's Battle Cry",
    info="A fierce scream pierces the air, granting bonus damage to all allies",
    lore="", cost=2,
    effect=[modifier1],
    type="modifier"
)

basic_sword = Equipment(
    name="Basic Sword",
    stat_modifiers=[
        StatModifier(id="base_attack_damage", stat="attack_damage", value=30, modifier_type="add")
    ]
)

spell1 = Spell(
    name="Shield",
    lore="",
    info="f",
    mp_cost=5,
    effects=[modifier2],
    type="modifier"
)

# Create two characters
character1 = Character(
    name="Guardian",
    character_class="Warrior",
    team="player",
    element="earth",
    base_stats={
        "health": 10000,
        "max_health": 100,
        "mp": 20,
        "max_mp": 20,
        "attack_damage": 15,
        "critical_chance": 0.1,
        "defense": 30,
        "magic_defense": 25,
        "skill_points": 20,
        "max_skill_points": 20,
        "accuracy": 50,
        "agility": 25,
        "weight": 10,
        "can_defy_death": 1,
        "fortitude": 0,
        "counterstrike": 0,
        "opening": 0
    },
    stat_modifiers=[modifier1],
    activeEffects=[],
    passives={
        "onKill": guardian.guardianOnKill,
        "onHit": guardian.guardianOnHit,
        "onMissedHit": guardian.guardianOnMissedHit,
        "onAbility": guardian.guardianOnAbility,
        "onSpell": guardian.guardianOnSpell,
        "onTakeDamage": guardian.guardianOnTakeDamage,
        "onDeath": guardian.guardianOnDeath,
        "onCritical": guardian.guardianOnCritical,
        "onBattleWon": guardian.guardianOnBattleWon,
        "onBattleLost": guardian.guardianOnBattleLost,
        "onBattleStart": guardian.guardianOnBattleStart,
        "onDodge": guardian.guardianOnDodge,
        "onHeal": guardian.guardianOnHeal,
        "onApplyModifier": guardian.guardianOnApplyModifier,
        "onRemoveModifier": guardian.guardianOnRemoveModifier,
        "onTurnStart": guardian.guardianOnTurnStart,
        "onTurnEnd": guardian.guardianOnTurnEnd,
        "onAllyDeath": guardian.guardianOnAllyDeath,
        "onEnemyDeath": guardian.guardianOnEnemyDeath
    },
    abilities=[guardian.guardianStunBash, guardian.guardianUnyieldingStance, guardian.guardianCounterstrike, guardian.guardianFortifiedStrike],
    spells=[guardian.guardianSelfHealing, guardian.guardianAttractHit, guardian.guardianStoneSkin],
    effects=[],
    equipment=[],
    inventory=[],
    description= 
f"""
The Guardian is a stalwart protector, embodying resilience and strength on the battlefield. With a focus
on defense and crowd control, they absorb damage and shield their allies, converting their fortitude into
overwhelming power. Drawing from the earth’s strength, Guardians excel in withstanding attacks while 
retaliating with calculated strikes that turn their defensive resolve into offensive might.
{"-" * 80}
Passives:
Fortitude Accumulation:     Each point of Fortitude increases the Guardian's damage, turning resilience into raw power.
Defensive Stance:           Every hit taken boosts Fortitude, empowering the Guardian to retaliate with greater force.
Unending Will to Fight:     Upon receiving a lethal hit for the first time, the Guardian revives with 1 health and
                            becomes untargetable for 1 round, ready to continue the fight.
{"-" * 80}
Abilities:
Stun Bash:          Strike the enemy with an earth-infused attack, dealing low damage and stunning them for 1 turn.
Unyielding Stance:  Enter a defensive posture that massively increases both physical and magical defense, gaining 
                    Fortitude for each turn while active.
Counterstrike:      Prepare for an incoming attack, nullifying damage and empowering the next strike, which deals 
                    significantly increased damage based on accumulated Fortitude.
{"-" * 80}
Spells:
Self Healing:   Emit a soothing aura that gradually restores health to the Guardian over 4 turns.
Attract Hit:    Taunt all enemies, drawing their attention and making them much more likely to target the Guardian for 4 turns.
Stone Skin:     Envelop the Guardian in a protective layer of stone, significantly increasing physical damage resistance at the
                cost of reduced magical defense and damage output.
{"-" * 80}
Ultimate Ability: Fortified Strike
| "With the roar of the earth beneath them, the Guardian calls forth the very essence of resilience. 
| In a single, earth-shattering blow, they unleash a torrent of power, where every ounce of fortitude
| and defense transforms into an unstoppable force. As the ground trembles, foes are laid bare, feeling
| the weight of a protector's fury—an unstoppable testament to a will forged in battle."
"""
)

character2 = Character(
    name="Mage",
    character_class="Mage",
    team="player",
    element="neutral",
    base_stats={
        "health": 80,
        "max_health": 80,
        "mp": 60,
        "max_mp": 60,
        "attack_damage": 10,
        "critical_chance": 0.15,
        "defense": 5,
        "magic_defense": 10,
        "skill_points": 10,
        "max_skill_points": 10,
        "accuracy": 30,
        "agility": 35,
        "weight": 10
    },
    stat_modifiers=[modifier2],
    abilities=[],
    activeEffects=[],
    passives={
        "onKill": mage.mageOnKill,
        "onHit": mage.mageOnHit,
        "onMissedHit": mage.mageOnMissedHit,
        "onAbility": mage.mageOnAbility,
        "onSpell": mage.mageOnSpell,
        "onTakeDamage": mage.mageOnTakeDamage,
        "onDeath": mage.mageOnDeath,
        "onCritical": mage.mageOnCritical,
        "onBattleWon": mage.mageOnBattleWon,
        "onBattleLost": mage.mageOnBattleLost,
        "onBattleStart": mage.mageOnBattleStart,
        "onDodge": mage.mageOnDodge,
        "onHeal": mage.mageOnHeal,
        "onApplyModifier": mage.mageOnApplyModifier,
        "onRemoveModifier": mage.mageOnRemoveModifier,
        "onTurnStart": mage.mageOnTurnStart,
        "onTurnEnd": mage.mageOnTurnEnd,
        "onAllyDeath": mage.mageOnAllyDeath,
        "onEnemyDeath": mage.mageOnEnemyDeath
    },
    spells=[],
    effects=[],
    equipment=[],
    inventory=[],
)

character3 = Character(
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
    abilities=[assassinSurpriseStrike, assassinBladeOfDeath, assassinSmokeBomb, debugInstaKill, debugFullHeal],
    spells=[assassinVanish, assassinSpinAttack, assassinSummonClone],
    passives={
        "onKill": assassinOnKill,
        "onHit": assassinOnHit,
        "onMissedHit": assassinOnMissedHit,
        "onAbility": assassinOnAbility,
        "onSpell": assassinOnSpell,
        "onTakeDamage": assassinOnTakeDamage,
        "onDeath": assassinOnDeath,
        "onCritical": assassinOnCritical,
        "onBattleWon": assassinOnBattleWon,
        "onBattleLost": assassinOnBattleLost,
        "onBattleStart": assassinOnBattleStart,
        "onDodge": assassinOnDodge,
        "onHeal": assassinOnHeal,
        "onApplyModifier": assassinOnApplyModifier,
        "onRemoveModifier": assassinOnRemoveModifier,
        "onTurnStart": assassinOnTurnStart,
        "onTurnEnd": assassinOnTurnEnd,
        "onAllyDeath": assassinOnAllyDeath,
        "onEnemyDeath": assassinOnEnemyDeath
    },
    equipment=[],
    inventory=[],
    description="""
The Assassin is a stealthy and agile class that excels in dealing high burst damage through surprise attacks, utilizing cunning
tactics and powerful self-buffs while relying on evasion and clever positioning to outmaneuver enemies and strike from the shadows.
                    
Passives:
    Bloodlust: Regain a small amount of HP after each kill, increased if the enemy is killed within one hit.
    Shadow's Embrace: When the assassin dies, they leave behind a shadowy afterimage that can redirect one hit from nearby enemies
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

enemy1 = Character(
    name = "Zombie",
    character_class="Zombie",
    team = "enemy",
    element = "earth",
    base_stats = {
        "health": 150,
        "max_health": 150,
        "mp": 20,
        "max_mp": 20,
        "attack_damage": 20,
        "critical_chance": 0,
        "defense": 5,
        "magic_defense": 0,
        "skill_points": 40,
        "max_skill_points": 40,
        "accuracy": 80,
        "agility": 5,
        "weight": 10
    },
    stat_modifiers=[],
    activeEffects={},
    effects=[{}],
    abilities=[{}],
    spells=[{}],
    passives={},
    equipment=[{}],
    inventory=[{}],
)

enemy2 = Character(
    name = "Goblin",
    character_class="Goblin",
    team = "enemy",
    element = "neutral",
    base_stats = {
        "health": 100,
        "max_health": 100,
        "mp": 20,
        "max_mp": 20,
        "attack_damage": 30,
        "critical_chance": 0,
        "defense": 0,
        "magic_defense": 0,
        "skill_points": 40,
        "max_skill_points": 40,
        "accuracy": 60,
        "agility": 5,
        "weight": 10
    },
    stat_modifiers=[],
    activeEffects={},
    effects=[{}],
    abilities=[{}],
    spells=[{}],
    passives={},
    equipment=[{}],
    inventory=[{}],
)

enemy3 = Character(
    name = "Skeleton",
    character_class="Skeleton",
    team = "enemy",
    element = "shadow",
    base_stats = {
        "health": 80,
        "max_health": 80,
        "mp": 20,
        "max_mp": 20,
        "attack_damage": 40,
        "critical_chance": 0,
        "defense": 30,
        "magic_defense": 0,
        "skill_points": 40,
        "max_skill_points": 40,
        "accuracy": 60,
        "agility": 5,
        "weight": 10
    },
    stat_modifiers=[],
    activeEffects={},
    effects=[{}],
    abilities=[{}],
    spells=[{}],
    passives={},
    equipment=[{}],
    inventory=[{}],
)

shared_game_data.characters = [character1, character2, character3, enemy1, enemy2, enemy3]

shared_game_data.enemyCharacters = [char for char in shared_game_data.characters if char.team != "player"]
shared_game_data.playerCharacters = [char for char in shared_game_data.characters if char.team == "player"]

game = True

while game:
    print(character.describe_character for character in shared_game_data.characters)
    game = main(shared_game_data.characters, shared_game_data.enemyCharacters, shared_game_data.playerCharacters)
    
    