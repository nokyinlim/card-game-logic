from character import StatModifier, Character, Ability, Spell

# Example usage

# Sample Stat Modifiers
modifier1 = StatModifier(id="mod1", stat="attack_damage", value=5, modifier_type="add")
modifier2 = StatModifier(id="mod2", stat="defense", value=0.2, modifier_type="multiply_base")
modifier3 = StatModifier(id="mod3", stat="agility", value=0.1, modifier_type="multiplicative")

# Sample Abilities and Spells
ability1 = Ability(name="Power Strike", cost=2, effect=modifier1)
spell1 = Spell(name="Shield", mp_cost=5, effect=modifier2)

# Sample Character
character1 = Character(
    name="Warrior",
    character_class="Warrior",
    element="earth",
    base_stats={
        "health": 100,
        "max_health": 100,
        "mp": 30,
        "max_mp": 30,
        "attack_damage": 15,
        "critical_chance": 0.1,
        "defense": 10,
        "magic_defense": 5,
        "skill_points": 10,
        "max_skill_points": 10
    },
    stat_modifiers=[modifier1, modifier2],
    effects=[],
    abilities=[ability1],
    spells=[spell1],
    equipment=[],
    inventory=[]
)

# Display stats before using abilities and spells
character1.display_character_stats()

# Use ability and cast spell
character1.use_ability(ability1)
character1.cast_spell(spell1)

# Display stats after using abilities and spells
character1.display_character_stats()