class Atom:
    __type = ""

    def __init__(self, type_):
        self.__type = type_

    def __str__(self):
        return self.__type

    def __repr__(self):
        return self.__type

    def getType(self) -> str:
        return self.__type

class Bond:
    __type = 0

    def __init__(self, type_):
        self.__type = type_

    def getType(self):
        return __type

    def toChar(self):
        if self.__type == 1:
            return '-'
        elif self.__type == 2:
            return '='
        else:
            return '#'

    def __str__(self):
        return self.toChar()

    def __repr__(self):
        return self.toChar()


class Struct:

    __MAX_NUM_OF_ATOMS = 100

    __numOfBonds = dict() # For all atoms it wil has num of their bonds
    __data = dict()  # This dict for all atoms has their nums
    __bondMatrix = list()  # This matrix for all pairs of atoms has the bond type value or 0 if there is no bond
    __numOfAtoms = 0  # Current num of atoms in struct

    def __init__(self):
        self.__bondMatrix = [list(0 for i in range(self.__MAX_NUM_OF_ATOMS)) \
                             for i in range(self.__MAX_NUM_OF_ATOMS)]

    def hello(self):
        print("hello")

        # This function add new atom and return his num
    def addAtom(self, atom) -> int:
        self.__data[self.__numOfAtoms] = atom
        self.__numOfBonds[self.__numOfAtoms] = 0
        self.__numOfAtoms += 1
        return self.__numOfAtoms - 1

    # This function return False if bod was already made and True if atoms were just connected
    def addBond(self, num1, num2, bondType) -> bool:
        if self.__bondMatrix[num1][num2] != 0:
            return False
        self.__bondMatrix[num1][num2] = bondType
        self.__bondMatrix[num2][num1] = bondType
        self.__numOfBonds[num1] += bondType
        self.__numOfBonds[num2] += bondType
        return True

    #This func will return num of bonds, that atom has
    def getNumOfBonds(self, num) -> int:
        if num in self.__numOfBonds:
            return self.__numOfBonds[num]
        else:
            return 0
