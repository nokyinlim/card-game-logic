
import json
from typing import List, Dict, Any, Callable

from random import random
import defaults


from account import update_account_stat
from passives import get_before_passive_function, get_passive_function



class StatModifier:
    """
    Stat Modifiers: Modifiers that can be applied to stats of a character
    id: str -> Identifier of the modifier
    stat: str -> ID of the stat
    value: float -> Value modifier of the stat
    modifier_type: str in ["add", "multiply_base", "multiplicative", "turn", "status"]
        add: Directly adds the value (flat, additive)
        multiply_base: Multiplies by the base value (e.g. 0.2 is 20% increase)
        multiplicative: Multiplies the final value (including other multiplicative stat modifiers, where 1.2 is 20% increase)
        turn: Applies the modifier each turn (does not revert after)
        status: Changes how the StatModifier will be processed (e.g. "poison", "burn")
            stat: str now represents the status effect
            value: float now represents the chance of the status effect. Negative value means chance to remove. 
            modifier_type: "status"
            duration: int -> Duration of the status effect
            targetsSelf: bool -> Whether the status effect targets self or the target (if specified; defaults always to Self)
            displayName: str -> Display name of the status effect (for UI only)
    duration: int -> Duration of the modifier in turns
    targetsSelf: bool -> Whether the modifier targets self or the target (if specified; defaults always to Self)
    applyer: Character -> Character that applied the modifier (unused for now)
    displayName: str -> Display name of the modifier (for UI only)
    """

    def __init__(self, id: str, stat: str, value: float, modifier_type: str, duration: int = None, targetsSelf: bool = True, applyer = None, displayName: str = ""):
        self.id = id
        self.stat = stat
        self.value = value
        self.modifier_type = modifier_type
        self.duration = duration  # Duration in turns
        self.targetsSelf = targetsSelf
        self.applyer = applyer
        self.displayName = displayName

    def stat_modifier_to_json(self) -> Dict[str, Any]:
        modifier = self
        return {
            "id": modifier.id,
            "stat": modifier.stat,
            "value": modifier.value,
            "modifier_type": modifier.modifier_type,
            "duration": modifier.duration,
            "targetsSelf": modifier.targetsSelf,
            "applyer": modifier.applyer,
            "displayName": modifier.displayName
        }

class Equipment:
    def __init__(self, name: str, stat_modifiers: List[StatModifier]):
        self.name = name
        self.stat_modifiers = stat_modifiers

class Ability:
    """
    Ability: a castable ability used by characters within character.abilities: List[Ability]
    name: str -> Name of the ability
    lore: str -> Lore of the ability (or line 1)
    info: str -> Information about the ability (or line 2)
    cost: int -> Skill point cost of the ability
    effect: List[StatModifier] -> List of stat modifiers applied by the ability
    type: str in ["modifier", "damage", "debuff"] -> Type of the ability
        modifier -> Applies a modifier to the character
        damage -> Deals damage to a target
        debuff -> Applies a debuff to a target
    damage: dict -> Damage information of the ability
        damage: int -> Damage dealt by the ability
        element: str -> Element of the ability
        targets: str -> Targets of the ability (unused for now)
    cooldown: int -> Cooldown of the ability
    """
    def __init__(self, name: str, lore: str, info: str, cost: int, effect: List[StatModifier], type: str, damage: dict = {
        "damage": 0,
        "element": "",
        "targets": ""
    }, cooldown: int = 0):
        self.name = name
        self.lore = lore
        self.info = info
        self.cost = cost
        self.effect = effect
        self.type = type
        self.damage = damage
        self.cooldown = cooldown
        pass

    def ability_to_json(self) -> Dict[str, Any]:
        ability = self

        ability_dict = {
            "name": ability.name,
            "lore": ability.lore,
            "info": ability.info,
            "cost": ability.cost,
            "effect": [effect.stat_modifier_to_json() for effect in ability.effect],
            "type": ability.type,
            "damage": ability.damage,
            "cooldown": ability.cooldown
        }
        
        return ability_dict

