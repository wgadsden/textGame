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
        print(f"Name: {self.name} - Level: {self.level}\nHealth: {self.health} - Attack: {self.level} - Speed: {self.speed}{temp.rstrip('- ')}")
        
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
        for i in range(len(character.defined_characters)):
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
"name": ["chicchikin", "febbyfaber", "bonybuni", "foxifox",
"1989 Suzuki Cappucino", "Spyro", "Mascot character", "School janitor",
"Fumo Goku","Reimu Hakurei",
"Caseoh","Cool gargoyle","Wrecking ball"], 
"attack": [50, 65, 60, 50,
30, 50, 50, 40,
80, 70,
40, 70, 60],
"speed": [2, 3, 3, 4,
1, 3, 4, 3,
2, 3,
5, 3, 2],
"health": [90, 95, 100, 110,
90, 110, 150, 120,
140, 120,
400, 150, 135], 
"actionIDs": [["Bite", "Cupcake", "Sing"], ["Bite", "Command", "Pizza wheel"], ["Bite", "Disturbing tone", "Jam out"], ["Bleeding slash", "Cripple", "Gun"],
["Crash","Exhaust fumes","Funny look"], ["Ram", "Fire bomb", "Fire breath"], ["Healing grenade", "Inspire", "Cleanse"],["Broom spear", "Sticky solution", "Wash off"],
["Kill yourself NOW", "Spirit bomb", "Instant transmission"],["The f*** off beam", "Life ritual", "Bad Apple!!"],
["Crash", "Burger bite", "Taunt"],["Piercing glare", "War scream", "Psychic headache"],["Debris crash", "Ultra heal", "Regenerative chitter"]]
}

class enemy:
    all_enemies = []
    
    def __init__(self, id):
        self.id = id
        self.tier = None
        for attr in ["name", "attack", "health", "speed", "actionIDs", "tier"]:
            setattr(self, attr, enemies[attr][id])
        enemy.all_enemies.append(self)
            
    def find_of_tier(tier):
        result = []
        for ent in enemy.all_enemies:
            if tier in ent.tier:
                result.append(ent)
        return result
    
    def get_enemies(type, tier, num, id=None):
        
        options = enemy.find_of_tier(tier)
        result = []
        
        if type == "boss":
            
            for ent in options:
                if "boss" not in ent.tier or "minion" not in ent.tier:
                    options.pop(options.index(ent))
                  
            for ent in options:
                if "boss" in ent.tier and id in ent.tier:
                    result.append(ent)
                    options.pop(options.index(ent))
                    
                elif "minion" in ent.tier and id in ent.tier:
                    if ent not in result:
                        result.append(ent)
                    else:
                        for i in range(2-(len(options)-1)):
                            result.append(ent)

        elif type == "mini":
            
            minis = []
            for ent in options:
                if "boss" in ent.tier or "minion" in ent.tier:
                    options.pop(options.index(ent))
                elif "mini" in ent.tier and id in ent.tier:
                    minis.append(ent)
                    options.pop(options.index(ent))
            result.append(random.randint(0,len(minis)-1))
            for i in range(num-1):
                result.append(options[random.randint(0, len(options)-1)])

        elif type == "fight":
            for ent in options:
                if "boss" in ent.tier or "minion" in ent.tier or "mini" in ent.tier:
                    options.pop(options.index(ent))
            
            for i in range(num):
                result.append(options[random.randint(0, len(options)-1)])
        
        if len(result) > 4:
            for i in range(4, len(result)):
                result.pop(4)
        
        return result

    def append_tier(tier):
        for a in range(len(enemies["name"])):
            if tier in enemies["tier"][a]:
                enemy(a)
    
