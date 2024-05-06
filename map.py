""" All map-based functions """

def printMap(map,pos):
    final = []
    for row in map:
        totalRow = ["","","","",""]

        for column in row:
            node = ["     ","     ","  +  ","     ","     "]

            if ">" in column[0]:
                node[2] = list(node[2])
                for i in range(3,5):
                    node[2][i] = "-"
                node[2] = "".join(node[2])
            if "<" in column[0]:
                node[2] = list(node[2])
                for i in range(0,2):
                    node[2][i] = "-"
                node[2] = "".join(node[2])
            if "^" in column[0]:
                for i in range(0,2):
                    node[i] = list(node[i])
                    node[i][2] = "|"
                    node[i] = "".join(node[i])
            if "V" in column[0]:
                for i in range(3,5):
                    node[i] = list(node[i])
                    node[i][2] = "|"
                    node[i] = "".join(node[i])

            a = pos
            if column == map[int(a[0])-1][int(a[1])-1]:
                node[2] = list(node[2])
                node[2][1] = ">"
                node[2][3] = "<"
                node[2] = "".join(node[2])


            if "S" in column[0] or "F" in column[0] or "T" in column[0] or "B" in column[0] or "N" in column[0] or "L" in column[0]:
                for i in range(1,4):
                    node[i] = list(node[i])
                for i in range(1,4):
                    node[1][i] = "-"
                    node[3][i] = "-"
                    
                if column != map[int(a[0])-1][int(a[1])-1]:
                    node[2][1] = "|"
                    node[2][3] = "|"
                
                try:
                    match column[1]:
                        case True:
                            column[0] = list(column[0])
                            node[2][2] = column[0][-1]
                            column[0] = "".join(column[0])
                        case False:
                            node[2][2] = "?"
                except:
                    pass
                for i in range(1,4):
                    node[i] = "".join(node[i])

            for i in range(5):
                totalRow[i] += node[i]

        for line in totalRow:
            final.append(line)

    for item in final:
        print(item)
    print("S: Start | F: Fight | T: Treasure | B: Boss | N: Next | L: Last | ?: Undiscovered\n")

def movePos(map, pos):
    a = pos
    a[0] = int(a[0]) - 1
    a[1] = int(a[1]) - 1
    temp = ""
    if "^" in map[a[0]][a[1]][0]:
        temp += "U: up "
    if "V" in map[a[0]][a[1]][0]:
        temp += "| D: down "
    if "<" in map[a[0]][a[1]][0]:
        temp += "| L: left "
    if ">" in map[a[0]][a[1]][0]:
        temp += "| R: right"

    print(f"Which direction do you want to go?\n{temp.lstrip('|')}\nType c to access the character menu")

    match input("> ").lower():
        case "u":
            if "^" in map[a[0]][a[1]][0]:
                temp = f"{a[0]},{a[1]+1}"
            else:
                print("Invalid direction")
        case "d":
            if "V" in map[a[0]][a[1]][0]:
                temp = f"{a[0]+2},{a[1]+1}"
            else:
                print("Invalid direction")
        case "l":
            if "<" in map[a[0]][a[1]][0]:
                temp = f"{a[0]+1},{a[1]}"
            else:
                print("Invalid direction")
        case "r":
            if ">" in map[a[0]][a[1]][0]:
                temp = f"{a[0]+1},{a[1]+2}"
            else:
                print("Invalid direction")
        case "c":
            return "exit"
        case None:
            print("Invalid input")

    if temp != pos:
        return temp
    else:
        return None

def checkPos(map, pos):
    a = pos
    a[0] = int(a[0]) - 1
    a[1] = int(a[1]) - 1
    if False in map[a[0]][a[1]]:
        map[a[0]][a[1]][1] = True
        match map[a[0]][a[1]][0][-1]:
            case "F":
                return "fight"
            case "T":
                return "treasure"
            case "B":
                return "boss"
    else:
        match map[a[0]][a[1]][0][-1]:
            case "N":
                return "next"
            case "L":
                return "back"

def findPos(map, tar):
    for r in map:
        for c in map:
            if tar in c[0]:
                return [r,c]