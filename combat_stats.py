# combat_stats provides tools to extract the moves and
# other stats required for simulating a battle
import requests

def get_possible_moves(pokemon_name:str="",pokemon_id:int=-1)->dict:
    if pokemon_name == "" and pokemon_id == -1:
        raise ValueError("You must specify either name or id")
    pass

pkm = requests.get("https://pokeapi.co/api/v2/pokemon/geodude/")

print(pkm)