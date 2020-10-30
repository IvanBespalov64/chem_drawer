from structure import Struct

import math
import sys
from PIL import Image, ImageDraw

class Drawer:

    __bondLength = 20

    #This func wil draw our graph
    def DepthFirstSearch(self, st : Struct, drawed, cur, pos, im : Image):
        print(pos)
        size = st.getSize()
        num_of_neighbours = 0
        draw = ImageDraw.Draw(im)
        drawed[cur] = True
        for i in range(size):
            if(st.getMatrixElement(cur, i) != 0):
                num_of_neighbours += 1
        cur_degree = 120
        if(num_of_neighbours > 3):
            cur_degree = 360 / num_of_neighbours
        step = cur_degree
        cur_degree /= 2
        k = 1 -   2 * (len(drawed) % 2);
        for i in range(size):
            if((not i in drawed) and st.getMatrixElement(cur, i) != 0):
                new_pos = (pos[0] + self.__bondLength * \
                    math.sin(math.radians(cur_degree)), \
                    pos[1] + self.__bondLength * \
                    k * math.cos(math.radians(cur_degree)))
                #print(pos + new_pos)
                draw.line(pos + new_pos, fill = (0, 0, 0, 255), width = 2)
                cur_degree += step
                im = self.DepthFirstSearch(st, drawed, i, new_pos, im)

        del draw
        return im

    def genImage (self, st : Struct) -> Image:
        t_im = self.DepthFirstSearch(st, dict(), 0, (20, 200), \
                        Image.new('RGBA', (600, 400), (255, 255, 255, 255)))
        t_im.show()
