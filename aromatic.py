from struct import Struct, Atom, Bond
import atom_info as AtomInfo
import util_funcs as Utils

class Aromatic:
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

    #It will return Struct of current compound
    def generate(self) -> Struct:
        #Firstly we must write tokenizer
        return None;

    #This func is row form of tokenizer
    def row_tokenize(self, lst, cycles, pos) -> list:
        #lst - current parsed list
        #cycles - dict with cycles
        #pos - current position

        s =  self.smilesStr
        tag = ""

        if(pos >= len(s)):
            return lst

        if(s[pos] == '['):
            return self.row_tokenize(lst, cycles, pos + 1)

        if(s[pos] == '='):
            lst.append(Utils.make_list(Bond(2)))
            return self.row_tokenize(lst, cycles, pos + 1)

        if(s[pos] == '#'):
            lst.append(Utils.make_list(Bond(3)))
            return self.row_tokenize(lst, cycles, pos + 1)

        lst.append(Utils.make_list(Bond(1)))

        current_atom_str = str(s[pos])
        pos += 1

        print(current_atom_str[-1])

        while(pos < len(s) and s[pos].isalpha() \
              and (not Utils.sameCase(current_atom_str[-1], s[pos]))):
            current_atom_str += s[pos]
            pos += 1

        current_atom_str = current_atom_str.lower()

        if pos >= len(s):
            lst.append(Utils.make_list(Atom(current_atom_str)))
            return lst

        if s[pos] == ']':
            lst.append(Utils.make_list(Atom(current_atom_str)))
            return self.row_tokenize(lst, cycles, pos + 1)

        if s[pos].isnumeric():
            current_cycle_num_str = ""
            while(pos < len(s) and s[pos].isnumeric()):
                current_cycle_num_str += s[pos]
                pos += 1
            current_cycle_num = int(current_cycle_num_str)
            if current_cycle_num in cycles:
                cycles.pop(current_cycle_num)
                tag = "END_OF_CYCLE" + current_cycle_num_str
            else:
                cycles[current_cycle_num] = "STARTED"
                tag = "START_OF_CYCLE" + current_cycle_num_str

        if tag == "":
            lst.append(Utils.make_list(Atom(current_atom_str)))
            return self.row_tokenize(lst, cycles, pos)
        else:
            lst.append(Utils.make_list(Atom(current_atom_str), tag))
            return self.row_tokenize(lst, cycles, pos)

    #It will return a list of tuples, that had a atoms, bonds and tags
    #Cycles has one bond before their start
    def tokenize(self) -> list:
        return self.row_tokenize(list(), dict(), 0)
