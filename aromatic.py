from compound import Compound
from struct import Struct, Atom, Bond
import atom_info as AtomInfo
import util_funcs as Utils

class Aromatic(Compound):

    def __init__(self, smilesStr: str):
        super().setSubtypeTag("AROMATIC");

        self.smilesStr = smilesStr
        self.tokens = self.tokenize()

    def isAromatic(self) -> bool:
        # Current smilesStr must be correct SMILES sequence
        for c in self.smilesStr:
            if c.isalpha() and c.isupper():
                return False
        else:
            return True
