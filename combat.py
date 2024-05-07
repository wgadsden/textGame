import math, time, random
""" Scripts for all combat-based functions and actions """

def combat(plr: list, enm: list):
    timeCounter = 1
    set = []
    actions = ["", "", "", "", "", "", "", ""]

    for char in plr: # Adds all player characters into their respective positions
        set.append({"name":char.name,"attack":char.attack,"speed":char.speed,"counter":char.speed,"maxHP":char.health,"HP":char.health,"actions":char.actionIDs,"type":"plr","state":["alive"]})

    for enmy in enm: # Adds all enemies into their respective positions
        set.append({"name":enmy.name,"attack":enmy.attack,"speed":enmy.speed,"counter":enmy.speed,"maxHP":enmy.health,"HP":enmy.health,"actions":enmy.actionIDs,"type":"enmy","state":["alive"]})

    for ent in set: # Adding all actions as classes
        temp = {}
        for item in ent["actions"]:
            temp.add(item)
        for item in temp:
            action(item)
            

    for i in range(len(set), 8): # Fills remaining slots with "empty" objects
        set.append({"name":"","speed":99999,"counter":99999,"maxHP":100,"HP":0,"type":"","state":[""]})
    
    result = ""

    while True:

        actions = ["", "", "", "", "", "", "", ""]

        if set[i]["HP"] in range(4,8) <= 0:
            result = "win"
            break
        elif set[i]["HP"] in range(0,4) <= 0:
            result = "lose"
            break

        for i in range(8):
            set[i]["counter"] -= timeCounter
            if ent["speed"] < 0 and "alive" in ent["state"]:
                set[i]["counter"] = set[i]["speed"]
                set[i]["state"].append("ready")
        
        set = statusEffects(set)
        
        printMenus(set)

        for i in range(8):
            if "alive" and "ready" in set[i]["state"]:
                if set[i]["type"] == "plr":
                    actions[i] = getActions(set[i])
                    printMenus(set)
                else:
                    actions[i] = set[i]["actions"][random.randint(0, len(set[i]["actions"]))]
        
        for i in range(8):
            for a in action.all_actions:
                if actions[i] == a.name:
                    actions[i] = a
                    break

        set = useActions(actions, set)

        time.sleep(1)

    for act in action.all_actions: # Removing all action objects at the end of battle
        act.del_self()

    if result == "win":
        return "win"
    elif result == "lose":
        return "lose"  
            
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

        print(f"{enm}{set[i+4]['name']}{' '*(21-len(set[i+4]['name']))} [{'='*math.round(10-((set[i+4]['maxHP']-set[i+4]['HP'])/set[i+4]['maxHP']*10))}{' '*math.round(10-(-set[i+4]['HP']/set[i+4]['maxHP']*10))}]     [{'='*math.round(10-((set[i]['maxHP']-set[i+4]['HP'])/set[i]['maxHP']*10))}{' '*math.round(10-(-set[i+4]['HP']/set[i+4]['maxHP']*10))}] {set[i]['name']}{' '*(21-len(set[i]['name']))}{plr}")

        time.sleep(0.2)

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
                dmg = math.round(acts[i].calculation[0] * set[i]["attack"] * (random.randint(90,110) / 100))
                tar = [set[4], set[5], set[6], set[7]]
                for e in tar:
                    if e["HP"] <= 0:
                        del tar[tar.index(e)]
                    elif "taunt" in e["state"]:
                        tar = [e]
                        break
                tar = tar[random.randint(0, len(tar))]
                temp = False
                a = 0
                for b in tar["state"]:
                        if "shield" in b:
                            temp = True
                            break
                        else:
                            a += 1
                n = set.index(tar)
                if temp:
                    set[n]["state"].pop(a)
                    print(f"{set[n]['name']} blocked the hit from {set[i]['name']}")
                else:    
                    set[n]["HP"] -= dmg
                    print(f"{set[i]['name']} did {dmg} damage to {set[n]['name']} with {acts[i]['name']}")
            case "a":
                dmg = math.round(acts[i].calculation[0] * set[i]["attack"] * (random.randint(90,110) / 100))
                for e in range(4,8):
                    temp = False
                    a = 0
                    for b in set[e]["state"]:
                        if "shield" in b:
                            temp = True
                            break
                        else:
                            a += 1
                    if temp:
                        set[e]["state"].pop(a)
                        print(f"{set[e]['name']} blocked the hit from {set[i]['name']}")
                    else:
                        set[e]["HP"] -= dmg
                        print(f"{set[i]['name']} did {dmg} damage to {set[e]['name']} with {acts[i]['name']}")
            case "h":
                heal = math.round(acts[i].calculation[0] * set[i]["maxHP"]) * (random.randint(95,105) / 100)
                if acts[i].calculation[1] != "self":
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
                        n = set.index(ent)
                        if set[n]["HP"] + heal > set[n]["maxHP"]:
                            set[n]["HP"] = set[n]["maxHP"]
                        else:
                            set[n]["HP"] += heal
                    print(f"{set[i]['name']} healed {heal} HP to {len(valTar)} targets with {acts[i]['name']}")
                else:
                    set[i+4]["HP"] += heal
                    print(f"{set[i+4]['name']} healed {heal} HP to themself targets with {acts[i+4]['name']}")
            case "b":
                match acts[i].calculation[0]:
                    case 0:
                        for e in range(0,4):
                            temp = False
                            for a in set[e]["state"]:
                                if "atkUP" in a:
                                    set[e]["state"][set[e]["state"].index(a)][1] = acts[i].calculation[1]
                                    temp = True
                                    print(f"{set[e]["name"]}'s attack buff was extended")
                                    break
                            if temp == False and "alive" in set[e]["state"]:
                                set[e]["state"].append(["atkUP", acts[i].calculation[1]])
                                set[e]["attack"] = set[e]["attack"] * 1.5
                                print(f"{set[e]['name']}'s attack was buffed by {set[i]['name']}")
                    case 1:
                        for e in range(0,4):
                            temp = False
                            for a in set[e]["state"]:
                                if "spdUP" in a:
                                    set[e]["state"][set[e]["state"].index(a)][1] = acts[i].calculation[1]
                                    temp = True
                                    print(f"{set[e]["name"]}'s speed buff was extended")
                                    break
                            if temp == False and "alive" in set[e]["state"]:
                                set[e]["state"].append(["spdUP", acts[i].calculation[1]])
                                set[e]["speed"] -= 1
                                print(f"{set[e]['name']}'s speed was buffed by {set[i]['name']}")
                    case 2:
                        for e in range(0,4):
                            temp = False
                            for a in set[e]["state"]:
                                if "regen" in a:
                                    set[e]["state"][set[e]["state"].index(a)][1] = acts[i].calculation[1]
                                    temp = True
                                    print(f"{set[e]["name"]}'s regeneration buff was extended")
                                    break
                            if temp == False and "alive" in set[e]["state"]:
                                set[e]["state"].append(["regen", acts[i].calculation[1]])
                                set[e]["speed"] -= 1
                                print(f"{set[e]['name']}'s regeneration was buffed by {set[i]['name']}")
                    case 3:
                        for e in range(0,4):
                            temp = False
                            for a in set[e]["state"]:
                                if "shield" in a:
                                    set[e]["state"][set[e]["state"].index(a)][1] = acts[i].calculation[1]
                                    temp = True
                                    print(f"{set[e]["name"]}'s shield was extended")
                                    break
                            if temp == False and "alive" in set[e]["state"]:
                                set[e]["state"].append(["shield", acts[i].calculation[1]])
                                print(f"{set[e]['name']}'s was shielded by {set[i]['name']}")
                    case 4:
                        temp = True
                        for e in len(set[i+4]["state"].len()):
                            if "taunt" in e:
                                temp = False
                        print(f"{set[i+4]["name"]} taunted the enemy for a turn")
                        if temp:
                            set[i+4]["state"].append("taunt")
            case "d":
                match acts[i].calculation[0]:
                    case 0:
                        for e in range(4,8):
                            temp = False
                            for a in set[e]["state"]:
                                if "atkDW" in a:
                                    set[e]["state"][set[e]["state"].index(a)][1] = acts[i+4].calculation[1]
                                    temp = True
                                    print(f"{set[e]["name"]}'s attack debuff was extended")
                                    break
                            if temp == False and "alive" in set[e]["state"]:
                                set[e]["state"].append(["atkDW", acts[i+4].calculation[1]])
                                set[e]["attack"] = set[e]["attack"] * (2/3)
                                print(f"{set[e]['name']}'s attack was debuffed by {set[i+4]['name']}")
                    case 1:
                        for e in range(4,8):
                            temp = False
                            for a in set[e]["state"]:
                                if "spdDW" in a:
                                    set[e]["state"][set[e]["state"].index(a)][1] = acts[i+4].calculation[1]
                                    temp = True
                                    print(f"{set[e]["name"]}'s speed debuff was extended")
                                    break
                            if temp == False and "alive" in set[e]["state"]:
                                set[e]["state"].append(["spdDW", acts[i+4].calculation[1]])
                                set[e]["speed"] += 1
                                print(f"{set[e]['name']}'s speed was debuffed by {set[i+4]['name']}")
                    case 2:
                        for e in range(4,8):
                            temp = False
                            for a in set[e]["state"]:
                                if "poison" in a:
                                    set[e]["state"][set[e]["state"].index(a)][1] = acts[i+4].calculation[1]
                                    temp = True
                                    print(f"{set[e]["name"]}'s damage over time debuff was extended")
                                    break
                            if temp == False and "alive" in set[e]["state"]:
                                set[e]["state"].append(["poison", acts[i].calculation[1], acts[i].calculation[2]])
                                print(f"{set[e]['name']} was struck with {acts[i].calculation[3]} by {set[i]['name']}")
            case "sp":
                match acts[i].calculation[0]:
                    case 0:
                        tar = [set[0], set[1], set[2], set[3]]
                        for e in tar:
                            if e["HP"] > 0:
                                del tar[tar.index(e)]
                        if len(tar) != 0:
                            tar = tar[random.randint(0, len(tar))]
                            n = set.index(tar)
                            set[n]["HP"] = 30
                            set[n]["state"].append("alive")
                            print(f"{set[n]["name"]} was revived by {set[i]["name"]}")
                        else:
                            print(f"{set[i]["name"]} had no targets to revive")
                    case 1:
                        for e in range(0,4):
                            for n in set[e]["state"]:
                                if n == "atkDW" or n == "spdDW" or n == "poison":
                                    set[e]["state"][set[e]["state"].index(n)][1] = 0
                        print(f"{set[i]["name"]} cleansed their team's negative effects")
                    case 2:
                        for e in range(4,8):
                            for n in set[e]["state"]:
                                if n == "atkUP" or n == "spdUP" or n == "poison":
                                    set[e]["state"][set[e]["state"].index(n)][1] = 0
                        print(f"{set[i]["name"]} cleansed their enemy's buffs")
            case None:
                pass
        
        if "ready" in set[i]["state"]:
            set[i]["state"].pop(set[i]["state"].index("ready"))
            time.sleep(1)

        set = checkHP(set)

        printMenus(set)

        match acts[i+4]["type"]:
            case "s":
                dmg = math.round(acts[i+4].calculation[0] * set[i]["attack"] * (random.randint(90,110) / 100))
                tar = [set[0], set[1], set[2], set[3]]
                for e in tar:
                    if e["HP"] <= 0:
                        del tar[tar.index(e)]
                    elif "taunt" in e["state"]:
                        tar = [e]
                        break
                tar = set[4+random.randint(0, len(tar))]
                temp = False
                a = 0
                for b in tar["state"]:
                        if "shield" in b:
                            temp = True
                            break
                        else:
                            a += 1
                n = set.index(tar)
                if temp:
                    set[n]["state"].pop(a)
                    print(f"{tar['name']} blocked the hit from {set[i+4]['name']}")
                else:    
                    set[n]["HP"] -= dmg
                    print(f"{set[i+4]['name']} did {dmg} damage to {tar['name']} with {acts[i+4]['name']}")
            case "a":
                dmg = math.round(acts[i].calculation[0] * set[i]["attack"] * (random.randint(90,110) / 100))
                for e in range(0,4):
                    temp = False
                    a = 0
                    for b in set[e]["state"]:
                        if "shield" in b:
                            temp = True
                            break
                        else:
                            a += 1
                    if temp:
                        set[e]["state"].pop(a)
                        print(f"{set[e]['name']} blocked the hit from {set[i+4]['name']}")
                    else:
                        set[e]["HP"] -= dmg
                        print(f"{set[i+4]['name']} did {dmg} damage to {set[e]['name']} with {acts[i+4]['name']}")
            case "h":
                heal = math.round(acts[i+4].calculation[0] * set[i+4]["maxHP"] * (random.randint(95,105) / 100))
                if acts[i].calculation[1] != "self":
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
                        n = set.index(tar)
                        if set[n]["HP"] + heal > set[n]["maxHP"]:
                            set[n]["HP"] = set[n]["maxHP"]
                        else:
                            set[n]["HP"] += heal
                    print(f"{set[i+4]['name']} healed {heal} HP to {len(valTar)} targets with {acts[i+4]['name']}")
                else:
                    set[i+4]["HP"] += heal
                    print(f"{set[i+4]['name']} healed {heal} HP to themself targets with {acts[i+4]['name']}")
            case "b":
                match acts[i].calculation[0]:
                    case 0:
                        for e in range(4,8):
                            temp = False
                            for a in set[e]["state"]:
                                if "atkUP" in a:
                                    set[e]["state"][set[e]["state"].index(a)][1] = acts[i+4].calculation[1]
                                    temp = True
                                    print(f"{set[e]["name"]}'s attack buff was extended")
                                    break
                            if temp == False and "alive" in set[e]["state"]:
                                set[e]["state"].append(["atkUP", acts[i+4].calculation[1]])
                                set[e]["attack"] = set[e]["attack"] * 1.5
                                print(f"{set[e]['name']}'s attack was buffed by {set[i+4]['name']}")
                    case 1:
                        for e in range(4,8):
                            temp = False
                            for a in set[e]["state"]:
                                if "spdUP" in a:
                                    set[e]["state"][set[e]["state"].index(a)][1] = acts[i+4].calculation[1]
                                    temp = True
                                    print(f"{set[e]["name"]}'s speed buff was extended")
                                    break
                            if temp == False and "alive" in set[e]["state"]:
                                set[e]["state"].append(["spdUP", acts[i+4].calculation[1]])
                                set[e]["speed"] -= 1
                                print(f"{set[e]['name']}'s speed was buffed by {set[i+4]['name']}")
                    case 2:
                        for e in range(4,8):
                            temp = False
                            for a in set[e]["state"]:
                                if "regen" in a:
                                    set[e]["state"][set[e]["state"].index(a)][1] = acts[i+4].calculation[1]
                                    temp = True
                                    print(f"{set[e]["name"]}'s regeneration buff was extended")
                                    break
                            if temp == False and "alive" in set[e]["state"]:
                                set[e]["state"].append(["regen", acts[i+4].calculation[1]])
                                set[e]["speed"] -= 1
                                print(f"{set[e]['name']}'s regeneration was buffed by {set[i+4]['name']}")
                    case 3:
                        for e in range(4,8):
                            temp = False
                            for a in set[e]["state"]:
                                if "shield" in a:
                                    set[e]["state"][set[e]["state"].index(a)][1] = acts[i+4].calculation[1]
                                    temp = True
                                    print(f"{set[e]["name"]}'s shield was extended")
                                    break
                            if temp == False and "alive" in set[e]["state"]:
                                set[e]["state"].append(["shield", acts[i+4].calculation[1]])
                                print(f"{set[e]['name']}'s was shielded by {set[i+4]['name']}")
            case "d":
                match acts[i].calculation[0]:
                    case 0:
                        for e in range(0,4):
                            temp = False
                            for a in set[e]["state"]:
                                if "atkDW" in a:
                                    set[e]["state"][set[e]["state"].index(a)][1] = acts[i+4].calculation[1]
                                    temp = True
                                    print(f"{set[e]["name"]}'s attack debuff was extended")
                                    break
                            if temp == False and "alive" in set[e]["state"]:
                                set[e]["state"].append(["atkDW", acts[i+4].calculation[1]])
                                set[e]["attack"] = set[e]["attack"] * (2/3)
                                print(f"{set[e]['name']}'s attack was debuffed by {set[i+4]['name']}")
                    case 1:
                        for e in range(0,4):
                            temp = False
                            for a in set[e]["state"]:
                                if "spdDW" in a:
                                    set[e]["state"][set[e]["state"].index(a)][1] = acts[i+4].calculation[1]
                                    temp = True
                                    print(f"{set[e]["name"]}'s speed debuff was extended")
                                    break
                            if temp == False and "alive" in set[e]["state"]:
                                set[e]["state"].append(["spdDW", acts[i+4].calculation[1]])
                                set[e]["speed"] += 1
                                print(f"{set[e]['name']}'s speed was debuffed by {set[i+4]['name']}")
                    case 2:
                        for e in range(0,4):
                            temp = False
                            for a in set[e]["state"]:
                                if "poison" in a:
                                    set[e]["state"][set[e]["state"].index(a)][1] = acts[i+4].calculation[1]
                                    temp = True
                                    print(f"{set[e]["name"]}'s damage over time debuff was extended")
                                    break
                            if temp == False and "alive" in set[e]["state"]:
                                set[e]["state"].append(["poison", acts[i+4].calculation[1], acts[i+4].calculation[2]])
                                print(f"{set[e]['name']} was struck with {acts[i].calculation[3]} by {set[i+4]['name']}")
            case "sp":
                match acts[i].calculation[0]:
                    case 0:
                        tar = [set[4], set[5], set[6], set[7]]
                        for e in tar:
                            if e["HP"] > 0:
                                del tar[tar.index(e)]
                        if len(tar) != 0:
                            tar = tar[random.randint(0, len(tar))]
                            n = set.index(tar)
                            set[n]["HP"] = 30
                            set[n]["state"].append("alive")
                            print(f"{set[n]["name"]} was revived by {set[i+4]["name"]}")
                        else:
                            print(f"{set[i+4]["name"]} had no targets to revive")
                    case 1:
                        for e in range(4,8):
                            for n in set[e]["state"]:
                                if n == "atkDW" or n == "spdDW" or n == "poison":
                                    set[e]["state"][set[e]["state"].index(n)][1] = 0
                        print(f"{set[i+4]["name"]} cleansed their team's negative effects")
                    case 2:
                        for e in range(0,4):
                            for n in set[e]["state"]:
                                if n == "atkUP" or n == "spdUP" or n == "poison":
                                    set[e]["state"][set[e]["state"].index(n)][1] = 0
                        print(f"{set[i+4]["name"]} cleansed their enemy's buffs")
                    case 3:
                        temp = True
                        for e in len(set[i+4]["state"].len()):
                            if "Bombed" in e:
                                temp = False
                        if temp:
                            set[i+4]["state"].append(["Bombed", 3])
                            print(f"{set[i+4]["name"]} activates their explosive vest")
                        else:
                            print(f"{set[i+4]["name"]} flailed about in agony")
            case None:
                pass
        
        if "ready" in set[i+4]["state"]:
            set[i]["state"].pop(set[i]["state"].index("ready"))
            time.sleep(1)

        set = checkHP(set)
    
        printMenus(set)
        
    # return set MAY BE UNNECESSARY

