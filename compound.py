from struct import Struct, Atom, Bond
import util_funcs as Utils
import atom_info as AtomInfo

class Compound:

    smilesStr = ""
    tokens = list()

    def __init__(self, smilesStr: str):
        self.smilesStr = smilesStr
        self.tokens = self.tokenize()

    #It will return Struct of current compound
    def generate(self) -> Struct:
        #Firstly we must write tokenizer
        return None;

    #This func is row form of tokenizer
    def row_tokenize(self, lst, cycles, pos, end, connected = False) -> list:
        #lst - current parsed list
        #cycles - dict with cycles
        #pos - current position

        s =  self.smilesStr
        tag = ""

        if(pos >= end):
            return lst

        if(s[pos] == '['):
            return self.row_tokenize(lst, cycles, pos + 1, end)

        if(s[pos] == ')'):
            return self.row_tokenize(lst, cycles, pos + 1, end)

        if(s[pos] == '('):
            new_pos = s.find(')', pos)
            print(new_pos)
            lst.append(self.row_tokenize(list(), dict(), pos + 1, new_pos))
            return self.row_tokenize(lst, cycles, new_pos + 1, end)

        if(s[pos] == '='):
            lst.append(Utils.make_list(Bond(2)))
            return self.row_tokenize(lst, cycles, pos + 1, end, True)

        if(s[pos] == '#'):
            lst.append(Utils.make_list(Bond(3)))
            return self.row_tokenize(lst, cycles, pos + 1, end, True)

        if((not connected) and (pos != 0)):
            lst.append(Utils.make_list(Bond(1)))

        current_atom_str = str(s[pos])
        pos += 1

        while((pos < end) and s[pos].isalpha() \
              and (not Utils.sameCase(current_atom_str[-1], s[pos]))):
            current_atom_str += s[pos]
            pos += 1

        current_atom_str = current_atom_str.lower()

        if(pos >= end):
            lst.append(Utils.make_list(Atom(current_atom_str)))
            return lst

        if s[pos] == ']':
            lst.append(Utils.make_list(Atom(current_atom_str)))
            return self.row_tokenize(lst, cycles, pos + 1, end)

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
            return self.row_tokenize(lst, cycles, pos, end)
        else:
            lst.append(Utils.make_list(Atom(current_atom_str), tag))
            return self.row_tokenize(lst, cycles, pos, end)

    #It will return a list of tuples, that had a atoms, bonds and tags
    #Cycles has no bonds before their start, only tags
    #In smiles string you mast write a type of bond in the branch
    #(ex. CC(=O)C and NOT CC=(O)C)
    def tokenize(self) -> list:
        return self.row_tokenize(list(), dict(), 0, len(self.smilesStr))
