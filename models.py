from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class PydanticCharacter(BaseModel):
    name: str
    character_class: str
    team: str
    element: str
    base_stats: Dict[str, Any]
    character_data: Dict[str, Any]
    stat_modifiers: List[Dict[str, Any]]  # List of StatModifier as dicts
    activeEffects: Dict[str, Any]
    effects: List[Dict[str, Any]]
    abilities: List[Dict[str, Any]]  # List of Ability as dicts
    spells: List[Dict[str, Any]]  # List of Spell as dicts
    passives: str
    equipment: List[Dict[str, Any]]
    inventory: List[Dict[str, Any]]  # List of Card as dicts
    description: str = Field(default="")
    active_modifiers: List[Dict[str, Any]] = Field(default_factory=list)  # List of active StatModifier as dicts
    turns: int = Field(default=0)
