class Atom:

    __type = "";

    def __init__(self, type):
        self.__type = type;

    def getType(self) -> str:
        return __type;

class Struct:

    #This dict for all atoms has their nums
    __data = {};
    #This matrix for all pairs of atoms has th bond type value or 0 if their is no bond
    __bondMatrix = {};
    #Current num of atoms in struct
    __numOfAtoms = 0;

    #This function add new atom and retrun his num
    def addAtom(self, atom) -> int:
        __data[__numOfAtoms] = atom;
        __numOfAtoms = __numOfAtoms + 1;
        return __numOfAtoms - 1;

    #This function return Flase if bod was already made and True if atoms were just connected
    def addBond(self, num1, num2, bondType) -> bool:
        if __bondMatrix[num1][num2] != 0:
            return False;
        __bondMatrix[num1][num2] = bondType;
        __bondMatrix[num2][num1] = bondType;
        return True;
