import combat as c, map as m, party as p
import math, time, re

# Input that removes all outside 
# re.sub('\\W+','', input("> "))
partyList = ["", "", "", ""]
def main():
    febbyfaber = p.character(1)
    febbyfaber.join_party(partyList, 1)
    chicchikin = p.character(0)
    chicchikin.join_party(partyList, 0)
    bonybuni = p.character(3)
    bonybuni.join_party(partyList, 3)
    foxifox = p.character(2)
    foxifox.join_party(partyList, 2)
    p.character.printChars()

if __name__ == "__main__":
    main()