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

def _get_data(object_type:str, name:str= "", id:int=-1)->dict:
    if name == "" and id == -1:
        raise ValueError("You must specify either name or id")
    data = requests.get(f"https://pokeapi.co/api/v2/{object_type}/{name if id == -1 else id}/")
    if data.status_code != 200:
        raise Exception(f"Invalid response, {data.status_code}")
    return json.loads(data.content)

# EXTERNAL METHODS =====================================================================================================
def get_possible_moves(pokemon_name:str="", pokemon_id:int=-1, pokemon_level:int=1)->list:
    pokemon_data = _get_data("pokemon", pokemon_name, pokemon_id)
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
    pokemon_data = _get_data("pokemon", pokemon_name, pokemon_id)
    stats = []
    for s in pokemon_data["stats"]:
        stat = {"name" : s["stat"]["name"], "value" : s["base_stat"]}
        stats.append(stat)
    return stats

def get_move_stats(move_name:str="", move_id:int=-1)->list:
    move_data = _get_data("move", move_name, move_id)
    stats = []
    for key in ["accuracy", "power", "type", "pp", "name"]:
        stats.append({key : move_data[key]})
    return stats


# Run this code to test if it works:
'''
print(get_move_stats("pound"))
a = get_pokemon_stats("geodude", pokemon_level=1)
print(a)'''
