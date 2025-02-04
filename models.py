from typing import List, Dict, Any, Optional

from pydantic import BaseModel, Field


class PydanticCharacter(BaseModel):
    name: str
    character_class: str
    team: str
    element: str
    base_stats: dict[str, Any]
    stat_modifiers: List[Dict]
    activeEffects: Dict[str, Any]
    effects: List[Dict[str, Any]]
    abilities: List[Dict]
    spells: List[Dict]
    passives: Dict[str, Any]
    equipment: List[Dict[str, Any]]
    inventory: List[Dict[str, Any]]
    description: Optional[str] = Field(default="")  # Default to an empty string
    active_modifiers: List[Dict] = Field(default_factory=list)  # Initialize as empty list
    turns: int = Field(default=0)  # Default to 0