def checkHP(set):
    for a in range(8):
        if set[a]["HP"] <= 0:
            set[a]["state"].pop(set[a]["state"].index("alive"))
            for st in range(len(set[a]["state"])):
                if "bombed" in st:
                        dmg = set[a]["maxHP"]/4
                        for e in range(8):
                            set[e]["HP"] -= dmg
                        print(f"{set[a]["name"]} blew up, dealing {dmg} dmg to everyone")
                        set[a]["state"].pop(e)
                        time.sleep(1)
                        checkHP(set)
    # return set MAY BE UNNECESSARY
                    
def statusEffects(set):
    for i in range(8):
        if "alive" in set[i]["state"] and "ready" in set[i]["state"]:
            for e in range(len(set[i]["state"])):
                match set[i]["state"][e]:
                    case "atkUP":
                        set[i]["state"][e][1] -= 1
                        if set[i]["state"][e][1] < 1:
                            set[i]["state"].pop(e)
                            set[i]["speed"] *= (2/3)
                            print(f"{set[i]["name"]}'s attack buff ended")
                    case "spdUP":
                        set[i]["state"][e][1] -= 1
                        if set[i]["state"][e][1] < 1:
                            set[i]["state"].pop(e)
                            set[i]["speed"] -= 1
                            print(f"{set[i]["name"]}'s speed buff ended")
                    case "regen":
                        set[i]["state"][e][1] -= 1
                        if set[i]["state"][e][1] < 1:
                            set[i]["state"].pop(e)
                            print(f"{set[i]["name"]}'s regeneration buff ended")
                        else:
                            set[i]["HP"] += math.round(set[i]["HP"]/5)
                    case "shield":
                        set[i]["state"][e][1] -= 1
                        if set[i]["state"][e][1] < 1:
                            set[i]["state"].pop(e)
                            print(f"{set[i]["name"]}'s shield ended")
                        
                    case "atkDW":
                        set[i]["state"][e][1] -= 1
                        if set[i]["state"][e][1] < 1:
                            set[i]["state"].pop(e)
                            set[i]["speed"] *= 1.5
                            print(f"{set[i]["name"]}'s attack debuff ended")
                    case "spdUP":
                        set[i]["state"][e][1] -= 1
                        if set[i]["state"][e][1] < 1:
                            set[i]["state"].pop(e)
                            set[i]["speed"] -= 1
                            print(f"{set[i]["name"]}'s speed debuff ended")
                    case "poison":
                        set[i]["state"][e][1] -= 1
                        dmg = math.round(set[i]["state"][e][2] * random.randint(95,105) / 100)
                        if set[i]["state"][e][1] < 1:
                            set[i]["state"].pop(e)
                            print(f"{set[i]["name"]}'s {set[i]["state"][e][3]} ended")
                        else:
                            set[i]["HP"] -= dmg
                            print(f"{set[i]["name"]}'s {set[i]["state"][e][3]} dealt {dmg} dmg to them")

                    case "bombed":
                        if set[i]["state"][e][1] > 0:
                            print(f"{set[i]["name"]} will blow in {set[i]["state"][e][1]} turn(s)")
                            set[i]["state"][e][1] -= 1
                        else:
                            dmg = set[i]["maxHP"]/2
                            for e in range(8):
                                set[e]["HP"] -= dmg
                            print(f"{set[i]["name"]} blew up, dealing {dmg} dmg to everyone")
                            set[i]["state"].pop(e)
                            set[i]["HP"] = 0
                            checkHP(set)
                    case "taunt":
                        set[i]["state"].pop(e)
            time.sleep(1)
    # return set MAY BE UNNECESSARY
                
