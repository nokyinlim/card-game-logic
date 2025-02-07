
import random
from typing import Dict, List
# from character import Character


def generate_random_character(characters):
    # Extract weights and characters
    weights = [character.get_stat("weight") for character in characters]
    for character in characters:
        print(f"Weight of {character.name}: {character.get_stat("weight")}")
    selected_character = random.choices(characters, weights=weights, k=1)[0]
    return selected_character


def calculate_effective_damage(damage, defense) -> float:
    # Calculate the damage reduction percentage
    damage_reduction_percentage = defense / (defense + 50)
    
    # Calculate the effective damage
    effective_damage = damage * (1 - damage_reduction_percentage)
    
    return effective_damage

def remove_dict_with_key_value(dict_list, key, value) -> Dict:
    # Use list comprehension to filter out the dictionary with the specific key-value pair
    return [d for d in dict_list if d.get(key) != value]


def remove_instance_with_property(instance_list, property_name, value) -> Dict:
    # Use list comprehension to filter out the instance with the specific property value
    return [instance for instance in instance_list if getattr(instance, property_name) != value]


def chance_to_be_true(percentage) -> bool:
    if not (0 <= percentage <= 100):
        raise ValueError("Percentage must be between 0 and 100.")
    
    return random.random() < (percentage / 100)

default_user_stats: Dict = {
    "win_fight": 0,
    "lose_fight": 0,
    "draw_fight": 0,
    "deal_damage": 0,
    "take_damage": 0,
    "heal_damage": 0,
    "reduce_taken_damage": 0,
    "deal_damage_fire": 0,
    "deal_damage_earth": 0,
    "deal_damage_water": 0,
    "deal_damage_thunder": 0,
    "deal_damage_air": 0,
    "deal_damage_neutral": 0,
    "deal_damage_shadow": 0,
    "deal_damage_light": 0,
    "deal_damage_physical": 0,
    "deal_damage_magic": 0,
    "deal_damage_true": 0,
    "use_ability": 0,
    "use_spell": 0,
    "use_card": 0,
    "apply_buff": 0,
    "apply_debuff": 0,
    "success_attack": 0,
    "miss_attack": 0,
    "critical_attack": 0,
    "block_attack": 0,
    "dodge_attack": 0,
    "armor_points_ignored": 0,
    "skill_damage": 0,
    "spell_damage": 0,
    "skill_points_used": 0,
    "spell_points_used": 0,
    "turn_skip": 0,
    "damage_record": 0
}