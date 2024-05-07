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
            case "mini":
                combat("mini", maps[playerMap][playerPos[0]][playerPos[1]])
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
            playerPos = m.findStart(playerMap, "S")
        case "win":
            match type:
                case "boss":
                    print(f"You beat the boss! Each character gained {mapInfo[playerMap]["experience"]*2} experience")
                    for ent in partyList:
                        ent.gain_experience(mapInfo[playerMap]["experience"]*2)
                case "mini":
                    print(f"You beat the miniboss. Each character gained {math.round(mapInfo[playerMap]["experience"]*1.5)} experience")
                    for ent in partyList:
                        ent.gain_experience(math.round(mapInfo[playerMap]["experience"]*1.5))
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
            global playerPos;playerPos = m.findPos(playerMap, "L")
            if mapInfo[playerMap]["found"] == False:
                getText(0)
                mapInfo[playerMap]["found"] = True
            else:
                print(f"Moved to zone {playerMap+1}")
        case "back": # Moving to the previous map
            playerMap -= 1
            global playerPos;playerPos = m.findPos(playerMap, "N")
            print(f"Moved to zone {playerMap+1}")

def getText(id=None): # 0 prints enter message, -1 prints leaving message (only new zones)
    if id == 0 or id == -1:
        for line in text[playerMap][id].split("\n"):
            time.sleep(0.2)
            print(line)
            time.sleep(0.55)
        time.sleep(1.5)
    else:
        for line in text[playerMap][random.randint(1,text[playerMap].len()-1)]:
            time.sleep(0.2)
            print(line)
            time.sleep(0.1)
        time.sleep(0.25)
            
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
[ # Map 0 "Tutorial Island"
[["V>"],["<V>F",False, 4],["<>T",False],["<V"]],
[["^VS",True],["^>"],["<V"],["^V>B",False],["<N",True]],
[["^>"],["<>"], ["<^>F",False, 2],["<^"]]
],
[ # Map 1 "The Night's Eye"
[["VL",True],["V>F",False,3],["<V"],["V>M",False,3],["<>"],["<VT",False]],
[["^V>S",True],["<^"],["^>T"],["V^<>"],["<VT",False],["^V>B",False],["<N",True]],
[["^>"],["<>F",False,2],["<>"],["^<>F",False,4],["<^>"],["<^F",False,2]]
],
[ # Map 2 "School with an airship crashed into it"
[["V>S",True],["<V>F",False,3],["<>F",False,4],["<>T",False],["<>M",False,4],["<V"]],
[["V^"],["V^"],["V>"],["<V>"],["<VF",False,2],["^V>B",False],["<N",True]],
[["V>L",True],["^>F",False,4],["<^T",False],["^T",False],["^>M",False,4],["<^"]]
],
[ # Map 3 "Fumo Land"
[[">M",False,3],["<V"],[">T",False],["<>M",False,2],["<VF",False,4],["V>"],["<N",True]],
[[">T",False],["<^>F",False,3],["<V"],["V>F",False,4],["<V^"],["^>"],["<VB",False]],
[[">L",True],["<>"],["<^>S",True],["<^"],["^>"],["<>T",False],["<^"]]
],
[ # Map 4 "Comically Evil Castle"
[["VL",True],["V>F",False,4],["<V>"],["<>F",False,3],["<T",False],["V>T",False],["<>"],["<V"]],
[["V^S",True],["V^>"],["<^>M",False,2],["<V>F",False,3],["<V>F",False,2],["<^"],["V>T",False],["<^F",False,4]],
[["^>F",False,2],["<^"],[">T",False],["<^"],["^>"],["<M",False,3],["^>B",False],["<N",True]]
],
[ # Map 5 "The Final Boss's Lair"
[["L>", True],["<>S", True],["<>"],["<>"],["<>"],["<>B", False],["<N", True]],
],
[ # Map 6 "The Boss Trials"
[["L>", True],["<>S", True],["<>B", False],["<>B", False],["<>B", False],["<>B", False],["<B", False]],
],
]
mapInfo = [
# All experience numbers should be subject to change based on playtesting (there will be no playtesting)
{"name": "Tutorial Island", "tier": "tutorial", "treasure": ["character:4"], "experience": 5, "found": True},

{"name": "The Night's Eye", "tier": "c", "treasure": ["character:5","experience:15","experience:15"], "experience": 7, "found": False},

{"name": "School with an airship crashed into it", "tier": "b", "treasure": ["character:6","character:7","experience:20"], "experience": 10, "found": False},

{"name": "Fumo Land", "tier": "a", "treasure": ["character:8","character:9","experience:25"], "experience": 13, "found": False},

{"name": "Comically Evil Castle", "tier": "s", "treasure": ["character:10","character:11","character:12","experience:30"], "experience": 15, "found": False},

{"name": "The Final Boss's Lair", "tier": "lord", "treasure": [], "experience": 45, "found": False},

{"name": "The Boss Trials", "tier": "absurd", "treasure": [], "experience": 60, "found": False}
]
playerMap = 0
playerPos = [2, 1]

