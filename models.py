from pydantic import BaseModel
from typing import List, Dict, Any

class PlayerState(BaseModel):
    name: str
    character_class: str
    trait: str
    health: int = 100
    inventory: List[str] = []

class NPCState(BaseModel):
    name: str
    mood: str = "neutral"
    relationship_with_player: int = 50

class GameState(BaseModel):
    player_state: PlayerState
    npc_states: Dict[str, NPCState] = {}
    story_log: List[str] = []
    world_state: Dict[str, Any] = {}