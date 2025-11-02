import json
import requests
from models import GameState, PlayerState

API_URL = "http://127.0.0.1:8000"

def create_character() -> GameState:
    print("--- CHIMERA: Adaptif Hikaye Anlatıcısı ---")
    print("Maceraya başlamadan önce karakterini yaratalım.")
    
    name = input("Karakterinin ismi ne olsun?: ")
    print("\nBir sınıf seç:\n1: Savaşçı\n2: Büyücü\n3: Haydut")
    class_choice = input("Seçim (1, 2 veya 3): ")
    print("\nBir karakter özelliği seç:\n1: Cesur\n2: Meraklı\n3: Kurnaz")
    trait_choice = input("Seçim (1, 2 veya 3): ")

    class_map = {"1": "Savaşçı", "2": "Büyücü", "3": "Haydut"}
    trait_map = {"1": "Cesur", "2": "Meraklı", "3": "Kurnaz"}

    player_data = PlayerState(
        name=name.strip(),
        character_class=class_map.get(class_choice, "Savaşçı"),
        trait=trait_map.get(trait_choice, "Cesur")
    )

    initial_game_state = GameState(player_state=player_data)
    initial_game_state.story_log.append(f"Maceran başlıyor, {player_data.name}!")

    print("\n--- Karakter Yaratıldı! ---")
    print(f"Hoş geldin, {player_data.name}! Sen {player_data.trait} bir {player_data.character_class}'sın.")
    print(initial_game_state.story_log[-1])

    return initial_game_state

if __name__ == "__main__":
    game_state = create_character()

    while True:
        action_text = input("> ")

        if action_text.lower() in ["çık", "exit", "quit"]:
            print("Görüşmek üzere!")
            break
        
        try:
            payload = {
                "current_state": json.loads(game_state.model_dump_json()),
                "user_action": {"action": action_text}
            }

            response = requests.post(f"{API_URL}/turn", json=payload)
            response.raise_for_status()

            new_state_data = response.json()
            game_state = GameState(**new_state_data)

            print(game_state.story_log[-1])

        except requests.exceptions.RequestException as e:
            print(f"\n!!! Sunucuya bağlanırken bir hata oluştu: {e}")
            print("Sunucunun (uvicorn main:app --reload) çalıştığından emin misin?\n")