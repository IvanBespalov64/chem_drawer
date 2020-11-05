# Note!!!!!
# It is important, that in tokens' list
# All contains in lists, BUT tags joined
# with Atoms in TUPLES

from chem_drawer.structure import Struct, Atom, Bond, StructureElement
import chem_drawer.util_funcs as Utils
import chem_drawer.atom_info as AtomInfo

class Compound:

    __START_CYCLE_TAG = "START_OF_CYCLE"
    __END_CYCLE_TAG = "END_OF_CYCLE"

    def __init__(self, smilesStr: str):

        # List of cycles
        self.cy_list = list()

        self.subtype_tag = ""
        self.smilesStr = smilesStr
        self.tokens = self.tokenize()

    def setSubtypeTag(self, subtypeTag : str):
        self.subtype_tag = subtypeTag

    #It will return Struct of current compound
    def row_generate(self, struct, last, cur_bond, current_token, cycles) -> Struct:
        for token in current_token:
            current_tag = ""
            while(isinstance(token, list) and len(token) == 1):
                token = token[0]
            if(isinstance(token, tuple)):
                current_tag = token[1]
                token = token[0]
            if(isinstance(token, list)):
                if(isinstance(token[0], list) and \
                   isinstance(token[0][0], Bond)):
                    cur_bond = token[0][0].getType()
                    struct =  Utils.connectByDot(struct, \
                                self.row_generate(Struct(), \
                                -1, 0, token[1:], cycles), cur_bond, last)
                else:
                    struct =  Utils.connectByDot(struct, \
                                self.row_generate(Struct(), \
                                -1, 0, token, cycles), cur_bond, last)

            if(isinstance(token, Atom)):
                ind = struct.addAtom(token)
                if(cur_bond != 0):
                    struct.addBond(last, ind, cur_bond)
                    cur_bond = 0
                last = ind
            elif(isinstance(token, Bond)):
                cur_bond = token.getType()
            if(current_tag != ""):
                cycle_num_str = "";
                if(self.__START_CYCLE_TAG in current_tag):
                    pos = current_tag.find(self.__START_CYCLE_TAG) \
                        + len(self.__START_CYCLE_TAG)
                    while(pos < len(current_tag) \
                          and current_tag[pos].isnumeric()):
                        cycle_num_str += current_tag[pos]
                        pos += 1
                    cycle_num = int(cycle_num_str)
                    cycles[cycle_num] = (last, max(1, cur_bond))
                    struct.cycles[last] = "START"
                elif(self.__END_CYCLE_TAG in current_tag):
                    pos = current_tag.find(self.__END_CYCLE_TAG) \
                        + len(self.__END_CYCLE_TAG)
                    while(pos < len(current_tag) \
                          and current_tag[pos].isnumeric()):
                        cycle_num_str += current_tag[pos]
                        pos += 1
                    cycle_num = int(cycle_num_str)
                    struct.addBond(last, cycles[cycle_num][0], \
                                       cycles[cycle_num][1])
                    struct.cycles[last] = "END"
        return struct

    # This func will build a graph that will in Struct
    # Of current compound by a tokenized smiles string
    def generate(self) -> Struct:
        ans = self.row_generate(Struct(), 0, 0, self.tokens, dict())
        self.find_cycles()
        return ans

    def row_find_cycles(self, cur_list, cur_token):
        cycle_ends = dict()

        for i in range(len(cur_token)):
            token = cur_token[i]
            if(len(token) != 2):
                continue
            if(isinstance(token[0], Atom) and isinstance(token[1], str)):
                if('END' in token[1]):
                    cycle_ends[Utils.parseNumOfCycleFromTag(token[1])] = i

        startedCycles = list()
        i = 0
        while (i < len(cur_token)):
            #print(cur_list)
            token = cur_token[i]
            # Max len of single info list - 2 (Atom + tag)
            # if it > 2 -> sublist
            if(len(token) > 2):
                i += 1
                self.row_find_cycles(list(), token)
            if isinstance(token[0], Atom):
                if(len(token) == 2 and isinstance(token[1], str)):
                    if("START" in token[1]):
                        if(len(startedCycles) != 0):
                            self.row_find_cycles(list(), cur_token[i:(cycle_ends[Utils.parseNumOfCycleFromTag(token[1])] + 1)])
                            cur_list.append(token[0].ind)
                            cur_list.append(\
                                cur_token[cycle_ends\
                                [Utils.parseNumOfCycleFromTag(\
                                token[1])]][0].ind)
                            i = cycle_ends\
                                [Utils.parseNumOfCycleFromTag(token[1])] + 1
                            continue
                        else:
                            startedCycles.append( \
                                  Utils.parseNumOfCycleFromTag(token[1]))
                if(len(startedCycles) != 0):
                    cur_list.append(token[0].ind)
                if(len(token) == 2 and isinstance(token[1], str)):
                    if("END" in token[1]):
                        startedCycles.pop()
            i += 1
        self.cy_list.append(cur_list)

    def find_cycles(self):
        self.row_find_cycles(list(), self.tokens)

    #This func is row form of tokenizer
    def row_tokenize(self, lst, cycles, pos, end, connected = False) -> list:
        #lst - current parsed list
        #cycles - dict with cycles
        #pos - current position

        s =  self.smilesStr
        tag = ""

        brackets = dict()
        stack = list()

        for i in range(len(s)):
            if(s[i] == '('):
                stack.append(i)
            if(s[i] == ')'):
                brackets[stack.pop()] = i

        if(self.subtype_tag != ""):
            tag += self.subtype_tag + "_"

        if(pos >= end):
            return lst

        if(s[pos] == '['):
            return self.row_tokenize(lst, cycles, pos + 1, end)

        if(s[pos] == ')'):
            return self.row_tokenize(lst, cycles, pos + 1, end)

        if(s[pos] == '('):
            new_pos = brackets[pos]
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
                tag += self.__END_CYCLE_TAG + current_cycle_num_str
            else:
                cycles[current_cycle_num] = "STARTED"
                tag += self.__START_CYCLE_TAG + current_cycle_num_str

        if tag == "":
            lst.append(Utils.make_list(Atom(current_atom_str)))
            return self.row_tokenize(lst, cycles, pos, end)
        else:
            lst.append((Atom(current_atom_str), tag))
            return self.row_tokenize(lst, cycles, pos, end)

    #It will return a list of tuples, that had a atoms, bonds and tags
    #Cycles has no bonds before their start, only tags
    #In smiles string you mast write a type of bond in the branch
    #(ex. CC(=O)C and NOT CC=(O)C)
    def tokenize(self) -> list:
        return self.row_tokenize(list(), dict(), 0, len(self.smilesStr))