# Text
# Honestly whatever the fuck goes here I don't care anymore
text = [
["You awaken on a pristine beach, the gentle waves lapping at your toes.\nLast thing you remember going to bed a bit tipsy, but not this tipsy.\nIt almost feels like you are in another world\nLush palm trees sway in the warm breeze.\nA faint trail leads inland, with a sign pointing... somewhere?",
'"You feel a strange sense of deja vu..."\n(reference for experienced players)',
'"This island seems suspiciously perfect..."',
'"Maybe a coconut will help you solve puzzles..."\n(unhelpful tip)',
'"A hermit crab scuttles by, leaving a trail of envy in its wake.\nYou wish you were that carefree."',
"Feeling confident in your newfound skills, you set sail from the island on a makeshift raft, ready to face new adventures!\nYou're not fully sure what your goals are or what you will do though.\n# Yeah, I'm going to need that intermission text Joey, just put it here"],
["A colossal airship, the Night's Eye, casts a long shadow as you climb aboard.\nGleaming brass pipes snake across the deck, powered by unknown forces.\nSmoke billows from a central smokestack.\nYou have a bad feeling in your gut about this ship.",
'"Keep an eye out for loose bolts and rogue pigeons."\n(unhelpful tip)',
'"You feel many judgemental stares, and decide to hurry along."',
'"Robotic voices drone the same few lines inbetween sprays of bullets."',
"As you approach the front of the ship, you feel its nose dive downwards.\nIt's heading straight for a building on the ground in a fairly populated area.\nThankfully, though, you manage to find a parachute and save yourself in time."],
["The wreckage of the Night's Eye lies smoldering in the center of a bustling schoolyard.\nStudents in mismatched uniforms scurry around, salvaging parts and dodging debris.\nYou can tell you have just landed in a hostile, viscous place.",
'You find a crumpled note that reads, "Detention for anyone caught playing with the time travel prototype."',
'That crumpled note about the time travel prototype?\nMaybe you should look into it some more.\n(unhelpful tip)',
'You see a janitor sweeping up some dust and rubble, clearly in vain.\nHe tries his best.',
'You bid farewell to that hellhole of a school, looking for another place to go.\nThankfully, hijacking a random 1989 Suzuki Cappucino in this parking lot was easy enough for you.\nYou drive off searching for answers to your situation.'
],
["A strange change occurs in the landscape before you can even realize it.\nAlmost as if you entered into a candyland.\nAdorable, round creatures with massive eyes frolic around.\n'Welcome to Fumo Land!' a big sign reads.",
"You see a rainbow, despite the fact that no rain has poured down since you got here.",
"A Fumo waddles up to you, offering a tiny, knitted scarf.",
"The Fumos love a good game of fetch!\nJust throw something small and adorable, like a rare artifact or a small child.\n(unhelpful tip)"
"You think you just saw a fumo mafia deal go down.\nFor your safety, you choose to avoid this area for a bit."
"Fun fact!\nFumos are notoriously bad at remembering names.\nSo, feel free to give yourself the most ridiculously awesome nickname you can think of.\nThey'll love it!"
],
["The 'peace' of Fumo Land is soon broken by a dubious looking castle.\nWell, kind of, it seems to be evil to a ridiculous extent.\nBut you feel the heat of the red moat and hear a deep, maniacal laughter echo out.\nYou feel as though you may get some answers here (for some reason).",
"You hear an overtly evil chord erupt from an organ somewhere in the building.\nYou wonder who is even playing it.",
"Skeletons line the wall, giving you a grim feeling they may come alive, but it is probably fine",
"A monotonous droning in the background lulls you into a hypnotic state.",
"Feeling hungry?\nTry the dungeon's well-stocked vending machine.\n(unhelpful tip)",
"Having traveled through the halls of the evil castle, you happen upon a regal stairway.\nAssuming it may lead to the final boss, you take your first step up the stairs.\nAnd then some more...\nAnd then even more...\nIt has alot of stairs."]
["Having finished climbing up the stairs, you reach a long hallway.\nA red carpet, seemingly laid out for you, lies before you.\nYou begin to walk forward.\n\n'You have finally arrived, I have been waiting for you.' A voice booms.",
"You sense an evil presence crawling on your back, staring into you.\nOr maybe that's just your hunger.",
"The demon lord gets up off of his knee, looking towards you.\n'I haven't been able to fight like that in a long time!'\n'I had a feeling you would be able to satisfy my craving for a good battle.'\n'Sorry about just taking you from your home and putting you into this world, I'll return you now.'\n'What is this world?'\n'Well, that's not super important right now, but maybe I'll bring you back if you really want to know.'\nThat is the last thing you remember before wake up back in your bed to your alarm.\nWas it a dream? You can't tell anymore.\n..."
],
["Welcome to the post-game.\nFeel free to return to previous maps and finish exploring or complete the boss trials."]
]

if __name__ == "__main__":
    main()