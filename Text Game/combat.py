import math, time, random
import party

def combat(plr: list, enm: list):
    timeCounter = 1
    set = []
    actions = ["", "", "", "", "", "", "", ""]

    for char in plr:
        set.append({"name":char.name,"attack":char.attack,"speed":char.speed,"counter":char.speed,"maxHP":char.health,"HP":char.health,"actions":char.actionIDs,"type":"plr","state":["alive"]})

    for enmy in enm:
        set.append({"name":enmy.name,"attack":enmy.attack,"speed":enmy.speed,"counter":enmy.speed,"maxHP":enmy.health,"HP":enmy.health,"actions":enmy.actionIDs,"type":"enmy","state":["alive"]})

    for ent in set:
        for item in ent["actions"]:
            action.all_actions.add(item)

    for i in range(len(set), 8):
        set.append({"name":"","speed":99999,"counter":99999,"maxHP":100,"HP":0,"type":"","state":[""]})
        
    # V Will be removed V
    for i in set:
        print(f"{i}. {set["name"]}{" " * (12-len(set["name"]))} SPD: {set["speed"]}")
    # ^                 ^

    while True:

        if set[i]["health"] in range(4,8) <= 0:
            pass # Should trigger win sequence for player
            break
        elif set[i]["health"] in range(0,4) <= 0:
            pass # Should trigger loss sequence for player
            break

        for ent in set:
            ent["counter"] -= timeCounter
            if ent["speed"] < 0 and "alive" in ent["state"]:
                ent["counter"] = ent["speed"]
                ent["state"].append("ready")
        
        printMenus(set)

        for i in range(8):
            if "alive" and "ready" in set[i]["state"]:
                if set[i]["type"] == "plr":
                    actions[i] = getActions(set[i])
                    printMenus(set)
                else:
                    actions[i] = set[i]["actions"][random.randint(0, len(set[i]["actions"]))]

    # Removing all action objects at the end of battle
    for item in action.all_actions:
        action.all_actions.discard(item)
        del item
     
            
def printMenus(set):
    for i in range(0,4):
        plr = ""
        enm = ""

        if "ready" in set[i+4]["state"]:
            enm = "[READY] "
        else:
            enm = "        "

        if "ready" in set[i]["state"]:
            plr = " [READY]"
        else:
            plr = "        "

        print(f"{enm}{set[i+4]["name"]}{" "*(12-len(set[i+4]["name"]))} [{"="*math.round(10-((set[i+4]["maxHP"]-set[i+4]["HP"])/set[i+4]["maxHP"]*10))}{" "*math.round(10-(-set[i+4]["HP"]/set[i+4]["maxHP"]*10))}]     [{"="*math.round(10-((set[i]["maxHP"]-set[i+4]["HP"])/set[i]["maxHP"]*10))}{" "*math.round(10-(-set[i+4]["HP"]/set[i+4]["maxHP"]*10))}] {set[i]["name"]}{" "*(12-len(set[i]["name"]))}{plr}")

def getActions(char):
    i = 1
    inp = 5 # Define as some arbitrary number greater than the amount of actions any character has
    for act in char["actions"]:
        print(f"{i}. {act}")
        i += 1
    while inp > i:
        inp = int(char["actions"][input("> ")])
    return char["actions"][inp-1]

def useActions(acts, set):
    # Every move needs to define a target and the damage done to them
    for i in range(4):
        match acts[i]["type"]:
            case "s":
                dmg = acts[i].calculation[0] * set[i]["attack"]
                tar = [set[4], set[5], set[6], set[7]]
                for i in tar:
                    if i["health"] <= 0:
                        del tar[tar.index(i)]
                    elif "taunt" in i["state"]:
                        tar = [i]
                        break
                set[4+random.randint(0, len(tar))]["health"] -= dmg
                print(f"{set[i]["name"]} did {dmg} damage to all enemies with {acts[i]["name"]}")
            case "a":
                dmg = acts[i].calculation[0] * set[i]["attack"]
                for i in range(4,8):
                    set[i]["health"] -= dmg
                print(f"{set[i]["name"]} did {dmg} damage to all enemies with {acts[i]["name"]}")
            case "h":
                pass
            case "b":
                pass
            case "d":
                pass
            case "sp":
                pass
            case None:
                pass
        match acts[i+4]["type"]:
            case "s":
                pass
            case "a":
                pass
            case "h":
                pass
            case "b":
                pass
            case "d":
                pass
            case "sp":
                pass
            case None:
                pass



class action:
    all_actions = {}

    def __init__(self, id):
        self.id = id
        for attr in ["name", "type", "calculation"]:
            setattr(self, attr, actionDict[attr][id])

# Action types are as follows:
# Single, Area, Healing, Buffing, Debuffing, Special
actionDict = {
"names": [],
"type": [],
"calculation": []
}