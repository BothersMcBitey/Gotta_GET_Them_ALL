import requests
import json
import random
import combat_stats as cs

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

# Get Pokémon choices
if mode == '1':
    user_pokemon = get_player_pokemon("User")
    cpu_pokemon = random.choice(pokemon_names)
    print(f"CPU chose: {cpu_pokemon}")

    # Get moves
    user_moves = cs.get_possible_moves(user_pokemon, pokemon_level=1)
    cpu_moves = cs.get_possible_moves(cpu_pokemon, pokemon_level=1)

    user_move_names = [move['name'] for move in user_moves]
    cpu_move_names = [move['name'] for move in cpu_moves]

    # User picks move
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

    # CPU picks random move
    if cpu_move_names:
        cpu_move = random.choice(cpu_move_names)
        print(f"CPU used {cpu_move}!")
    else:
        print("CPU has no available moves.")

else:
    player1_pokemon = get_player_pokemon("Player 1")
    player2_pokemon = get_player_pokemon("Player 2")

    # Get moves
    p1_moves = cs.get_possible_moves(player1_pokemon, pokemon_level=1)
    p2_moves = cs.get_possible_moves(player2_pokemon, pokemon_level=1)

    p1_move_names = [move['name'] for move in p1_moves]
    p2_move_names = [move['name'] for move in p2_moves]

    # Player 1 move selection
    print("Player 1's available moves:")
    for move_name in p1_move_names:
        print(f"- {move_name}")

    while True:
        p1_chosen_move = input("Player 1, choose your move from the list above: ").lower()
        if p1_chosen_move in p1_move_names:
            print(f"Player 1 used {p1_chosen_move}!")
            break
        else:
            print("Invalid move. Please choose a valid move from the list.")

    # Player 2 move selection
    print("Player 2's available moves:")
    for move_name in p2_move_names:
        print(f"- {move_name}")

    while True:
        p2_chosen_move = input("Player 2, choose your move from the list above: ").lower()
        if p2_chosen_move in p2_move_names:
            print(f"Player 2 used {p2_chosen_move}!")
            break
        else:
            print("Invalid move. Please choose a valid move from the list.")
