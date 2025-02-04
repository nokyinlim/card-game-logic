import json
from typing import List

from character import StatModifier, Character, Ability, Spell, Equipment
# import mods
import defaults

from shared_game_data import characters, playerCharacters, enemyCharacters
from models import *
from utils import *




def action_attack(character_name: str, game_code: str, target_name: str, target_type: str = "characters", character_type: str = "characters") -> bool:
    # target_name = input(f"Who do you want to attack? ({', '.join(c.name for c in characters if c != character)}): ") if not target_name else target_name
    # target = next(c for c in characters if c.name.lower() == target_name.lower())

    games = readGames()
    cGame = games[game_code]
    characters = cGame[character_type]
    index = 0
    for i, char in enumerate(characters):
        if char["name"] == character_name:
            index = i

    attackerCharIndex = 0
    targetCharIndex = 1
    for i, character in enumerate(games[game_code]["characters"]):
        if character["name"] == character_name:
            attackerCharIndex = i
        if character["name"] == target_name:
            targetCharIndex = i

    targetIndex = 0
    targets = cGame[target_type]
    for i, tar in enumerate(targets):
        if tar["name"] == target_name:
            targetIndex = i

    print(characters)
    target = getCharacterFromDict(targets[targetIndex])
    character = getCharacterFromDict(characters[index])

    attackRes = character.attack(target, element=character.element)
    print("attack\n", attackRes)
    didHit = attackRes["didHit"]
    character: Character = attackRes["self"]
    target: Character = attackRes["target"]
    if didHit:
        try:
            character["passives"]["onHit"](character, target)
        except:
            pass
    else:
        try:
            character["passives"]["onMissedHit"](character, target)
        except:
            pass
    print(target.base_stats["health"])
    print(target.character_to_json())
    games[game_code][target_type][targetIndex] = target.character_to_json()
    games[game_code]["characters"][attackerCharIndex] = character.character_to_json()
    games[game_code]["characters"][targetCharIndex] = target.character_to_json()
    games[game_code][character_type][index] = character.character_to_json()

    print(target.character_to_json()["base_stats"]["health"])
    writeGames(games)
    return True

def select_character(characters, character, message, can_self_select=True):
    selected = False
    while not selected:
        target_name = input(f"{message}({', '.join(c.name for c in characters if (c != character or can_self_select))}): ")
        try:
            target = next(c for c in characters if c.name.lower() == target_name.lower())
            selected = True
        except StopIteration:
            print("Target is invalid!")
    return target

def mainLoopAbilityAction(targets, ability: Ability, character: Character, characters: List[Character], enemyCharacters: List[Character], playerCharacters: List[Character]) -> List[Character]:
    match ability.type:
        case "modifier":
            try:
                character.passives["ability"](character, ability)
            except:
                pass
            character.use_ability(ability)
        case "damage":
            if not ability.damage["targets"]:
                print(enemyCharacters)
                target = select_character(enemyCharacters, character, "Select Target - ", False)
                character.use_ability(ability, [target])
                targets.append(target)
            else:
                match ability.damage["targets"]:
                    case "all":
                        character.use_ability(ability, characters)
                        targets = characters
                    case "enemies":
                        character.use_ability(ability, enemyCharacters)
                        targets = enemyCharacters
                    case "allies":
                        character.use_ability(ability, playerCharacters)
                        targets = playerCharacters
    return targets
    

