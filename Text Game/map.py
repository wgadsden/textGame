# Arrows (^V<>) are "connections" between nodes
# (First) letter is the type of location
# S = start, F = fight, T = treasure, E = end/boss
# (Second) letter is the connections to other locations (Only locations)
# (Third) letter is if the location has been discovered or not (Only locations)
map1 = {
"row1": [["V>"],["<V>F",["2,1","3,3","1,3"],False],["<>T",["1,2","2,4"],False],["<V"]],
"row2": [["^VS",["1,2","3,3"],True],["^>"],[">V"],["^VE",["1,3","3,3"]],],
"row3": [["^>"],["<>"], ["<^>F",["2,1","1,2","2,4",],False],[">^"]]
}
final = []
for row in map1:
    totalRow = ["","","","",""]
    for column in row:
        node = ["     ","     ","  +  ","     ","     "]
        if ">" in column[0]:
            for i in range(3,5):
                node[2][i] = "-"
        if "<" in column[0]:
            for i in range(0,2):
                node[2][i] = "-"
        if "^" in column[0]:
            for i in range(0,2):
                node[i][2] = "|"
        if "V" in column[0]:
            for i in range(3,5):
                node[i][2] = "|"
        
        if "S" or "F" or "T" or "E" in column[0]:
            for i in range(1,4):
                node[1][i] = "-"
                node[3][i] = "-"
            node[2][1] = "|"
            node[2][3] = "|"
            if column[2] == True:
                node[2][2] = column[0][-1]
            else:
                node[2][2] = "?"
        
        for line in node:
            totalRow[node.index(line)] += node
    for line in totalRow:
        final.append(line)

for item in final:
    print(item)