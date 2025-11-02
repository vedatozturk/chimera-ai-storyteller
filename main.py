import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from models import GameState, PlayerState, NPCState
from ai_service import model

app = FastAPI(
    title="Chimera Project API",
    description="Bir yapay zeka hikaye anlatıcısı için backend servisi.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Action(BaseModel):
    action: str

def create_prompt(current_state: GameState, user_action: Action) -> str:
    prompt = f"""
Sen, Chimera adında usta bir oyun yöneticisisin. Karanlık ve gizemli bir fantezi dünyasını yönetiyorsun.
Görevin, oyuncunun verdiği kararlara ve mevcut duruma göre hikayeyi devam ettirmek VE oyun durumunu güncellemektir.

--- MEVCUT DURUM ---
{current_state.model_dump_json(indent=2)}

--- OYUNCU EYLEMİ ---
{user_action.action}
---

Yukarıdaki duruma göre hikayenin bir sonraki adımını yaz ve oyun durumunu (GameState) güncelle.
Cevabın SADECE aşağıdaki formatta bir JSON objesi olmalı, başka hiçbir metin ekleme:

{{
  "new_story_text": "Buraya hikayenin yeni bölümünü yaz.",
  "updated_player_state": {{
    "health": 100,
    "inventory": ["Eşya 1", "Eşya 2"]
  }},
  "updated_npc_states": {{
    "Hancı Barlok": {{
        "mood": "kizgin",
        "relationship_with_player": 40
    }}
  }},
  "updated_world_state": {{
    "kapi_acik": true,
    "canavar_oldu": false
  }}
}}
"""
    return prompt

@app.get("/")
async def root():
    return {"message": "Chimera API is running with AI Brain v2 (JSON Aware)!"}

@app.post("/turn")
async def handle_turn(current_state: GameState, user_action: Action) -> GameState:
    if model is None:
        current_state.story_log.append("HATA: Yapay zeka modeli yüklenemedi.")
        return current_state
        
    prompt = create_prompt(current_state, user_action)
    response = model.generate_content(prompt)
    
    try:
        clean_response_text = response.text.strip().replace("```json", "").replace("```", "")
        ai_data = json.loads(clean_response_text)
        
        current_state.story_log.append(ai_data.get("new_story_text", "Yapay zeka hikaye üretemedi."))
        
        if "updated_player_state" in ai_data:
            player_update = ai_data.get("updated_player_state", {})
            current_state.player_state.health = player_update.get("health", current_state.player_state.health)
            current_state.player_state.inventory = player_update.get("inventory", current_state.player_state.inventory)

        if "updated_npc_states" in ai_data:
            npc_updates = ai_data.get("updated_npc_states", {})
            for npc_name, updates in npc_updates.items():
                if npc_name in current_state.npc_states:
                    current_state.npc_states[npc_name].mood = updates.get("mood", current_state.npc_states[npc_name].mood)
                    current_state.npc_states[npc_name].relationship_with_player = updates.get("relationship_with_player", current_state.npc_states[npc_name].relationship_with_player)
                else:
                    current_state.npc_states[npc_name] = NPCState(
                        name=npc_name,
                        mood=updates.get("mood", "neutral"),
                        relationship_with_player=updates.get("relationship_with_player", 50)
                    )

        if "updated_world_state" in ai_data:
            world_updates = ai_data.get("updated_world_state", {})
            current_state.world_state.update(world_updates)

    except (json.JSONDecodeError, AttributeError, KeyError) as e:
        error_message = f"Yapay zeka geçersiz bir cevap formatı döndürdü: {e}"
        print(error_message) 
        current_state.story_log.append(response.text)
        current_state.story_log.append("(Sistem Notu: Yapay zeka ile iletişimde bir format hatası oluştu.)")

    return current_state
