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
    return lst
