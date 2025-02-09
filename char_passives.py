from classes.guardian import passives as guardian_passives
from classes.character_general import passives as character_passives

from typing import Dict, Any, Callable

passives: Dict[str, Dict[str, Dict[str, Any]]] = {
    "guardian": guardian_passives,
    "character": character_passives
}

# Circular imports are annoying
@DeprecationWarning
def get_passive_function(passive_name: str, function_type: str) -> Callable[..., None]:
    """
    Retrieves a passive function from the passives dictionary.
    
    ### Args:
        passive_name (str): The key name of the passive (e.g. "guardian")
        function_type (str): The type of function to retrieve (e.g. "onDeath", "onHit")
        
    ### Returns:
        Optional[Callable]: The passive function if it exists, None otherwise
    """
    try:
        return passives[passive_name][function_type]
    except:
        print(f"Could not find passive function {function_type} for {passive_name}")
        return None