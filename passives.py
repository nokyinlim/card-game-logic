
from typing import Dict, Any, List, Optional

# from character import Character

# import guardian

class CharacterPassive:
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


def get_passives_by_string(passives_key: str):
    pass

def use_test_passive(target = "", attacker = ""):
    print("Test Passive Activated!")
    pass

test_passive = CharacterPassive("onKill", ["target", "attacker"], use_test_passive)

test_passive.use_passive({
    "target": "bob",
    "attacker": "bob's enemy"
})