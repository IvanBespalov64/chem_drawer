class Atom:

    __type = "";

    def __init__(self, type):
        self.__type = type;

    def getType(self) -> str:
        return __type;

class Bond:

    #type could be:
    #1 - single-bond
    #2 - double-bond
    #3 - triple-bond
    __type = "";

    def __init__(self, type):
        self.__type = type;