class action:
    all_actions = {}

    def __init__(self, name):
        self.name = name
        self.id = 0
        for n in actionDict["names"]:
            if name in n:
                self.id = actionDict["names"].index(n)
        for attr in ["type", "calculation"]:
            setattr(self, attr, actionDict[attr][self.id])
        action.all_actions.add(self)
    
    def del_self():
        action.all_actions.delete(self)
        del self

# Action types are as follows:
# Single | Area   | Healing       | Buffing       | Debuffing                                             | Special
# Calculations per type are as follows
# [%DMG] | [%DMG] | [%DMG,NO.TAR] | [BFID,LENGTH] | [DBFID,LENGTH,%DMG(if applicable),TXT(if applicable)] | [SPID]
# Buffs are as follows
# 0: Atk^    1: Spd^     2: Regen     3: Shield    4: Taunt
# Debuffs are as follows
# 0: AtkV    1: SpdV     2: DoT       3: 
# Specials are as follows
# 0: Revive  1: Cleanse  2: Undebuff  3: Kamikaze  4: 
#                                     ^Enemy only
actionDict = {
"names": [
["Bite", "Gun"], ["Crash", "Ram", "Broom spear","The f*** off beam","Punch","Complain","Ruler slap","Bat swing","Soul clutch", "Gun+"], ["Kill yourself NOW", "Sword slash"], ["Piercing glare", "Ultrakill", "Mega bite"], # Single attacks
["Pizza wheel", "Rap bomb", "Draw", "Clutch up"], ["Fire bomb", "Spirit bomb","Superiority complex","Missiles","Supersonic cry", "Unfunny joke"], ["Debris crash","Imminent danger"]# Area attacks
["Cupcake","Sunny day"], ["Gatorade jug", "Healing spell", "Healing bomb"], ["Healing grenade"], ["Ultraheal"], ["Acorn", "Cannibalism", "Apple", "Adrenaline shot"], ["Burger bite", "Phoenix feather"], # Heals
["Command","Gear up"], ["Inspire", "War scream", "Victory cry","Red glow"], ["Jam out", "Bad Apple!!", "Blatant harrasment", "Agility","Blue glow"], ["Sing"], ["Regenerative chitter","Green glow"], ["Block stance","Instant transmission","Strange occurence"], ["Taunt"], # Buffs
["Disturbing tone", "Funny look", "Demoralize", "Empathy", "Bone rattle", "Halloween scare"], ["Cripple", "Exhaust fumes", "Sticky solution", "Sticky situation", "Zap taser","MLP Jar","Slow down"], ["Bleeding slash", "Deep cuts"], ["Venom spray"], ["Fire breath", "Grease spray"], ["Scorching ray"], ["Headache"], # Debuffs
["Life ritual", "Full repair"], ["Cleanse", "Pace set"], ["Wash off", "Tears"], ["Kamikaze"] # Specials
], 
"type": [
"s","s","s","s"
"a","a","a",
"h","h","h","h","h","h",
"b","b","b","b","b","b","b",
"d","d","d","d","d","d","d",
"sp","sp","sp","sp"
],
"calculation": [
0.80, 1.00, 1.20, 1.50,
0.40, 0.60, 0.80,
[0.40, 2], [0.20, 4], [0.60, 3], [1.00, 2], [0.50, "self"], [0.30, "self"]
[0, 2], [0, 3], [1, 2], [2, 2], [2, 4], [3, 2], [4]
[0, 2], [1, 2], [2, 2, 0.50, "bleed"], [2, 3, 0.50, "poison"], [2, 3, 0.60, "burning"], [2, 2, 0.80, "scorching"], [2, 2, 0.80, "brain pain"],
[0], [1], [2], [3],
]
}