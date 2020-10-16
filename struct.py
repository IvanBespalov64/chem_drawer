class Atom:
    __type = ""

    def __init__(self, type_):
        self.__type = type_

    def getType(self) -> str:
        return self.__type


class Struct:

    __MAX_NUM_OF_ATOMS = 100

    __data = dict()  # This dict for all atoms has their nums
    __bondMatrix = list()  # This matrix for all pairs of atoms has the bond type value or 0 if there is no bond
    __numOfAtoms = 0  # Current num of atoms in struct

    def __init__(self):
        self.__bondMatrix = [list(0 for i in range(self.__MAX_NUM_OF_ATOMS)) \
                             for i in range(self.__MAX_NUM_OF_ATOMS)]

    # This function add new atom and return his num
    def addAtom(self, atom) -> int:
        self.__data[self.__numOfAtoms] = atom
        __numOfAtoms = self.__numOfAtoms + 1
        return __numOfAtoms - 1

    # This function return False if bod was already made and True if atoms were just connected
    def addBond(self, num1, num2, bondType) -> bool:
        if self.__bondMatrix[num1][num2] != 0:
            return False
        self.__bondMatrix[num1][num2] = bondType
        self.__bondMatrix[num2][num1] = bondType
        return True
