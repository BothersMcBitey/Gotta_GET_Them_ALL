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

print(f"CPU chose: {cpu_choice}")