# Tiers range from C to S, higher tiers are stronger
# Tutorial tier are beginner creatures only found in the tutorial section
enemies = {
"name": ["Sqrl OG", "OG Crab", "Biggie", # World 0
"4Chan user", "Suicide bomber", "Robot", "Steampunk mech", "Tinkerer", "Automatic sentry", # World 1
"1st grade class", "LARGE spider", "Annoyed teacher", "Detention officer", "Little League Coach", "Little League Player", # World 2
"Normal sized fumo", "Shiny fumo", "Cat?", "SCP-Fumo", "Kuma", "World Destroyer Fumo", # World 3
"Evil gargoyle", "Skeleton knight", "Living sarcohagus", "Ghoul", "Jack Skellington", "The Free Bird", "Dominic the Dragon", # World 4
"Evil Edgy Overlord", "Red Crystal", "Blue Crystal", "Green Crystal", # World 5
"Artificer", "Magic machine gun", "Big League Coach", "Big League Player", "The Almighty Fumo", "Ascended Dragon Aesir", "The Demon Lord"], # World 6
"attack": [30, 50, 60,
45, 35, 35, 50, 30, 20, # World 1
60, 40, 50, 50, 50, 35, # World 2
50, 65, 40, 60, 50, 75, # World 3
70, 50, 60, 50, 70, 65, 80, # World 4
90, 30, 30, 30, # World 5
60, 35, 70, 50, 100, 110, 125], # World 6
"speed": [3, 4, 4,
4, 3, 3, 4, 3, 1, # World 1
4, 2, 3, 3, 4, 2, # World 2
3, 5, 2, 4, 2, 4, # World 3
4, 3, 4, 3, 3, 2, 4, # World 4
3, 5, 5, 5, # World 5
3, 1, 3, 2, 3, 3, 2], # World 6
"health": [100, 160, 400,
200, 120, 180, 350, 500, 120, # World 1
250, 175, 200, 500, 800, 250, # World 2
300, 350, 250, 700, 600, 1000, # World 3
500, 400, 600, 350, 1000, 800, 1350, # World 4
1750, 500, 500, 500, # World 5
1700, 350, 1500, 500, 2000, 2200, 2500], # World 6
"actionIDs": [["Gun", "Acorn"], ["Gun", "Cannibalism"], ["Burger bite", "Gun", "Rap bomb"],
["Complain", "Superiority complex", "MLP Jar"], ["Kamikaze", "Gun"], ["Zap taser", "Punch"], ["Missiles", "Grease spray", "Gear up"], ["Gun", "Gear up", "Healing grenade", "Quick repair"], ["Gun"], # World 1
["Draw", "Bite", "Cannibalism"], ["Bite", "Sticky situation", "Venom spray"], ["Ruler slap", "Apple", "Demoralize"], ["Punch", "Block stance","Adrenaline shot"], ["Victory cry", "Gatorade jug", "Blatant harrassment", "Pace set"], ["Bat swing","Clutch up"], # World 2
["Supersonic cry", "Sunny day", "Empathy"], ["Punch", "Tears"], ["Bite", "Agility"], ["Strange occurence", "Headache", "Imminent danger"], ["Unfunny joke", "Healing spell", "Deep cuts"], ["Ultrakill","Sunny day", "War scream", "Imminent danger"], # World 3
["Piercing glare", "War scream", "Psychic headache"], ["Sword slash", "Bone rattle"], ["Soul clutch", "Slow down"], ["Supersonic cry", "Sing", "Tears"], ["Halloween scare", "Supersonic cry", "Deep cuts"], ["Fire breath", "Phoenix feather", "Piercing glare"], ["Scorching ray", "Mega bite","Debris crash", "War scream"], # World 4
["Imminent danger","Ultrakill","Block stance"], ["Red glow"], ["Blue glow"], ["Green glow"], # World 5
["Gun+", "Gear up", "Healing bomb", "Quick repair"], ["Gun+"], ["Victory cry", "Gatorade jug", "Blatant harrasment", "Pace set"], ["Bat swing","Clutch up"], ["Ultrakill","Sunny day", "War scream", "Imminenet danger"], ["Scorching ray", "Mega bite","Debris crash", "War scream"], ["Imminent danger","Ultrakill","Block stance"]], # World 6
"tier": [["tutorial","norm"], ["tutorial","norm"], ["tutorial","boss",1],
["c","norm"], ["c","norm"], ["c","norm"], ["c","mini",1], ["c","boss",2], ["c","minion",2], # World 1
["b","norm"], ["b","norm"], ["b","norm"], ["b","mini",1], ["b","boss",2], ["b","minion",2], # World 2
["a","norm"], ["a","norm"], ["a","norm"], ["a","mini",1], ["a","mini",2], ["a","boss",3], # World 3
["s","norm"], ["s","norm"], ["s","norm"], ["s","norm"], ["s","mini",1], ["s","mini",2], ["s","boss",3], # World 4
["lord","boss",1], ["lord","minion",1], ["lord","minion",1], ["lord","minion",1], # World 5
["absurd","boss",1], ["absurd","minion",1], ["absurd","boss",2], ["absurd","minion",2], ["absurd","boss",3], ["absurd","boss",4], ["absurd","boss",5]] # World 6
}