import requests
import json
import random
import pokemon as pk

# only global variable, which is here because of laziness ==============================================================
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


def display_pokemon_names()->None:
    # Get the list of Pokémon from the API
    url = 'https://pokeapi.co/api/v2/pokemon/'
    response = requests.get(url)
    pokemon_list = json.loads(response.text)['results']
    # Create a list of Pokémon names for easy validation
    pokemon_names = [pokemon['name'] for pokemon in pokemon_list]
    print("Available Pokémon:")
    line_size_count = 0
    for name in pokemon_names:
        print(name, end=", ")
        line_size_count += 1
        if line_size_count >= 8:
            print()
            line_size_count = 0
    print("\n")


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
        "pokemon" : None
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

    # get pokemon stats
    for player in players:
        player["pokemon"] = pk.Pokemon(player["pokemon"])

    # play game
    player_id:int = 0
    while True:
        p = players[player_id]
        p_other = players[(player_id + 1) % 2]
        player_mon: pk.Pokemon = p["pokemon"]
        other_mon: pk.Pokemon = p_other["pokemon"]

        print(f"It's {p["name"]}'s turn!")
        # User picks move
        choose_random = (p["name"] == "CPU" and game_mode == 1)
        chosen_move = get_choice(f"What will {p["name"]}'s {player_mon.name.capitalize()} do?",
                                 [x.name for x in player_mon.move_set],
                                 "Invalid move. Please choose a valid move from the list.", choose_random)
        print(f"{player_mon.name.capitalize()} uses {chosen_move}!")

        # resolve attack
        move:pk.Move = player_mon.get_move(chosen_move)
        # Let's use accuracy (even if incorrectly)
        hits:bool = move.accuracy >= random.random()
        if hits:
            print(f"{move.name} hits {p_other["name"]}'s {other_mon.name} for {move.power} damage.")
            other_mon.hp -= move.power
        else:
            print(f"{player_mon.name} missed!")
        if other_mon.hp <= 0:
            print(f"{p_other["name"]}'s {other_mon.name} is KO'd!")
            print(f"{p["name"]} has won!")
            break
        else:
            player_id = (player_id + 1) % 2


if __name__=="__main__":
    print("Welcome to Gotta_GET_Them_All, the (unofficial) CLI pokemon game.")
    display_pokemon_names()
    # Choose game mode
    game_mode = int(get_choice("Choose game mode: 1 Player (1) or 2 Player (2):", ['1', '2'],
                           "Invalid input. Please enter 1 or 2."))
    play_game(game_mode)