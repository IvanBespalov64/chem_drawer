from chem_drawer.structure import Struct
import chem_drawer.atom_info as AtomInfo

import math
import sys
from PIL import Image, ImageDraw, ImageFont

class Drawer:

    __bondLength = 40

    # A half-dist between bonds in doublebond
    __d = 2
    # A half-dist between bonds in triplebond
    __td = 4

    def __init__(self):
        #Will descript
        self.__max_x = 0
        self.__max_y = 0
        self.__min_x = 2000
        self.__min_y = 2000

        #for all atoms will have their positions
        self.atom_pos = dict()

    #This func wil draw our graph
    def DepthFirstSearch(self, st : Struct, drawed, cur, pos, im : Image):
        self.atom_pos[cur] = pos
        #Updating size of molecule to correct drawing
        self.__min_x = min(self.__min_x, pos[0])
        self.__max_x = max(self.__max_x, pos[0])
        self.__min_y = min(self.__min_y, pos[1])
        self.__max_y = max(self.__max_y, pos[1])

        size = st.getSize()
        draw = ImageDraw.Draw(im)
        drawed[cur] = True

        #Calculating degree between bonds
        cur_degree = 120
        num_of_neighbours = len(st.getAdjacencyList(cur))
        if(num_of_neighbours > 3):
            cur_degree = 360 / num_of_neighbours
        step = cur_degree
        cur_degree /= 2
        k = 1 - 2 * (len(drawed) % 2)

        next_positions = list()
        for u in st.getAdjacencyList(cur):
            if(not u in drawed):
                next_positions.append((pos[0] + self.__bondLength * \
                    math.sin(math.radians(cur_degree)), \
                    pos[1] + self.__bondLength * \
                    k * math.cos(math.radians(cur_degree))))
                cur_degree += step
        position_counter = 0
        for u in st.getAdjacencyList(cur):
            if(not u in drawed):
                new_pos = next_positions[position_counter]
                position_counter += 1

                if(st.getMatrixElement(cur, u) == 1):
                    draw.line(pos + new_pos, fill = (0, 0, 0, 255), width = 3)
                elif(st.getMatrixElement(cur, u) == 2):
                    x_ = 0
                    y_ = 0
                    tg_a = 0
                    if((new_pos[0] - pos[0]) != 0):
                        tg_a = (new_pos[1] - pos[1]) / (new_pos[0] - pos[0])
                        x_ = self.__d * tg_a / math.sqrt(1 + tg_a ** 2)
                        y_ = self.__d / math.sqrt(1 + tg_a ** 2)
                    else:
                        x_ = self.__d
                    draw.line((pos[0] - x_, pos[1] + y_,\
                               new_pos[0] - x_, new_pos[1] + y_),\
                               fill = (0, 0, 0, 255), width = 3)
                    draw.line((pos[0] + x_, pos[1] - y_,\
                               new_pos[0] + x_, new_pos[1] - y_),\
                               fill = (0, 0, 0, 255), width = 3)
                elif(st.getMatrixElement(cur, u) == 3):
                    new_pos = (pos[0] + self.__bondLength * \
                               math.sin(math.radians(cur_degree)), \
                               pos[1] + self.__bondLength * \
                               p_k * math.cos(math.radians(cur_degree)))
                    x_ = 0
                    y_ = 0
                    tg_a = 0
                    if((new_pos[0] - pos[0]) != 0):
                        tg_a = (new_pos[1] - pos[1]) / (new_pos[0] - pos[0])
                        x_ = self.__td * tg_a / math.sqrt(1 + tg_a ** 2)
                        y_ = self.__td / math.sqrt(1 + tg_a ** 2)
                    else:
                        x_ = self.__td
                    draw.line((pos[0] - x_, pos[1] + y_,\
                           new_pos[0] - x_, new_pos[1] + y_),\
                           fill = (0, 0, 0, 255), width = 2)
                    draw.line((pos[0] + x_, pos[1] - y_,\
                           new_pos[0] + x_, new_pos[1] - y_),\
                           fill = (0, 0, 0, 255), width = 2)
                    draw.line(pos + new_pos, fill = (0, 0, 0, 255), width = 3)
                if(cur in st.cycles and st.cycles[cur] == "START"):
                    im = self.DepthFirstSearch(st, drawed, u, new_pos, im)
                elif(cur in st.cycles and st.cycles[cur] == "END"):
                    im = self.DepthFirstSearch(st, drawed, u, new_pos, im)
                else:
                    im = self.DepthFirstSearch(st, drawed, u, new_pos, im)

            elif((cur in st.cycles) and (u in st.cycles) \
                 and (st.cycles[u] == "START") and \
                 (st.cycles[cur] == "END")):
                draw.line(pos + self.atom_pos[u], \
                          fill = (0, 0, 0, 255), width = 2)

        if(st.getAtom(cur).getType() != 'c'):
            draw.ellipse((pos[0] - 3, pos[1] - 3, pos[0] + 3, pos[1] + 3), fill = (0, 0, 0, 0), outline = (0, 0, 0, 0))
            draw.text((pos[0] - 2, pos[1] - 5), \
                      st.getAtom(cur).getFormattedType(), \
                      font = ImageFont.load_default(), fill = \
                      AtomInfo.getColor(st.getAtom(cur)))

        del draw
        return im

    def genImage (self, st : Struct) -> Image:
        for i in range(st.getSize()):
            st.adjacencyList[i].sort(key = lambda x: \
                                     len(st.adjacencyList[x]), reverse = True)
        t_im = self.DepthFirstSearch(st, dict(), 0, (200, 200), \
                        Image.new('RGBA', (2000, 1000), (255, 255, 255, 0)))
        width = math.ceil(self.__max_x - self.__min_x)
        height = math.ceil(self.__max_y - self.__min_y)

        im = t_im.crop((self.__min_x - 10, self.__min_y - 10, \
                        self.__max_x + 10, self.__max_y + 10))
        im.show()
