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
        temp = {}
        for item in ent["actions"]:
            temp.add(item)
        for item in temp:
            for i in actionDict:
                if item in i:
                    action(actionDict["names"].index(i))
                    break

    for i in range(len(set), 8):
        set.append({"name":"","speed":99999,"counter":99999,"maxHP":100,"HP":0,"type":"","state":[""]})
        
    # V Will be removed V
    for i in set:
        print(f"{i}. {set["name"]}{" " * (12-len(set["name"]))} SPD: {set["speed"]}")
    # ^                 ^

    while True:

        if set[i]["HP"] in range(4,8) <= 0:
            pass # Should trigger win sequence for player
            break
        elif set[i]["HP"] in range(0,4) <= 0:
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
    for act in action.all_actions:
        act.del_self()
     
            
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
                for e in tar:
                    if e["HP"] <= 0:
                        del tar[tar.index(e)]
                    elif "taunt" in e["state"]:
                        tar = [e]
                        break
                tar = tar[random.randint(0, len(tar))]
                tar["HP"] -= dmg
                print(f"{set[i]["name"]} did {dmg} damage to {tar["name"]} with {acts[i]["name"]}")
            case "a":
                dmg = acts[i].calculation[0] * set[i]["attack"]
                for e in range(4,8):
                    set[e]["HP"] -= dmg
                print(f"{set[i]["name"]} did {dmg} damage to all enemies with {acts[i]["name"]}")
            case "h":
                heal = acts[i].calculation[0] * set[i]["attack"]
                tar = [set[0], set[1], set[2], set[3]]
                for e in tar:
                    if e["HP"] <= 0 or e["HP"] == e["maxHP"]:
                        del tar[tar.index(e)]
                valTar = []
                for e in range(acts[i].calculation[1]):
                    valid = tar[random.randint(0, len(tar))]
                    if valid not in valTar:
                        valTar.append(valid)
                        del tar[tar.index(valid)]
                for ent in valTar:
                    ent["HP"] -= heal
                print(f"{set[i]["name"]} healed {heal} HP to {len(valTar)} targets with {acts[i]["name"]}")
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
                dmg = acts[i+4].calculation[0] * set[i]["attack"]
                tar = [set[0], set[1], set[2], set[3]]
                for e in tar:
                    if e["HP"] <= 0:
                        del tar[tar.index(e)]
                    elif "taunt" in e["state"]:
                        tar = [e]
                        break
                tar = set[4+random.randint(0, len(tar))]["HP"]
                tar["HP"] -= dmg
                print(f"{set[i+4]["name"]} did {dmg} damage to {tar["name"]} with {acts[i+4]["name"]}")
            case "a":
                dmg = acts[i].calculation[0] * set[i]["attack"]
                for e in range(0,4):
                    set[e]["HP"] -= dmg
                print(f"{set[i]["name"]} did {dmg} damage to all enemies with {acts[i]["name"]}")
            case "h":
                heal = acts[i].calculation[0] * set[i]["attack"]
                tar = [set[4], set[5], set[6], set[7]]
                for e in tar:
                    if e["HP"] <= 0 or e["HP"] == e["maxHP"]:
                        del tar[tar.index(e)]
                valTar = []
                for e in range(acts[i].calculation[1]):
                    valid = tar[random.randint(0, len(tar))]
                    if valid not in valTar:
                        valTar.append(valid)
                        del tar[tar.index(valid)]
                for ent in valTar:
                    ent["HP"] -= heal
                print(f"{set[i]["name"]} healed {heal} HP to {len(valTar)} targets with {acts[i]["name"]}")
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
        action.all_actions.add(self)
    
    def del_self():
        action.all_actions.delete(self)
        del self

# Action types are as follows:
# Single | Area   | Healing       | Buffing       | Debuffing                          | Special
# Calculations per type are as follows
# [%DMG] | [%DMG] | [%DMG,NO.TAR] | [BFID,LENGTH] | [DBFID,LENGTH,%DMG(if applicable)] | [LENGTH, %DMG]
actionDict = {
"names": [],
"type": [],
"calculation": []
}