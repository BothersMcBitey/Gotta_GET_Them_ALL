from random import random

import requests
import json
import random

# Get the list of pokemon from the API
url = 'https://pokeapi.co/api/v2/pokemon/'
response = requests.get(url)
pokemon_list = json.loads(response.text)['results']
for pokemon in pokemon_list:
    print(pokemon['name'])


cpu_choice = random.choice(pokemon_list)['name']

# Loop until user gives a valid input
while True:
    user_choice = input("Would you like a random Pokémon (R) or choose (C)? ").upper()

    if user_choice == 'R':
        user_pokemon = random.choice(pokemon_list)['name']
        print(f"User chose: {user_pokemon}")
        break
    elif user_choice == 'C':
        user_pokemon = input("Enter your Pokémon: ").lower()
        print(f"User chose: {user_pokemon}")
        break
    else:
        print("Invalid input, please write R or C.")

print(f"CPU chose: {cpu_choice}")