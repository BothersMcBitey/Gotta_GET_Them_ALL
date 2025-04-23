import requests
import json
import random
import combat_stats as cs

# only global variable, because GET requests are slow ==================================================================
list_of_pokemon_names = ""

def get_choice(message:str, options:list=["y","n"], error_message:str="Invalid input. Try again.",
               random_choice:bool=False)->str:
    options_string = "("
    for i in range(len(options)):
        options[i] = options[i].lower()
        options_string += options[i] +  " / "
    options_string = options_string[:-3] + ")"
    while True:
        print(message)
        print(options_string)
        if random_choice:
            return random.choice(options)
        else:
            response = input("> ").strip().lower()
            if response in options:
                return response
            else:
                print(error_message)

def get_pokemon_names()->list:
    # Get the list of Pokémon from the API
    url = 'https://pokeapi.co/api/v2/pokemon/'
    response = requests.get(url)
    pokemon_list = json.loads(response.text)['results']
    # Create a list of Pokémon names for easy validation
    pokemon_names = [pokemon['name'] for pokemon in pokemon_list]
    return pokemon_names

# Function to get a player's Pokémon
def get_player_pokemon(player_name)->str:
    is_random = get_choice(f"{player_name}, would you like a random Pokémon (r) or choose your own (c)?",
                           ["r","c"], "Invalid input, please write R or C.")
    pokemon = None
    if is_random == 'r':
        pokemon = random.choice(list_of_pokemon_names)
    elif is_random == 'c':
        pokemon = get_choice(f"{player_name}, choose your Pokémon:", list_of_pokemon_names,
                             "Invalid Pokémon name. Please enter a valid Pokémon from the list.")
    else:
        raise Exception("Invalid choice given. Somehow.")
    print(f"{player_name} chose: {pokemon.capitalize()}")
    return pokemon

def play_game(game_mode:int=1)->None:
    player_dict = {
        "name" : "",
        "pokemon" : "",
        "moves" : [],
        "move_names" : []
    }
    player_one = player_dict.copy()
    player_two = player_dict.copy()
    players = [player_one, player_two]

    # Get player's names
    player_one["name"] = input("Player one, what is your name?\n> ")
    if game_mode == 1:
        player_two["name"] = "CPU"
    elif game_mode == 2:
        player_two["name"] = input("Player two, what is your name?\n> 1")

    # Choose pokemon
    player_one["pokemon"] = get_player_pokemon(player_one["name"])
    if game_mode == 1:
        player_two["pokemon"] = random.choice(list_of_pokemon_names)
        print(f"CPU chose: {player_two["pokemon"].capitalize()}")
    elif game_mode == 2:
        player_two["pokemon"] = get_player_pokemon(player_two["name"])

    # Get moves
    for player in players:
        player["moves"] = cs.get_possible_moves(pokemon_name=player["pokemon"], pokemon_level=1)
        player["move_names"] = [move["name"] for move in player["moves"]]

    # play game
    for p in players:
        print(f"It's {p["name"]}'s turn!")
        # User picks move
        choose_random = (p["name"] == "CPU" and game_mode == 1)
        chosen_move = get_choice(f"What will {p["name"]}'s {p["pokemon"].capitalize()} do?", p["move_names"],
                                 "Invalid move. Please choose a valid move from the list.", choose_random)
        print(f"{p["pokemon"].capitalize()} uses {chosen_move}!")


if __name__=="__main__":
    print("Available Pokémon:")
    list_of_pokemon_names = get_pokemon_names()
    for name in list_of_pokemon_names:
        print(name)
    # Choose game mode
    game_mode = int(get_choice("Choose game mode: 1 Player (1) or 2 Player (2):", ['1', '2'],
                           "Invalid input. Please enter 1 or 2."))
    play_game(game_mode)