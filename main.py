import combat as c, map as m, party as p
import math, time, re, operator, random

# Input that removes all outside 
# re.sub('\\W+','', input("> "))

def main():
    for i in range(4):
        charFound(i)
        allChars[i].join_party(partyList, i)
    
    getText(0)
    
    while True:
        match mapNav():
            case "fight":
                combat("fight", maps[playerMap][playerPos[0]][playerPos[1]])
            case "boss":
                combat("boss")
            case "treasure":
                a = random.randint(0, len(mapInfo[playerMap]["treasure"].len()))
                b = mapInfo[playerMap]["treasure"][a].split(":")
                if "character" == b[0]:
                    charFound(b[1])
                    mapInfo[playerMap]["treasure"].pop(a)
                elif "experience" == b[0]:
                    print("You found an experience chest (however that works)!")
                    for ent in partyList:
                        ent.gain_experience(b[1])
            case "next": # Moving to the next map
                enterMap("next")
            case "back": # Moving to the previous map
                enterMap("back")
            case "char": # Entering character menu screen (until exited)
                charMenu()
            case None: # 25% chance for "banter"
                if random.randint(0,3) == 1:
                    getText()

def charFound(id):
    id = p.character(id)
    allChars.append(id)
    allChars.sort(key=operator.attrgetter('id'))
    print(f"{id.name} was found! Added to collected characters.")

def charMenu():
    while True:
        print("Welcome to the character menu, what would you like to do?\n1. See all of your characters\n2. See your party\n3. Change a character in your party\n4. See a character's stats\n5. Exit")
        match input("> "):
            case "1":
                p.character.printChars()
            case "2":
                for ent in partyList:
                    ent.print_stats()
            case "3":
                for i in range(4):
                    print(f"{i+1}. {partyList[i].name}")
                try:
                    a = int(input("Input the number of the character to replace\n> "))-1
                    b = int(input("Input the number of the character to place in that spot\n> "))-1
                    if len(allChars) > b and a in range(4):
                        if allChars[b] in partyList:
                            print("That character is already in the party")
                        else:
                            allChars[b].join_party(partyList, a)
                    else:
                        print("Invalid input(s)")
                except ValueError:
                    print("You didn't input a number")
            case "4":
                try:
                    a = int(input("Input the number of the character whose stats you want to see"))-1
                    if len(allChars) > b:
                        allChars[b].print_stats()
                    else:
                        print("Invalid input")
                except ValueError:
                    print("You didn't input a number")
            case "5":
                print("Returning to map")
                break
            case None:
                print("Invalid option")

def combat(type, num=2):
    r = c.combat(partyList,p.enemy.get_enemies(type, mapInfo[playerMap]["tier"], num))
    match r:
        case "lose":
            print("You lost the battle and were sent back to the start of the map")
            global playerPos 
            playerPos = m.findStart(playerMap)
        case "win":
            match type:
                case "boss":
                    print(f"You beat the boss! Each character gained {mapInfo[playerMap]["experience"]*2} experience")
                    for ent in partyList:
                        ent.gain_experience(mapInfo[playerMap]["experience"]*2)
                case "fight":
                    print(f"You won, and each character gained {mapInfo[playerMap]["experience"]} experience")
                    for ent in partyList:
                        ent.gain_experience(mapInfo[playerMap]["experience"])

def mapNav():
    m.printMap(playerMap, playerPos)
    time.sleep(0.2)
    r = m.movePos(playerMap, playerPos)
    if r == "exit":
        return "char"
    else:
        playerPos = r
        return m.checkPos(playerMap, playerPos)

def enterMap(dir):
    match dir:
        case "next": # Moving to the next map
            getText(-1)
            time.sleep(1)
            playerMap += 1
            if mapInfo[playerMap]["found"] == False:
                getText(0)
                mapInfo[playerMap]["found"] = True
            else:
                print(f"Moved to zone {playerMap+1}")
        case "back": # Moving to the previous map
            playerMap -= 1
            print(f"Moved to zone {playerMap+1}")

def getText(id=None): # 0 prints enter message, -1 prints leaving message (only new zones)
    if id == 0 or id == -1:
        for line in text[playerMap][id].split("\n"):
            print(line)
            time.sleep(0.2)
    else:
        for line in text[playerMap][random.randint(1,text[playerMap].len()-1)]:
            print(line)
            time.sleep(0.1)
            
# Player's party
partyList = ["", "", "", ""]
allChars = []

# Map stuff
# Arrows (^V<>) are "connections" between nodes
# (First) letter is the type of location
# S = start, F = fight, T = treasure, B = boss, N = next, L = back
# (Second) letter is the connections to other locations (Only locations)
# (Third) letter is if the location has been discovered or not (Only locations)
maps = [
[
[["V>"],["<V>F",False, 4],["<>T",False],["<V"]],
[["^VS",True],["^>"],["<V"],["^V>B",False],["<N",True]],
[["^>"],["<>"], ["<^>F",False, 2],["<^"]]
],
[]
]
mapInfo = [
# All experience numbers should be subject to change based on playtesting (there will be no playtesting)
{"name": "Tutorial Island", "tier": "tutorial", "treasure": ["character:4"], "experience": 5, "found": True},

{"name": "The Night's Eye", "tier": "c", "treasure": ["character:5","experience:15"], "experience": 7, "found": False},

{"name": "School with an airship crashed into it", "tier": "b", "treasure": ["character:6","character:7","experience:20"], "experience": 10, "found": False},

{"name": "Fumo land", "tier": "a", "treasure": ["character:8","character:9","experience:25"], "experience": 13, "found": False},

{"name": "Comically evil castle", "tier": "s", "treasure": ["character:10","character:11","character:12","experience:30"], "experience": 15, "found": False},
]
playerMap = 0
playerPos = [2, 1]

# Text
# Honestly whatever the fuck goes here I don't care anymore
text = [
[]
]

if __name__ == "__main__":
    main()