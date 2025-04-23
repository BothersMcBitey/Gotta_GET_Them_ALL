import requests
import json
import random

# Get the list of Pokémon from the API
url = 'https://pokeapi.co/api/v2/pokemon/'
response = requests.get(url)
pokemon_list = json.loads(response.text)['results']

# Create a list of Pokémon names for easy validation
pokemon_names = [pokemon['name'] for pokemon in pokemon_list]

# Print available Pokémon
print("Available Pokémon:")
for name in pokemon_names:
    print(name)

# Choose game mode
while True:
    mode = input("Choose game mode: 1 Player (1) or 2 Player (2): ").strip()
    if mode in ['1', '2']:
        break
    else:
        print("Invalid input. Please enter 1 or 2.")

# Function to get a player's Pokémon
def get_player_pokemon(player_name):
    while True:
        choice = input(f"{player_name}, would you like a random Pokémon (R) or choose (C)? ").upper()
        if choice == 'R':
            pokemon = random.choice(pokemon_names)
            print(f"{player_name} chose: {pokemon}")
            return pokemon
        elif choice == 'C':
            while True:
                pokemon = input(f"{player_name}, enter your Pokémon: ").lower()
                if pokemon in pokemon_names:
                    print(f"{player_name} chose: {pokemon}")
                    return pokemon
                else:
                    print("Invalid Pokémon name. Please enter a valid Pokémon from the list.")
        else:
            print("Invalid input, please write R or C.")

# Game logic
if mode == '1':
    user_pokemon = get_player_pokemon("User")
    cpu_pokemon = random.choice(pokemon_names)
    print(f"CPU chose: {cpu_pokemon}")
else:
    player1_pokemon = get_player_pokemon("Player 1")
    player2_pokemon = get_player_pokemon("Player 2")




def get_possible_moves(pokemon_name:str="",pokemon_id:int=-1,pokemon_level:int=1)->list:
    if pokemon_name == "" and pokemon_id == -1:
        raise ValueError("You must specify either name or id")
    pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name if pokemon_id == -1 else pokemon_id}/")
    if pokemon.status_code != 200: raise Exception(f"Invalid response, {pokemon.status_code}")
    pokemon_moves_data = json.loads(pokemon.content)
    moves = []
    for entry in pokemon_moves_data["moves"]:
        # get most recent entry - from the most recent game
        most_recent_version = entry["version_group_details"][-1]
        # only get moves it learns naturally
        if most_recent_version["move_learn_method"]["name"] == "level-up":
            if most_recent_version["level_learned_at"] <= pokemon_level:
                moves.append(entry["move"])
    return moves

# Run this code to test if it works:

user_moves = get_possible_moves(user_pokemon, pokemon_level=1)
# Extract just the names
user_move_names = [move['name'] for move in user_moves]

# Print the move names
print("User's available moves:")
for move_name in user_move_names:
    print(f"- {move_name}")

while True:
    chosen_move = input("Choose your move from the list above: ").lower()
    if chosen_move in user_move_names:
        print(f"User used {chosen_move}!")
        break
    else:
        print("Invalid move. Please choose a valid move from the list.")



