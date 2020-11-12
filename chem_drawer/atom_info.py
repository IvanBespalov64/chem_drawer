from chem_drawer.structure import Atom

# For all atom names it will return num of valent electrons
__atom_info = dict()
__colors = {
    "n" : (0, 0, 255, 255),
    "o" : (255, 0, 0, 255),
    "s" : (0, 255, 0, 255),
    "h" : (255, 255, 255, 255),
    "b" : (255, 255, 0, 255),
    "default" : (125, 0, 125, 255)
}

def getValentElectrons(atom : Atom) -> int:
    return 0

def getColor(atom : Atom) -> tuple:
    if(atom.getType() in __colors):
        return __colors[atom.getType()]
    else:
        return __colors["default"]
