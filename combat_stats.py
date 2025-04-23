# combat_stats provides tools to extract the moves and
# other stats required for simulating a battle
import requests
import json

pokemon_attributes = [
    "abilities", "base_experience", "cries", "forms", "game_indices", "height", "held_items", "id", "is_default",
    "location_area_encounters", "moves", "name", "order", "past_abilities", "past_types", "species", "sprites", "stats",
    "types", "weight"
]

def get_possible_moves(pokemon_name:str="",pokemon_id:int=-1,pokemon_level:int=1)->list:
    if pokemon_name == "" and pokemon_id == -1:
        raise ValueError("You must specify either name or id")
    pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name if pokemon_id == -1 else pokemon_id}/")
    if pokemon.status_code != 200:
        raise Exception(f"Invalid response, {pokemon.status_code}")
    pokemon_data = json.loads(pokemon.content)
    moves = []
    for entry in pokemon_data["moves"]:
        # get most recent entry - from the most recent game
        most_recent_version = entry["version_group_details"][-1]
        # only get moves it learns naturally
        if most_recent_version["move_learn_method"]["name"] == "level-up":
            if most_recent_version["level_learned_at"] <= pokemon_level:
                moves.append(entry["move"])
    return moves


def get_pokemon_stats(pokemon_name:str="",pokemon_id:int=-1,pokemon_level:int=1)->list:
    if pokemon_name == "" and pokemon_id == -1:
        raise ValueError("You must specify either name or id")
    pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name if pokemon_id == -1 else pokemon_id}/")
    if pokemon.status_code != 200:
        raise Exception(f"Invalid response, {pokemon.status_code}")
    pokemon_data = json.loads(pokemon.content)
    stats = []
    for s in pokemon_data["stats"]:
        stat = {"name" : s["stat"]["name"], "value" : s["base_stat"]}
        stats.append(stat)
    return stats


# Run this code to test if it works:
'''
a = get_pokemon_stats("geodude", pokemon_level=1)
print(a)'''
