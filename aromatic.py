class Aromatic:
    smilesStr = "";

    def __init__(self, smilesStr: str):
        self.smilesStr = smilesStr;

    def isAromatic(self) -> bool:
        #Current smilesStr must be correct SMILES sequense
        for c in self.smilesStr:
            if c.isalpha() and c.isupper():
                return False;
        else:
            return True;