class Spell:
    """
        Spell: a castable spell used by characters within character.spells: List[Spell]
        name: str -> Name of the spell
        lore: str -> Lore of the spell (or line 1)
        info: str -> Information about the spell (or line 2)
        mp_cost: int -> Mana cost of the spell
        effects: List[StatModifier] -> List of stat modifiers applied by the spell
        type: str in ["modifier", "damage", "debuff"] -> Type of the spell
            modifier -> Applies a modifier to the character
            damage -> Deals damage to a target
            debuff -> Applies a debuff to a target
        damage: dict -> Damage information of the spell
            damage: int -> Damage dealt by the spell
            element: str -> Element of the spell
            targets: str -> Targets of the spell (unused for now)
        cooldown: int -> Cooldown of the spell
    """
    def __init__(self, name: str, lore: str, info: str, mp_cost: int, effects: List[StatModifier], type: str, damage: dict = {
        "damage": 0,
        "element": "",
        "targets": ""
    }, cooldown: int = 0):
        
        self.name = name
        self.lore = lore
        self.info = info
        self.mp_cost = mp_cost
        self.effects = effects
        self.type = type
        self.damage = damage
        self.cooldown = cooldown
        pass

    
    
    def spell_to_json(self) -> Dict[str, Any]:
        """
        Returns a Dictionary representation of the spell
        """
        spell = self

        spell_dict = {
            "name": spell.name,
            "lore": spell.lore,
            "info": spell.info,
            "mp_cost": spell.mp_cost,
            "effects": [effect.stat_modifier_to_json() for effect in spell.effects],
            "type": spell.type,
            "damage": spell.damage,
            "cooldown": spell.cooldown
        }
        
        return spell_dict


class Card:
    """
    Card: a collectible, single-use card used by characters within character.inventory: List[Card]
    type: str in ["custom", "ability", "damage", "spell", "effect"] -> Type of the card
        custom -> Custom card with custom effects. data format:
            action: str -> Action, defined in utils.py to be performed. String matching a function name.
        ability -> Ability card
            ability: Ability -> Ability object to be used
        damage -> Damage card
            damage: int -> Damage dealt by the card
            damage_type: str -> Damage type of the damage ("physical", "magic", "true")
            element: str -> Element of the card. Refer to element_types.
            target: str -> Target for the damage. Given as a player_id, or leave empty for self.
        spell -> Spell card
            spell: Spell -> Spell object to be used
        effect -> Applies one or more effects on characters.
            effects: List[StatModifier] -> List of stat modifiers to be applied
            self_id: str -> Current user's player ID
            target_id: str -> Opponent user's player ID
    """
    def __init__(self,
            type: str,
            name: str,
            data: Dict[str, Any]
    ):
        self.type = type
        self.name = name
        self.data = data
        pass

""" # list of stats
List of Stats

Modifiers are not added directly to the character

health: int -> Tracks the current health of the character
max_health: int -> Tracks the maximum health of the character
mp: int -> Tracks the current mana of the character
max_mp: int -> Tracks the maximum mana of the character
skill_points: int -> Tracks skill points (abilities)
max_skill_points: int -> Max Skill Points (abilities)
attack_damage: int -> Tracks the attack damage of the character
spell_damage: int -> Tracks the spell damage of the character
critical_chance: float -> Critical hit chance of the character
defense: int -> Tracks the defense of the character
magic_defense: int -> Tracks magic defense of the character
accuracy: int -> Tracks accuracy of the character
agility: int -> Tracks speed of character
"""

element_types: dict[str, dict[str, str]] = {
    "fire": {
        "strength": "earth",
        "weakness": "water"
    },
    "earth": {
        "strength": "air",
        "weakness": "fire"
    },
    "air": {
        "strength": "thunder",
        "weakness": "earth"
    },
    "thunder": {
        "strength": "water",
        "weakness": "air"
    },
    "water": {
        "strength": "fire",
        "weakness": "thunder"
    },
    "neutral": {
        "strength": "",
        "weakness": ""
    },
    "light": {
        "strength": "shadow",
        "weakness": "light"
    },
    "shadow": {
        "strength": "light",
        "weakness": "shadow"
    }
}



