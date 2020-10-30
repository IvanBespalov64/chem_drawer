from structure import Struct, Atom, Bond

#returns 0 if lower case and 1 if upper case
def getCase(a) -> int:
    if a.isupper():
        return 1
    else:
        return 0
#Returns True if a & b in same case and False if not
def sameCase(a, b) -> bool:
    return (getCase(a) == getCase(b))

#Make a list of args
def make_list(*lst):
    return list(lst)


def connectByDot(st1 : Struct, st2 : Struct, bond : Bond, first = -1, second = -1):
    st1.cycles.update(st2.cycles)
    st2.cycles.update(st1.cycles)
    #print(st1.cycles)
    if(st1.getSize() == 0):
        return st2;
    if(st2.getSize() == 0):
        return st1;
    if(first == -1):
        first = max(0, st1.getSize() - 1)
    if(second == -1):
        second = 0
    prev_size = st1.getSize()
    for i in range(st2.getSize()):
        st1.addAtom(st2._Struct__data[i]);
    st1.addBond(first, prev_size + second, bond)
    for i in range(st2._Struct__MAX_NUM_OF_ATOMS):
        for j in range(i + 1, st2._Struct__MAX_NUM_OF_ATOMS):
            if(st2._Struct__bondMatrix[i][j] != 0):
                st1.addBond(prev_size + i, prev_size + j, \
                             st2._Struct__bondMatrix[i][j])
    return st1;
