# combat_stats provides tools to extract the moves and
# other stats required for simulating a battle
import requests
import json

# HELPER CODE ==========================================================================================================
pokemon_attributes = [
    "abilities", "base_experience", "cries", "forms", "game_indices", "height", "held_items", "id", "is_default",
    "location_area_encounters", "moves", "name", "order", "past_abilities", "past_types", "species", "sprites", "stats",
    "types", "weight"
]

def _get_data(object_type:str, object_name:str= "", object_id:int=-1)->dict:
    if object_name == "" and object_id == -1:
        raise ValueError(f"You must specify either name or id. Received {object_name} and {object_id}")
    data = requests.get(f"https://pokeapi.co/api/v2/{object_type}/{object_name if object_id == -1 else object_id}/")
    if data.status_code != 200:
        raise Exception(f"Invalid response, {data.status_code}")
    return json.loads(data.content)

# EXTERNAL METHODS =====================================================================================================
def get_possible_moves(pokemon_name:str="", pokemon_id:int=-1, pokemon_level:int=1)->list:
    pokemon_data = _get_data("pokemon", object_name=pokemon_name, object_id=pokemon_id)
    moves = []
    for entry in pokemon_data["moves"]:
        # get most recent entry - from the most recent game
        most_recent_version = entry["version_group_details"][-1]
        # only get moves it learns naturally
        if most_recent_version["move_learn_method"]["name"] == "level-up":
            if most_recent_version["level_learned_at"] <= pokemon_level:
                moves.append(entry["move"])
    return moves

def get_pokemon_stats(pokemon_name:str="", pokemon_id:int=-1)->list:
    pokemon_data = _get_data("pokemon", object_name=pokemon_name, object_id=pokemon_id)
    stats = []
    for s in pokemon_data["stats"]:
        stat = {"name" : s["stat"]["name"], "value" : s["base_stat"]}
        stats.append(stat)
    return stats

def get_move_stats(move_name:str="", move_id:int=-1)->dict:
    move_data = _get_data("move", object_name=move_name, object_id=move_id)
    stats = {
        "accuracy" : move_data["accuracy"],
        "power" : move_data["power"],
        "type" : move_data["type"],
        "pp" : move_data["pp"],
        "name" : move_data["name"]
    }
    return stats


# Run this code to test if it works:
#print(get_move_stats("pound"))
#print(get_pokemon_stats("geodude"))


