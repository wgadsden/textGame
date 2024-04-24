import re, operator

class character:
    defined_characters = []

    def __init__(self, id):
        self.id = id
        for attr in ["name", "attack", "health", "speed", "actionIDs"]:
            setattr(self, attr, characters[attr][id])
        self.experience = 0
        self.level = 1
        character.defined_characters.append(self)
        character.defined_characters.sort(key=operator.attrgetter('id'))
    
    def print_stats(self):
        print(f"Name: {self.name}\nHealth: {self.health}\nAttack: {self.level}\nSpeed: {self.speed}\n{(str(self.action_list())).strip("[]").replace("'", "")}")
        
    def action_list(self):
        # Returns a list of actions based on the character's action IDs for printing
        l = []
        for id in self.actionIDs:
            l.append(actions[id])
        return l
    
    def gain_experience(self, exp):
        # Increases experience by a given amount and automatically increases level
        self.experience += exp
        tmpLvl = self.level # Stores the level for printing the statement at the end
        while True:
            n = self.level+1
            expNeed = round((n*(n^2+75*n-150))/30+2.5-(1/30))
            if exp >= expNeed:
                self.level += 1
            else:
                break
        if self.level > tmpLvl:
            print(f"{self.name} leveled up from {tmpLvl} to {self.level}")

    def join_party(self, listIn, spot=4):
        if spot > 3:
            while spot > 3:
                print("Please input a valid number (1-4)")
                spot = int(input("> ")) - 1
        listIn.pop(spot)
        listIn.insert(spot, self)
        print(f"Added {self.name} to the party")

    def findChar(name: str):
        """
        Returns with the operable value of a class object of the character class
        Intended use is to take input for the function and iterate over the list of obtained characters
        Checks the input against the full name of each object's name, then the first 4 letters of the name
        If it finds a match, it will return the found object
        """
        
        for char in character.defined_characters:
            a = re.sub('\\W+','', char.name)
            for i in range(0,4):
                if name[i] == a[i]:
                    if i == 3:                        
                        name = char

                else:
                    break

        try:
            print(f"Found the character {name.name} in obtained characters")
            return name
        
        except:
            print("Attempted to find a character that doesn't exist or is unobtained")

    def printChars():
        """
        Prints a full list of characters with 4 characters per line.
        """
        string = "Characters:\n"
        i = 0
        for item in character.defined_characters:
            match i:
                case 3:
                    string += f" {item.name}\n"
                    i = 0

                case 0:
                    string += f"{item.name},"
                    i += 1

                case _:
                    string += f" {item.name},"
                    i += 1
        print(string.rstrip(",\n"))

characters = { #chicchikin is id no. 0, febbyfaber is id no. 1, etc.
"name": ["chicchikin", "febbyfaber", "foxifox", "bonybuni"], 
"attack": [60, 80, 60, 70],
"speed": [4, 3, 2, 3], 
"health": [60, 75, 90, 80], 
"actionIDs": [[0, 1, 3], [1, 2, 5], [4, 5, 6], [0, 2, 6]]
}

class enemy:
    def __init__(self, id):
        self.id = id
        for attr in ["name", "attack", "health", "speed", "actionIDs"]:
            setattr(self, attr, characters[attr][id])
