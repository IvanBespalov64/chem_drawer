from struct import Struct, Atom
import atom_info as AtomInfo


class Aromatic:
    smilesStr = ""

    def __init__(self, smilesStr: str):
        self.smilesStr = smilesStr

    def isAromatic(self) -> bool:
        # Current smilesStr must be correct SMILES sequence
        for c in self.smilesStr:
            if c.isalpha() and c.isupper():
                return False
        else:
            return True

    def generate(self) -> Struct:

        if not self.isAromatic():
            return None

        __num_of_carbon = 0  # Number of carbon atoms
        __num_of_possible = 0  # Number of electron pairs, that cun be donored to congureated system
        for c in self.smilesStr:
            if not c.isalpha():
                continue
            if c == 'c':
                __num_of_carbon += 1
            if AtomInfo.getValentElctrons(Atom(c)) > 4:
                __num_of_possible += (AtomInfo.getValentElctrons(Atom(c)) - 4)
