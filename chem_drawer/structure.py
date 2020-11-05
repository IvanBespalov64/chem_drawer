class StructureElement:
    pass

class Atom(StructureElement):

    def __init__(self, type_):
        self.ind = 0
        self.__type = type_

    def __str__(self):
        return self.__type

    def __repr__(self):
        return self.__type

    def getType(self) -> str:
        return self.__type

    def setInd(self, x : int):
        self.ind = x

    def getFormattedType(self) -> str:
        return str(self.__type[0].capitalize())

class Bond(StructureElement):

    def __init__(self, type_):
        self.__type = type_

    def getType(self):
        return self.__type

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


    def __init__(self):

        # Const value, Max number of atoms in struct
        self.__MAX_NUM_OF_ATOMS = 100
        # For every atom, that is start or end of cycle have info
        self.cycles = dict()
        # For all atoms it wil has num of their bonds
        self.__numOfBonds = dict()
        # This dict for all atoms has their nums
        self.__data = dict()
        # This matrix for all pairs of atoms has the bond type value or 0 if there is no bond
        self.__bondMatrix = list()
        # Better structure for containig graph for drawing
        self.adjacencyList = list()
        # Current num of atoms in struct
        self.__numOfAtoms = 0

        self.__bondMatrix = [list(0 for i in range(self.__MAX_NUM_OF_ATOMS)) \
                             for i in range(self.__MAX_NUM_OF_ATOMS)]

        self.adjacencyList = [list() \
                                for i in range(self.__MAX_NUM_OF_ATOMS)]


    # This function add new atom and return his num
    def addAtom(self, atom) -> int:

        atom.setInd(self.__numOfAtoms)

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
        self.adjacencyList[num1].append(num2)
        self.adjacencyList[num2].append(num1)
        self.__numOfBonds[num1] += bondType
        self.__numOfBonds[num2] += bondType
        return True

    # This func will return num of bonds, that atom has
    def getNumOfBonds(self, num) -> int:
        if num in self.__numOfBonds:
            return self.__numOfBonds[num]
        else:
            return 0


    def getMatrixElement(self, x, y) -> int:
        return self.__bondMatrix[x][y]

    def getAdjacencyList(self, v) -> list:
        return self.adjacencyList[v]

    def getAtom(self, i):
        return self.__data[i]

    def printBonds(self):
        print(self.__numOfBonds)

    # Returns num of atoms
    def getSize(self) -> int:
        return self.__numOfAtoms
