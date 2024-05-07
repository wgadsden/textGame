import re, operator, random, time
""" Scripts for all party, character, and enemy based functions """

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
        temp = "\nActions: "
        for act in self.actionIDs:
            temp += f"{act} - "
        print(f"Name: {self.name} - Level: {self.level}\nHealth: {self.health} - Attack: {self.level} - Speed: {self.speed}{temp.rstrip("- ")}")
        
    def gain_experience(self, exp):
        # Increases experience by a given amount and automatically increases level
        self.experience += exp
        tmpLvl = self.level # Stores the level for printing the statement at the end
        while True:
            n = self.level+1
            expNeed = round((n*(n^2+75*n-150))/30+2.5-(1/30))
            if exp >= expNeed:
                self.level += 1
                self.health += 5
                self.attack += 2
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
        string = ["Characters:\n"]
        for i in range(character.defined_characters.len()):
            match i % 4:
                case 0:
                    string += f"{i+1}. {character.defined_characters[i].name},"

                case 3:
                    string += f" {i+1}. {character.defined_characters[i].name}\n"

                case None:
                    string += f" {i+1}. {character.defined_characters[i].name},"
        
        for line in string.split("\n"):
            print(line.rstrip(","))
            time.sleep(0.2)
            

characters = { #chicchikin is id no. 0, febbyfaber is id no. 1, etc.
"name": ["chicchikin", "febbyfaber", "bonybuni", "foxifox"], 
"attack": [50, 65, 60, 50],
"speed": [2, 3, 3, 4], 
"health": [70, 75, 80, 90], 
"actionIDs": [["Bite", "Cupcake", "Sing"], ["Bite", "Command", "Pizza wheel"], ["Bite", "Disturbing tone", "Jam out"], ["Bleeding slash", "Cripple", "Gun"]]
}

class enemy:
    all_enemies = {}
    
    def __init__(self, id):
        self.id = id
        for attr in ["name", "attack", "health", "speed", "actionIDs", "tier"]:
            setattr(self, attr, characters[attr][id])
        enemy.all_enemies.add(self)
            
    def find_of_tier(tier):
        result = []
        for ent in enemy.all_enemies:
            if tier in ent.tier:
                result.append(ent)
        return result
    
    def get_enemies(type, tier, num):
        
        options = enemy.find_of_tier(tier)
        result = []
        
        if type == "boss":
            
            for ent in options:
                if "norm" in ent.tier or "mini" in ent.tier:
                    options.pop(options.index(ent))
                  
            for ent in options:
                if "boss" in ent.tier:
                    result.append(ent)
                    options.pop(options.index(ent))
                    
                elif "minion" in ent.tier:
                    if ent not in result:
                        result.append(ent)
                    else:
                        for i in range(2-(options.len()-1)):
                            result.append(ent)

        elif type == "mini":
            
            minis = []
            for ent in options:
                if "boss" in ent.tier or "minion" in ent.tier:
                    options.pop(options.index(ent))
                elif "mini" in ent.tier:
                    minis.append(ent)
                    options.pop(options.index(ent))
            result.append(random.randint(0,len(minis)))
            for i in range(num-1):
                result.append(options[random.randint(0, len(options))])

        elif type == "fight":
            for ent in options:
                if "boss" in ent.tier or "minion" in ent.tier or "mini" in ent.tier:
                    options.pop(options.index(ent))
                    
            for i in range(num):
                result.append(options[random.randint(0, len(options))])
        
        if len(result) > 4:
            for i in range(4, len(result)):
                result.pop(4)
        
        return result

    def append_tier(tier):
        for a in range(enemies["name"].len()):
            if tier in enemies["tier"][a]:
                enemy(a)
    
# Tiers range from C to S, higher tiers are stronger
# Tutorial tier are beginner creatures only found in the tutorial section
enemies = {
"name": ["Sqrl OG", "OG Crab", "Biggie"],
"attack": [30, 50, 60],
"speed": [3, 4, 4],
"health": [100, 160, 400],
"actionIDs": [["Gun", "Acorn"], ["Gun", "Cannibalism"], ["Burger bite", "Gun", "Rap bomb"]],
"tier": [["tutorial","norm"], ["tutorial","norm"], ["tutorial","boss"]]
}