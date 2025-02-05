from character import Character, StatModifier, Equipment, Card, Ability, Spell

new_character = Character(
    name="Electric-Mage",
    character_class="Mage",
    team="string",
    element="electric",
    base_stats={
        "health": 60,
        "max_health": 60,
        "mp": 60,
        "max_mp": 60,
        "spell_damage": 30,
        "attack_damage": 15,
        "critical_chance": 0.05,
        "defense": 10,
        "magic_defense": 15,
        "skill_points": 5,
        "max_skill_points": 5,
        "accuracy": 40,
        "agility": 15
    },
    stat_modifiers=[],
    activeEffects=[],
    effects=[],
    abilities=[
        Ability(
            name="Charge",
            description="",
            lore="Increase spell damage during the next 3 turns.",
            cost=5,
            effect=[StatModifier(
                id = "charge.spell_damage",
                stat="spell_damage",
                value=0.2,
                modifier_type="multiply_base",
                duration=3,
                targetsSelf=True
            )]
        )
    ], spells=[Spell(
        name="Thunderstrike",
        lore="Unleashes a massive thunderbolt dealing major Thunder-type damage to 1 Target.",
        info="Afterward, decreases own defense and can no longer cast spells for 1 turn.",
        mp_cost=10,
        effects=[StatModifier(
            id="thunderstrike.defense_power_down",
            stat="defense",
            value=-10,
            modifier_type="add",
            duration=1,
            targetsSelf=True
        )],
        type="damage",
        damage={
            "damage": 30,
            "element": "thunder",
            "targets": "1"
        }
    ), Spell(
        name="Static Ignition",
        lore="A spark of electricity deals minor Thunder-type damage that ignites the target, dealing True damage over time.",
        info="",
        mp_cost=5,
        effects=[StatModifier(
            id="static_ignition.damage",
            stat="health",
            value=-5,
            modifier_type="add",
            duration=3,
            targetsSelf=False
        )],
        type="damage",
        damage={
            "damage": -20,
            "element": "thunder",
            "targets": ""
        }
    )]
)