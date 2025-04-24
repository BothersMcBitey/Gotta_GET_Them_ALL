#defines how pokemon work

import api_interactions as api

class Move:
    def __init__(self, name:str="", id:int=-1):
        if name == "" and id == -1:
            raise ValueError("At least one of Name or ID must be given")
        if id == -1:
            self.name = name
            self.data = api._get_data("move", object_name=self.name)
            self.id = self.data["id"]
        else:
            self.id = id
            self.data = api._get_data("move", object_id=self.id)
            self.name = self.data["name"]
        self.accuracy = self.data["accuracy"] if self.data["accuracy"] is not None else 1
        self.power = self.data["power"] if self.data["power"] is not None else 0
        self.type = self.data["type"]
        self.pp = self.data["pp"]

    def __str__(self):
        s = f"id: {self.id}, "
        s += f"name: {self.name}, "
        s += f"power: {self.power}, "
        s += f"accuracy: {self.accuracy}, "
        s += f"type: {self.type}"
        return s

class Pokemon:
    # if no name or ID is given, this will break
    def __init__(self, name:str="", id:int=-1):
        if name == "" and id == -1:
            raise ValueError("At least one of Name or ID must be given")
        if id == -1:
            self.name = name
            self.data = api._get_data("pokemon", object_name=self.name)
            self.id = self.data["id"]
        else:
            self.id = id
            self.data = api._get_data("pokemon", object_id=self.id)
            self.name = self.data["name"]
        self.move_set = self.construct_moveset()
        #TODO: Rewrite this whole section, it sucks
        stats = api.get_pokemon_stats(self.name)
        self.hp:int = [x for x in stats if x["name"]=="hp"][0]["value"]
        self.attack:int = [x for x in stats if x["name"]=="attack"][0]["value"]
        self.defense:int = [x for x in stats if x["name"]=="defense"][0]["value"]
        self.special_attack:int = [x for x in stats if x["name"]=="special-attack"][0]["value"]
        self.special_defense:int = [x for x in stats if x["name"]=="special-defense"][0]["value"]
        self.speed:int  = [x for x in stats if x["name"]=="speed"][0]["value"]

    def construct_moveset(self)->list:
        possible_moves = api.get_possible_moves(self.name)
        move_set = []
        for pm in possible_moves:
            move_set.append(Move(pm["name"]))
        return move_set

    def get_move(self, move_name:str)->Move:
        for move in self.move_set:
            if move.name == move_name: return move
        raise Exception(f"Move {move_name} is not in this pokemon's move set")

    def __str__(self):
        s = f"id: {self.id}, "
        s += f"name: {self.name}, "
        s += f"hp: {self.hp}, "
        s += f"attack: {self.attack}, "
        s += f"move_set: \n\t{[str(x) for x in self.move_set]}"
        return s

#p = Pokemon("charmander")
#print(p)