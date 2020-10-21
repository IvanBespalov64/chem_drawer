from compound import Compound
from struct import Struct, Atom, Bond
import atom_info as AtomInfo
import util_funcs as Utils

class Aromatic(Compound):
    smilesStr = ""
    tokens = list()

    def __init__(self, smilesStr: str):
        self.smilesStr = smilesStr
        self.tokens = self.tokenize()

    def isAromatic(self) -> bool:
        # Current smilesStr must be correct SMILES sequence
        for c in self.smilesStr:
            if c.isalpha() and c.isupper():
                return False
        else:
            return True

    

    
