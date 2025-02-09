"""
This file contains logic for activating, storing and using Character Passives.
The variable passives: Dict[character: str, passives: Dict[passive: str, CharacterPassive]]

To obtain the passive for one character, you should use the use_passive() function within CharacterPassive. 
However, you may also run passives directly by running CharacterPassive.function
"""

from typing import Dict, Any, List, Optional, Callable

# from character import Character

def show_passive_warning(function_type, passive_name) -> None:
    print(f"[WARN] Could not find passive function {function_type} for {passive_name}.")
    print("When creating characters, make sure that all passive functions are added to the passives dictionary, even if they are empty.")


# turns out this was unneeded lol
# iguess it stays as a reference for now
@PendingDeprecationWarning
class CharacterPassive:
    """
    ### Passives
    Passives are special abilities that are automatically activated under certain conditions.
    They are stored in a dictionary, with the key being the character's name and the value being a dictionary of passives.

    ### Arguments
    #### onHit: Callable[[Character, Character], None] -> A function that is called when the character hits another character.
    1. character: Character
    2. target: Character
    #### onMissedHit: Callable[[Character, Character], None] -> A function that is called when the character misses a hit on another character.
    1. character: Character
    2. target: Character

    """

    def __init__(self, id: str, params: List[str], function):
        self.id = id
        self.params = params
        self.function = function
        pass

    def get_params(self) -> List[str]:
        return self.params

    def use_passive(self, function_params: Dict[str, Any]) -> Optional[Any]:
        """
        Uses this CharacterPassive of a character (by calling a function).
        function_params: Dict[str, Any] -> A list of key-pair values, matching exactly the name of the function arguments
        Example:
        self.function = def someFunc(arg_1: str, arg_2: int) -> str
        CharacterPassive.use_passive(function_params={
            "arg_1": "some_argument",
            "arg_2": 1234
        })

        Using any other format raises a ValueError.

        Function called: self.function.
        returns Optional[Any] -> The result of the function, if any.
        """

        for param in function_params:
            print(f"The param was: {param}")
            # print(f"The param2 was: {param2}")
            pass
        try:
            self.function()
        except: print("An error occurred when calling the function")

    pass

# passives: Dict[str, Dict[str, Dict[str, Any]]] = {
#     "guardian": {
#         "onHit": guardian.onHit,
#         "onMissedHit": guardian.onMissedHit,
#         "onKill": guardian.onKill
#     }
# }

# def get_character_passives(character: Character):
    
#     passives_key = character.passives


#     pass


# def get_passives_by_string(passives_key: str):
#     pass

def get_before_passive_function(passive_name: str, function_type: str) -> (Callable[..., Dict[str, Any]] | None):
    """
    Retrieves a "before{Action}" passive function from the passives dictionary.
    
    ### Args:
        passive_name (str): The key name of the passive (e.g. "guardian")
        function_type (str): The type of function to retrieve (e.g. "onDeath", "onHit")
        
    ### Returns:
        Optional[Callable]: The passive function if it exists, None otherwise
    """

    # This is not ideal, but it will do for now.
    from char_passives import passives

    try:
        return passives[passive_name][function_type]
    except:
        show_passive_warning(function_type, passive_name)
    return None

def get_passive_function(passive_name: str, function_type: str) -> (Callable[..., None] | None):
    """
    Retrieves a passive function from the passives dictionary.
    
    ### Args:
        passive_name (str): The key name of the passive (e.g. "guardian")
        function_type (str): The type of function to retrieve (e.g. "onDeath", "onHit")
        
    ### Returns:
        Optional[Callable]: The passive function if it exists, None otherwise
    """

    # This is not ideal, but it will do for now.
    from char_passives import passives

    try:
        return passives[passive_name][function_type]
    except:
        show_passive_warning(function_type, passive_name)
    return None

# def use_test_passive(target = "", attacker = ""):
#     print("Test Passive Activated!")
#     pass

# test_passive = CharacterPassive("onKill", ["target", "attacker"], use_test_passive)

# test_passive.use_passive({
#     "target": "bob",
#     "attacker": "bob's enemy"
# })