def mainAction(params: dict, action: str, character: Character, characters: List[Character], enemyCharacters: List[Character], playerCharacters: List[Character]):

    # for i in range(50):
    #     targetCharacter = defaults.generate_random_character(playerCharacters)
    #     print(f"{targetCharacter.name}")

    if character.team == "player":
        playerTeam = "player"
        enemyTeam = "enemy"
    else: 
        playerTeam = "enemy"
        enemyTeam = "player"

    print("-" * 30)
    character.display_character_stats()
    turnEnded = False
    while not turnEnded:
        try: character.passives["onTurnStart"](character)
        except: pass

        # action = input(f"{character.name}, choose an action (attack, use ability, cast spell, show description, skip, forfeit): ").strip().lower()

        if action == "forfeit":
            return False

        if action == "attack":
            try: targetName = params["target"]
            except KeyError: print("no target")
            turnEnded = action_attack(character, params['target'])

        elif "ability" in action:
            try: 
                targets = params["targets"]
                ability_name = params["ability"]
            except KeyError: print("no targets or ability")

            if not character.abilities:
                print(f"{character.name} has no abilities!")
                continue
            # ability_name = input(f"Choose an ability: {'\n'.join((ability.name + (('\n' + ability.lore) if ability.lore else "") + (('\n' + ability.info) if ability.info else "")) for ability in character.abilities)}\n")
            ability = next(a for a in character.abilities if a.name.lower() == ability_name.lower())
            
            if ability.cooldown == 0:
                targets = mainLoopAbilityAction(targets, ability, character, characters, enemyCharacters, playerCharacters)
                try:
                    character.passives["onAbility"](character, ability, targets)
                except: pass
                turnEnded = True
            else:
                try: cooldown = character.base_stats[ability.name]
                except: cooldown = ability.cooldown
                if cooldown > 0:
                    print("Ability is on Cooldown! Choose another action.")
                else:
                    targets = mainLoopAbilityAction(targets, ability, character, characters, enemyCharacters, playerCharacters)
                    character.base_stats[ability.name] = ability.cooldown
                    try:
                        character.passives["onAbility"](character, ability, targets)
                    except: pass
                    turnEnded = True
                    pass
                

        elif "spell" in action:
            if not character.spells:
                print(f"{character.name} has no spells!")
                continue
            spell_name = input(f"Choose a spell:\n{'\n'.join((spell.name + (('\n' + spell.lore) if spell.lore else "") + (('\n' + spell.info) if spell.info else "")) for spell in character.spells)}\n")
            spell = next(s for s in character.spells if s.name.lower() == spell_name.lower())
            targets = []
            match spell.type:
                case "modifier":
                    character.cast_spell(spell)
                case "damage":
                    if not spell.damage["targets"]:
                        target = select_character(enemyCharacters, character, "Select Target - ", False)
                        character.cast_spell(spell, [target])
                        targets.append(target)
                    else:
                        match spell.damage["targets"]:
                            case "all":
                                character.cast_spell(spell, characters)
                                targets = characters
                            case "enemies":
                                character.cast_spell(spell, enemyCharacters)
                                targets = enemyCharacters
                            case "allies":
                                character.cast_spell(spell, playerCharacters)
                                targets = playerCharacters
            try:
                character.passives["onSpell"](character, spell, targets)
            except: pass
            turnEnded = True

        elif "equip" in action:
            print("Equipping Basic Sword")
            # character.equip(basic_sword)

        elif "skip" in action:
            turnEnded = True

        elif "description" in action:
            print(character.description)
        
        # Check if any character is dead
        for c in characters:
            if c.base_stats['health'] <= 0:
                print(f"{c.name} has been defeated!")
                try:
                    character.passives["onKill"](character)
                except:
                    pass



                characters.remove(c)
                if c.team == "player":
                    playerCharacters.remove(c)
                else:
                    enemyCharacters.remove(c)

            if playerCharacters == []:
                for enemy in enemyCharacters:
                    try:
                        enemy.passives["onBattleWon"](enemy, enemyCharacters, playerCharacters)
                    except: pass
                print("There are no more players left, the enemies have won!")
                return False
            elif enemyCharacters == []:
                for player in playerCharacters:
                    try:
                        player.passives["onBattleWon"](player, playerCharacters, enemyCharacters)
                    except: pass
                print("There are no more enemies left, the players have won!")
                return False

    character.end_turn()

    print("-" * 30)
    # else: # Enemy AI
    #     # enemy AI
    #     # for now, attack every move
    #     # select a target
    #     print("-" * 30)
    #     print(f"{character.name}: {character.base_stats["health"]} HP")

    #     # print(playerCharacters)
    #     target = defaults.generate_random_character(playerCharacters)
    #     print(target.name)
    #     didHit = character.attack(target, element=character.element)
    #     if didHit:
    #         try:
    #             character.passives["onKill"](character)
    #         except:
    #             pass

        

    #     for c in characters:
    #         if c.base_stats['health'] <= 0:
    #             print(f"{c.name} has been defeated!")
    #             try:
    #                 character.passives["onKill"](character)
    #             except:
    #                 pass
    #             characters.remove(c)
    #             if c.team == "player":
    #                 playerCharacters.remove(c)
    #             else:
    #                 enemyCharacters.remove(c)
    #         if playerCharacters == []:
    #             for enemy in enemyCharacters:
    #                 try:
    #                     enemy.passives["onBattleWon"](enemy, enemyCharacters, playerCharacters)
    #                 except: pass

    #             print("There are no more players left, the enemies have won!")
    #             return False
    #         elif enemyCharacters == []:
    #             for player in playerCharacters:
    #                 try:
    #                     player.passives["onBattleWon"](player, playerCharacters, enemyCharacters)
    #                 except: pass
    #             print("There are no more enemies left, the players have won!")
    #             return False

    #     character.end_turn()

    #     print("-" * 30)
    return True

# if __name__ == "__main__":
# main()