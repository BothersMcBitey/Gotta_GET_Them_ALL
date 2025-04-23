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