class Character:
    """
    Creates a Character object with the following parameters:
    ### Parameters
    - name (str): Name of the character
    - character_class (str): Class of the character
    - team (str): Team of the character (deprecated)
    - element (str): Element of the character
    - base_stats (dict): Base stats of the character
        - health (int): Tracks the current health of the character
        - max_health (int): Tracks the base maximum health of the character
        - mp (int): Tracks the current mana of the character
        - max_mp (int): Tracks the base maximum mana of the character
        - spell_damage (int): Tracks the base spell damage of the character
        - attack_damage (int): Tracks the base attack damage of the character
        - critical_chance (float): Base critical hit chance of the character
        - defense (int): Tracks the base defense of the character
        - magic_defense (int): Tracks the base magic defense of the character
        - accuracy (int): Tracks the base accuracy of the character
        - agility (int): Tracks the base speed of the character
        - skill_points (int): Tracks skill points (abilities)
        - max_skill_points (int): Max Skill Points (abilities)
    - character_data (Dict[str, Any]): Character data (leave empty); defined as needed to store char-specific data
    - stat_modifiers (List[StatModifier]): List of stat modifiers applied to the character
    - activeEffects (dict): Active effects on the character (leave empty)
    - effects (List[dict]): Effects of the character (leave empty)
    - abilities (List[Ability]): List of abilities of the character
    - spells (List[Spell]): List of spells of the character
    - passives (str): Key of the Passive constant (from passives.py)
    - equipment (List[dict]): List of equipment currently equipped by the character (leave empty)
    - inventory (List[Card]): List of cards in the character's inventory (leave empty, user-defined)
    - description (str): Description of the character (optional, recommended)
    """

    def __init__(self,
                 name: str, 
                 character_class: str, 
                 team: str,
                 element: str,
                 base_stats: dict,
                 character_data: Dict[str, Any],
                 stat_modifiers: List[StatModifier],
                 activeEffects: List[StatModifier],
                 effects: List[dict],
                 abilities: List[Ability],
                 spells: List[Spell],
                 passives: str,
                 equipment: List[dict],
                 inventory: List[Card],
                 description: str = ""): # Inventory == cards
        self.name = name
        self.character_class = character_class
        self.team = team
        self.element = element
        self.base_stats = base_stats
        self.character_data = character_data
        self.stat_modifiers = stat_modifiers
        self.activeEffects = activeEffects
        self.effects = effects
        self.abilities = abilities
        self.spells = spells
        self.passives = passives
        self.equipment = equipment
        self.active_modifiers: List[StatModifier] = []  # To track active modifiers
        self.inventory = inventory
        self.turns = 0
        self.description = description

        pass

    def apply_active_modifiers(self):
        for modifier in self.active_modifiers:
            if modifier.duration is not None:
                modifier.duration -= 1  # Reduce duration by 1
                if modifier.modifier_type == "turn":
                    print("Turn-based Modifier")
                    print(f"Stat: {modifier.stat}, Value: {modifier.value}")
                    # applies each turn

                    if modifier.stat == "health":
                        print(f"Health Modifier for {self.name}")
                        print(f"Old Health: {self.base_stats["health"]}")
                        self.damage_character(
                            damage=-modifier.value,
                            damage_origin="true",
                            damage_type="neutral",
                            ignore_armor=True,
                            critical=False,
                            damager=modifier.applyer
                        )
                        print(f"New Health: {self.base_stats["health"]}")
                        pass
                    else: 
                        self.base_stats[modifier.stat] += modifier.value

                    pass

                if modifier.duration <= 0:
                    print(f"Removed a Modifier from {self.name}: {modifier.id}")
                    self.stat_modifiers.remove(modifier)  # Remove expired modifiers
                    self.active_modifiers.remove(modifier)  # Remove from active modifiers

    def equip(self, equipment: Equipment):
        self.equipment.append(equipment)
        for mod in equipment.stat_modifiers:
            self.stat_modifiers.append(mod)
            self.active_modifiers.append(mod)  # Track as active
        
    def unequip(self, equipment: Equipment):
        if equipment not in self.equipment:
            return
        
        self.equipment.remove(equipment)
        for mod in equipment.stat_modifiers:
            try:
                self.stat_modifiers.remove(mod)
                self.active_modifiers.remove(mod)
            except:
                print("Could not find any equipment Stat Modifiers")

    def apply_status_effects(self):
        effects = self.activeEffects
        for effect in effects:
            if effect.duration is None:
                continue

            effect.duration -= 1
            if effect.duration > 0:
                continue

            self.activeEffects.remove(effect)
            print(f"{self.name} no longer has {effect.displayName}")

            # Run passive
            passive = get_passive_function(self.passives, "onRemoveModifier")
            if passive: passive(self, effect)

    def end_turn(self):
        self.turns += 1
        self.apply_active_modifiers()  # Apply active modifiers at the end of each turn
        self.apply_status_effects()

    def get_stat(self, stat: str) -> float:
        """
        Returns the value of a given stat, including StatModifiers and Equipment.
        """
        base_stat = self.base_stats[stat]

        modifiers = self.stat_modifiers

        addModifiers = 0
        multBaseModifiers = 1
        multAllModifiers = 1

        for modifier in modifiers:
            if modifier.stat != stat:
                continue

            if modifier.modifier_type in ["turn", "status"]:
                continue
                
            match modifier.modifier_type:
                case "add":
                    addModifiers += modifier.value
                case "multiply_base":
                    multBaseModifiers += modifier.value
                case "multiplicative":
                    multAllModifiers *= modifier.value

        final_stat: float = ((base_stat * multBaseModifiers) + addModifiers) * multAllModifiers
        return final_stat
    
    def attack(self, target: 'Character', element = "neutral", attacker_username: str = "", target_username: str = "", guarantee_hit: bool = False, damage_origin: str = "physical") -> Dict[str, Any]:
        """
        Attacks a target character with the attack damage of the character.
        target: Character -> Target character to attack
        element: str -> Element of the attack (defaults to "neutral")

        This includes Critical Hit Chance, Accuracy, and Elemental Strengths/Weaknesses

        :return: Dict[str, Any] -> Dictionary containing the results of the attack
        didHit: bool -> Whether the attack hit the target
        self: Character -> The attacking character
        target: Character -> The target character
        damage: int -> Damage dealt to the target
        critical: bool -> Whether the attack was a critical hit
        element: str -> Element of the attack
        damage_type: str -> Origin of the damage (physical, magic, true)
        message: str -> Message output of the attack
        """
        damage = self.get_stat("attack_damage")
        # damage_type = "neutral"  # Assuming all attacks are neutral for now
        print(f"Debug: {self.name} attacks {target.name} for base {damage} damage!")

        criticalChancePercent = self.get_stat("critical_chance") * 100

        critical = defaults.chance_to_be_true(criticalChancePercent)

        bonusAccuracy = self.get_stat("accuracy") - target.get_stat('agility')
        totalAccuracy = (0.7 + bonusAccuracy) / 100
        didHit = (totalAccuracy > random() or guarantee_hit)

        ignore_armor: bool = False

        try: 
            damage = get_before_passive_function(damage_amount=final_damage, char=self, target=target, type=damage_origin, element=element, ignore_armor=ignore_armor, critical=critical, didHit=didHit)
            final_damage = damage["damage"]
            didHit = damage["didHit"]
            critical = damage["critical"]
            ignore_armor = damage["ignore_armor"]
            # others added here
        except: final_damage = damage

        if didHit:
            # Call the target's damage_character method to apply damage
            messages = target.damage_character(final_damage, damage_origin=damage_origin, damage_type=element, ignore_armor=ignore_armor, critical=critical, damager_username=attacker_username, defender_username=target_username, damager=self)
            passive = get_passive_function(self.passives, "onHit")
            if passive: passive(self, target, final_damage, damage_origin, element, critical, ignore_armor=ignore_armor)
            # print(f"{self.name} hits the {target.name} for {final_damage} damage!")
            # message = f"{self.name} hits the {target.name} for {final_damage} damage!"
        else:
            print(f"{self.name} missed the {target.name}!")
            messages = [f"{self.name} missed the {target.name}!"]
            passive = get_passive_function(self.passives, "onMissedHit")
            if passive: passive(self, target, final_damage, damage_origin, element, critical, ignore_armor)

        if critical:
            print(f"{self.name} lands a critical hit on {target.name}!")
            messages.append(f"{self.name} lands a critical hit on {target.name}!") if didHit else None
            passive = get_passive_function(self.passives, "onCritical")
            if passive: passive(self, target, didHit)
        


        # for later implementation
        if False and attacker_username:
            if didHit:
                update_account_stat(attacker_username, "success_attack")

                update_account_stat(attacker_username, "deal_damage", final_damage, "add")

                stat_to_update: str = f"deal_damage_{element}"
                update_account_stat(attacker_username, stat_to_update, final_damage, "add")

                stat_to_update: str = "deal_damage_physical"
                update_account_stat(attacker_username, stat_to_update, final_damage, "add")
            else:
                update_account_stat(attacker_username, "miss_attack")

            if critical:
                update_account_stat(attacker_username, "critical_attack")
            

            pass
        
        return {"didHit": didHit, 
                "self": self, 
                "target": target, 
                "damage": final_damage, 
                "critical": critical, 
                "element": element, 
                "damage_type": damage_origin,
                "messages": messages
                }

    def damage_character(self, 
                     damage: int, 
                     damage_origin: str, 
                     damage_type: str, 
                     ignore_armor: bool = False,
                     critical: bool = False,
                     damager: 'Character' = None,
                     damager_username: str = "",
                     defender_username: str = "") -> List[str]:
        """
        Damages this current character, with the given parameters:
        damage: int -> Damage value to be dealt
        damage_origin: str in ["physical", "magic", "true"] -> Origin of the damage
            physical -> Physical damage (uses defense, ignores magic defense)
            magic -> Magical damage (uses magic defense, ignores defense)
            true -> True damage (ignores both defense and magic defense)
        damage_type: str -> Element of the damage. See element_types
        ignore_armor: bool -> Whether the damage ignores armor (sets armor to 2/3 of the original)
        critical: bool -> Whether the damage is a critical hit (increases damage by 50%)
        damager: Character -> Character that dealt the damage (optional, needed for character passives)
        damager_username: str -> Username of the damager (optional, needed for account stats)
        """

        # Determine the defense value based on the damage origin
        defense = 0
        match damage_origin:
            case "physical":
                defense = self.get_stat("defense")
            case "magic":
                defense = self.get_stat("magic_defense")
            case "true":
                defense = 0

        if self.element == "shadow" and damage_type != "light":
            # print("Shadow Resilience!")
            defense += 100

        # Ignore defense if specified; for full armor ignore use True Damage
        if ignore_armor:
            armor_points_ignored = defense * 1/3
            update_account_stat(damager_username, "armor_points_ignored", armor_points_ignored, "add")
            defense *= 2/3
            

        # Apply critical hit modifier
        if critical:
            damage *= 1.5  

        # Calculate effective damage
        effective_damage = defaults.calculate_effective_damage(damage, defense)
        effective_damage = max(1, effective_damage)  # Ensure damage is not negative
        

        # print(f"Attacker uses {damage_type}; attack stong against: {element_types[damage_type]["strength"]} == enemy: {self.element};weak against {element_types[self.element]["weakness"]}")
        if element_types[damage_type]["strength"] == self.element:
            effective_damage *= 1.8
            print("Elemental Strength!")
        elif element_types[damage_type]["weakness"] == self.element:
            effective_damage *= 0.7
            print("Elemental Resistance!")

        # Subtract effective damage from health
        self.base_stats["health"] -= effective_damage

        # health can now drop below 0
        # self.base_stats["health"] = max(0, self.base_stats["health"])  # Ensure health doesn't drop below 0

        if self.base_stats["health"] <= 0:
            print("Character has Died!")
            if damager and self.passives:
                passive_name = self.passives
                # this part uses the get_passive_function() from passives.py
                # this is necessary to avoid a cicular import
                
                # Get and execute the onDeath passive if it exists, so try statement not necessary
                on_death_func = get_passive_function(passive_name, "onDeath")
                if on_death_func:
                    on_death_func(self, damager, damage_origin, damage_type)
        else:
            # onDamage function

            if damager and self.passives:
                passive_name = self.passives
                # this part uses the get_passive_function() from passives.py
                # this is necessary to avoid a cicular import
                    

                on_damage_func = get_passive_function(passive_name, "onTakeDamage")
                if on_damage_func:
                    try: 
                        on_damage_func(self, damager, damage_origin, damage_type, effective_damage, critical, ignore_armor)
                    except:
                        print("Error in onDamage function: Not Implemented")
            pass

        # Output the damage dealt
        print(f"{damager.name} attacks {self.name} for {effective_damage} {damage_type} damage!")

        return [f"{damager.name} attacks {self.name} for {effective_damage} {damage_type} damage!"]

    def apply_stat_modifier(self, effect: StatModifier):
        print(f"Applied effect: {effect.stat} {effect.value} ({effect.modifier_type})")

        passive = get_passive_function(self.passives, "onApplyModifier")
        if passive: passive(self, StatModifier)
        if effect.modifier_type == "turn":
            self.active_modifiers.append(effect)
        elif effect.modifier_type == "status":
            self.activeEffects[effect.stat] = effect
        else: 
            self.stat_modifiers.append(effect)

    def use_ability(self, ability: Ability, targets: List['Character'] = None):
        """
        Uses an ability from a Character. 
        Usage: character.use_ability(ability, targets)
        ability: Ability -> Ability to be used
        targets: List[Character] -> List of targets for the ability (only if ability.type == "damage" or "debuff")
        """
        messages: List[str] = []
        if self.base_stats["skill_points"] >= ability.cost:
            self.base_stats["skill_points"] -= ability.cost
            # Apply the effect of the ability
            
            match ability.type:
                case "modifier":
                    print(f"{self.name} used ability: {ability.name}!")
                    messages.append(f"{self.name} used ability: {ability.name}!")
                    for effect in ability.effect:
                        print(f"Applied effect: {effect.stat} {effect.value} ({effect.modifier_type})")
                        if effect.modifier_type == "turn":
                            self.active_modifiers.append(effect)
                        else: 
                            self.stat_modifiers.append(effect)
                case "damage":
                    print(f"{self.name} used ability: {ability.name}!")
                    messages.append(f"{self.name} used ability: {ability.name} on {[char.name for char in targets]}!")

                    if not targets:
                        messages = ["No targets specified for the ability."]
                        return {
                            "self": self,
                            "targets": targets,
                            "messages": messages,
                            "error": True
                        }
                    
                    for target in targets:
                        target.damage_character(ability.damage["damage"], "magic", ability.damage["element"])
                        if ability.effect != []:
                            for effect in ability.effect:
                                print(f"Applied effect: {effect.stat} {effect.value} ({effect.modifier_type})")
                                
                                if effect.targetsSelf:
                                    if effect.modifier_type == "turn":
                                        self.active_modifiers.append(effect)
                                    else: 
                                        self.stat_modifiers.append(effect)
                                else:
                                    if effect.modifier_type == "turn":
                                        [target.active_modifiers.append(effect) for target in targets]
                                    else:
                                        [target.stat_modifiers.append(effect) for target in targets]
                            
                    pass
                case "debuff":
                    print("Debuff Ability!")
        else:
            print(f"{self.name} does not have enough skill points to use {ability.name}.")
            messages.append(f"{self.name} does not have enough skill points to use {ability.name}.")
        
        return {
            "self": self,
            "targets": targets,
            "messages": messages,
            "error": False
        }

    def cast_spell(self, spell: Spell, targets: List['Character'] = None):
        """
        Casts a spell from a Character.
        Usage: character.cast_spell(spell, targets)
        spell: Spell -> Spell to be cast
        targets: List[Character] -> List of targets for the spell (only if spell.type == "damage" or "debuff")
        """
        if self.base_stats["mp"] >= spell.mp_cost:
            self.base_stats["mp"] -= spell.mp_cost
            # Apply the effect of the spell
            match spell.type:
                case "modifier":
                    print(f"{self.name} used ability: {spell.name}!")
                    for effect in spell.effects:
                        print(f"Applied effect: {effect.stat} {effect.value} ({effect.modifier_type})")
                        if effect.modifier_type == "turn":
                            self.active_modifiers.append(effect)
                        else: 
                            self.stat_modifiers.append(effect)
                case "damage":
                    print(f"{self.name} used ability: {spell.name}!")
                    damage = spell.damage["damage"]
                    if damage > 0:
                        damage += self.get_stat("spell_damage")
                    elif damage < 0:
                        damage -= self.get_stat("spell_damage")
                    for target in targets:
                        if target:
                            target.damage_character(damage, "magic", spell.damage["element"])
                        pass
                    if spell.effects:
                        for effect in spell.effects:
                            print(f"Applied effect: {effect.stat} {effect.value} ({effect.modifier_type})")
                            if effect.modifier_type == "turn":
                                self.active_modifiers.append(effect)
                            else: 
                                self.stat_modifiers.append(effect)
                case "debuff":
                    print("Debuff Ability!")
                case "cure":
                    print("Cure Ability!")

                    if spell.effects:
                        for effect in spell.effects:
                            print(f"Status To Cure: {effect.stat}")
                            if effect.stat in target.activeEffects:
                                target.activeEffects.remove(effect.stat)
                                print(f"Removed {effect.stat} from {target.name}")
                            

        else:
            print(f"{self.name} does not have enough MP to cast {spell.name}.")
        
        return {
            "self": self,
            "targets": targets
        }

    # Display character stats
    @DeprecationWarning
    def display_character_stats(self):
        print("-" * 30)
        print(f"Name: {self.name}")
        print(f"Class: {self.character_class}")
        print(f"Health: {self.base_stats['health']}/{self.base_stats['max_health']}")
        print(f"Mana: {self.base_stats['mp']}/{self.base_stats['max_mp']}")
        print(f"Skills: {self.base_stats['skill_points']}/{self.base_stats['max_skill_points']}")
        print(f"Attack Damage: {self.get_stat('attack_damage')}")
        print(f"Critical Chance: {self.get_stat('critical_chance') * 100}%")
        print(f"Defense: {self.get_stat('defense')}")
        print(f"Magic Defense: {self.get_stat('magic_defense')}")
        print("-" * 30)

    def describe_character(self):
        print(self.name)
        print(self.description)

    def character_to_json(self, new_team = "") -> dict:
        """
        Creates a Dictionary representation of this character
        Usage: character.character_to_json()
        """
        character = self
        return {
            "name": character.name,
            "character_class": character.character_class,
            "team": character.team,
            "element": character.element,
            "base_stats": character.base_stats,
            "character_data": character.character_data,
            "stat_modifiers": [
                {
                    "id": mod.id,
                    "stat": mod.stat,
                    "value": mod.value,
                    "modifier_type": mod.modifier_type,
                    "duration": mod.duration,
                    "targetsSelf": mod.targetsSelf,
                    "applyer": mod.applyer,
                    "displayName": mod.displayName
                } for mod in character.stat_modifiers
            ],
            "activeEffects": [{
                "id": effect.id,
                "stat": effect.stat,
                "value": effect.value,
                "modifier_type": effect.modifier_type,
                "duration": effect.duration,
                "targetsSelf": effect.targetsSelf,
                "applyer": effect.applyer,
                "displayName": effect.displayName
            } for effect in character.activeEffects],
            "effects": character.effects,
            "abilities": [
                {
                    "name": ability.name,
                    "lore": ability.lore,
                    "info": ability.info,
                    "cost": ability.cost,
                    "effect": [
                        {
                            "id": mod.id,
                            "stat": mod.stat,
                            "value": mod.value,
                            "modifier_type": mod.modifier_type,
                            "duration": mod.duration,
                            "targetsSelf": mod.targetsSelf,
                            "applyer": mod.applyer,
                            "displayName": mod.displayName
                        } for mod in ability.effect
                    ],
                    "type": ability.type,
                    "damage": ability.damage,
                    "cooldown": ability.cooldown
                } for ability in character.abilities
            ],
            "spells": [
                {
                    "name": spell.name,
                    "lore": spell.lore,
                    "info": spell.info,
                    "mp_cost": spell.mp_cost,
                    "effects": [
                        {
                            "id": mod.id,
                            "stat": mod.stat,
                            "value": mod.value,
                            "modifier_type": mod.modifier_type,
                            "duration": mod.duration,
                            "targetsSelf": mod.targetsSelf,
                            "applyer": mod.applyer,
                            "displayName": mod.displayName
                        } for mod in spell.effects
                    ],
                    "type": spell.type,
                    "damage": spell.damage,
                    "cooldown": spell.cooldown
                } for spell in character.spells
            ],
            "passives": character.passives,
            "equipment": character.equipment,
            "inventory": [{
                "type": item.type,
                "name": item.name,
                "data": item.data
            } for item in character.inventory],
            "active_modifiers": [
                {
                    "id": mod.id,
                    "stat": mod.stat,
                    "value": mod.value,
                    "modifier_type": mod.modifier_type,
                    "duration": mod.duration,
                    "targetsSelf": mod.targetsSelf,
                    "applyer": mod.applyer,
                    "displayName": mod.displayName
                } for mod in character.active_modifiers
            ],
            "turns": character.turns,
            "description": character.description
        }
    
    def get_available_options(self, keep_class: bool = False) -> List[Dict]:
        """
        Get the available move options for a character.
        Default Moves: Attack, Forfeit, Skip Turn
        Spells and Abilities are included as one option each.
        """

        options: List[Dict[str, Any]] = []

        attack: Dict[str, Any] = {
            "type": "action",
            "name": "Attack",
            "params": ["Target"]
        }

        options.append(attack)

        forfeit: Dict[str, Any] = {
            "type": "base",
            "name": "Forfeit",
            "params": []
        }

        options.append(forfeit)

        skip: Dict[str, Any] = {
            "type": "base",
            "name": "Skip Turn",
            "params": []
        }

        options.append(skip)

        spells = self.spells

        for spell in spells:
            # spell_type = spell.type
            should_have_target = spell.type in ["damage", "debuff"]

            params = []

            if should_have_target:
                params.append("Target")


            spell_item = {
                "type": "spell",
                "name": spell.name,
                "params": params,
                "info": spell if keep_class else spell.spell_to_json()
            }

            options.append(spell_item)


        abilities = self.abilities
        for ability in abilities:
            # spell_type = spell.type
            should_have_target = ability.type in ["damage", "debuff"]

            params = []

            if should_have_target:
                params.append("Target")


            ability_item = {
                "type": "ability",
                "name": ability.name,
                "params": params,
                "info": ability if keep_class else ability.ability_to_json()
            }

            options.append(ability_item)

        print(options)
        return options

    def get_cards(self) -> List[Dict[str, Any]]:

        cards = self.inventory
        cards_json: List[Dict[str, Any]] = []
        for card in cards:
            cards_json.append({
                "name": card.name,
                "type": card.type,
                "data": card.data
            })
            pass
        
        return cards_json
        

# The old Enemy class is now fully removed and replaced by a new version.

class Enemy(Character):
    def __init__(self, name, character_class, team, element, base_stats, character_data, stat_modifiers, activeEffects, effects, abilities, spells, passives, equipment, inventory, logic: Callable[['Enemy', List['Enemy'], List[Character]], Dict[str, Any]]):
        super().__init__(name, character_class, team, element, base_stats, character_data, stat_modifiers, activeEffects, effects, abilities, spells, passives, equipment, inventory, "")
        self.logic = logic
    
    def define_action(self, allies: List['Enemy'], enemies: List[Character], run_action = False) -> Dict[str, Any]:
        """
        Defines the action of the enemy character.
        Uses the self.logic function to determine the action.

        use run_action=True to run the action immediately
        """



        return self.logic(self, allies, enemies)

    pass



