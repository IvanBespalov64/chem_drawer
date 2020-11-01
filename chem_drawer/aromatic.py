from chem_drawer.compound import Compound
from chem_drawer.structure import Struct, Atom, Bond
import chem_drawer.atom_info as AtomInfo
import chem_drawer.util_funcs as Utils

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
