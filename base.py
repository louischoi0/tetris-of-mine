import time
import random
import pdb
import copy
import threading
from threading import Lock
import sys

EXIT = False
CONSOLE = 0
X_START = 4
Y_START = 21
X_MAX = 10
Y_MAX = 26
X_VISUAL_MAX = 10
Y_VISUAL_MAX = 23

BlockIndex = [ "stick" , "cube", "mout" , "twizle" , "twizler" ,"hook"]
BlockMap = {
    'stick' :  ( ((0,0) , (0,1) , (0,2) , (0,3)) , ((0,0), (1,0),(2,0), (3,0)) ) ,
    'cube' :  ( ((0, 0) , (1,0), (0,1) , (1,1)) ,) ,
    'mout' :
                (
                    ((0,0),(1,0),(2,0),(1,1))  , ((0,0),(0,1),(0,2),(1,1)),
                    ((0,0),(-1,1),(0,1),(1,1)) , ((0,0),(-1,1),(0,1),(0,2))
                ),
    'twizle' : ( ((0,0) ,(1,0), (1,1), (2,1)) , ((0,0), (0,1),(-1,1),(-1,2)) ),
    'twizler' :( ((0,0) ,( -1 ,0) , (-1,1), (-2,1)) , ((0,0), (0,1), (1,1), (1,2))  ),
    #'hook' :(((0,0), (0,1),(0,2),(1,0)),()
    #'hookr' :(())
}
TransPos = {
    'stick' : ( (-2, 2),( 2, -2) ),
    'cube' : (),
    'mout' : ( (1,-1),(0,0),(0,0),(-1,1)),
    'twizle' : ((1,-1),(-1,1)),
    'twizler' : ((-1,0),(1,0))
}
MaxMinX = {
    'stick' : ((0,X_MAX) , (0, X_MAX - 3)),
    'cube' : ((0, X_MAX - 1),),
    'mout' : ((0, X_MAX -2),(0, X_MAX - 1),(0, X_MAX - 2),(0, X_MAX - 1)),
    'twizle' : ((0, X_MAX -2) ,(1, X_MAX)),
    'twizler' : ((2, X_MAX) , (0,X_MAX -1))
}
InvestigatePos = {
    'stick' : (( True, False, False, False) , (True , True, True, True)),
    'cube' : ( (True, True , False , False), ),
    'mout' : ( (True,True,True, False), (True,False,False,True),(True,True,False,True),(True,True,False,False)),
    'twizle' : ( (True,True,False,True), (True,False,True,False) ),
    'twizler' : ( (True,True , False, False), (True,False,True,False) )
}

InvestigateLeftPos = {
    'stick' : ((True,True,True,True), (True, False,False,False)),
    'cube' : ( (True,False,True,False), ),
    'mout' : ( (True,False,False,True), (True,True,True,False), (True,True,False,False),(True,True,False,True)),
    'twizle' : ((True,False,True,False),(True,False,True,True)),
    'twizler' : ((False,True,False,True),(True,True,False,True))
}

InvestigateRightPos = {
    'stick' : ((True,True,True,True),(False,False,False,True)),
    'cube' : ( (False,True,False,True), ),
    'mout' : ((False,False,True,True),(True,False,True,True),(True,False,False,True),(True,False,True,True)),
    'twizle' : ((False,True,False,True),(True,True,False,True)),
    'twizler' :((True,False,True,False),(True,False,True,True))
}
FormCount = {
    'stick' : 2,
    'cube' : 1,
    'mout' : 4,
    'twizle' : 2,
    'twizler' : 2
}

def update_pos_block(blc) :
        finpos = [ [self.X + BlockMap[self.name][self.trans][0][0] , self.Y + BlockMap[self.name][self.trans][0][1]]
                        [self.X + BlockMap[self.name][self.trans][1][0] , self.Y + BlockMap[self.name][self.trans][1][1]] ,
                        [self.X + BlockMap[self.name][self.trans][2][0] , self.Y + BlockMap[self.name][self.trans][2][1]] ,
                        [self.X + BlockMap[self.name][self.trans][3][0] , self.Y + BlockMap[self.name][self.trans][3][1]] ]
        return finpos

class block(object):

    def __init__(self,name,map):
        self.maxHeight = 0
        self.map = map
        self.X = X_START
        self.Y = Y_START
        self.name = name
        self.trans = 0
        self.finpos = [ [self.X + BlockMap[name][0][0][0] , self.Y + BlockMap[self.name][0][0][1]]  ,
                        [self.X + BlockMap[name][0][1][0] , self.Y + BlockMap[self.name][0][1][1]] ,
                        [self.X + BlockMap[name][0][2][0] , self.Y + BlockMap[self.name][0][2][1]] ,
                        [self.X + BlockMap[name][0][3][0] , self.Y + BlockMap[self.name][0][3][1]] ]
    def update_pos(self) :
        self.finpos = [ [self.X + BlockMap[self.name][self.trans][0][0] , self.Y + BlockMap[self.name][self.trans][0][1]]  ,
                        [self.X + BlockMap[self.name][self.trans][1][0] , self.Y + BlockMap[self.name][self.trans][1][1]] ,
                        [self.X + BlockMap[self.name][self.trans][2][0] , self.Y + BlockMap[self.name][self.trans][2][1]] ,
                        [self.X + BlockMap[self.name][self.trans][3][0] , self.Y + BlockMap[self.name][self.trans][3][1]] ]
    def set_trans(self,i) :
        self.trans = i
    def get_trans(self) :
        return self.trans
    def move(self , Xoff , Yoff):
        self.X += Xoff
        self.Y += Yoff
        self.update_pos()
    def transpose_poss(self, mapp) :
        tX = self.X + TransPos[self.name][self.trans][0]
        tY = self.Y + TransPos[self.name][self.trans][1]
        if tX < 0 or tX >= X_VISUAL_MAX or tY < 0 :
            return False
        transf = (self.trans + 1) % FormCount[self.name]
        tfinpos = [ [tX + BlockMap[self.name][transf][0][0] , tY + BlockMap[self.name][transf][0][1]]  ,
                        [tX + BlockMap[self.name][transf][1][0] , tY + BlockMap[self.name][transf][1][1]] ,
                        [tX + BlockMap[self.name][transf][2][0] , tY + BlockMap[self.name][transf][2][1]] ,
                        [tX + BlockMap[self.name][transf][3][0] , tY + BlockMap[self.name][transf][3][1]] ]
        for i in tfinpos :
            if i[0] < 0 or i[0] >= X_VISUAL_MAX or i[1] < 0 :
                return False
            if mapp[i[0]][i[1]] == 1 :
                return False
        return True
    def transpose(self) :
        if FormCount[self.name] == 1:
            return
        if not self.transpose_poss(self.map) :
            return
        self.X += TransPos[self.name][self.trans][0]
        self.Y += TransPos[self.name][self.trans][1]
        self.trans = (self.trans + 1) % FormCount[self.name]
        self.update_pos()
    def get_mark(self) :
        return (self.X , self.Y)
    def get_y(self) :
        return self.Y
    def set_y(self, y) :
        self.Y = y
    def final_position(self) :
        self.update_pos()
        return self.finpos
    def move_left(self) :
        self.X -= 1
        self.update_pos()
    def move_right(self) :
        self.X += 1
        self.update_pos()
    def move_down(self) :
        self.Y -= 1
        self.update_pos()
    def get_name(self) :
        return self.name
    def get_x(self) :
        return self.X
    def set_x(self,x) :
        self.X = x
    def check_position(self) :
        for i in self.finpos :
            print( "%d , %d" %(i[0] , i[1]))

    def get_inv_list(self) :
        return InvestigatePos[self.name][self.trans]
    def get_inv_left_list(self) :
        return InvestigateLeftPos[self.name][self.trans]
    def get_inv_right_list(self) :
        return InvestigateRightPos[self.name][self.trans]
class Render(object) :

    def __init__(self, master) :
        self.end = False
        self.map = [[0 for row in range (Y_MAX)] for row in range(X_MAX)]
        self.falling = None
        self.block_line = ''
        self.master = master
        self.downposs = True
        self.frame = 0
        self.fin = False
        idx = random.randrange(0,4)
        self.create_blocks(idx,self.map)
        self.draw_falling_bloc()
        self.maxHeight = 0

    def set_failling_block(self, bloc) :
        self.falling = bloc
    def inv_falling_area(self, x , y) :
        pos = self.falling.final_position()
        for i in range(0,4) :
            if pos[i][0] == x and pos[i][1] == y :
                return True
        return False
    def next_frame(self) :
        pos = self.falling.final_position()
        inv = self.falling.get_inv_list()
        for i in range(0,4) :
            if inv[i] :
                if self.map[pos[i][0]][pos[i][1] -1] == 1 or pos[i][1] == 0 :
                    self.downposs = False
                    break
        if self.downposs :
            self.fblock_zero()
            self.falling.move_down()
            self.fblock_update()
        else :
            self.inv_max_height()
            if self.investigate_end() :
                sys.exit(0)
            idx = random.randrange(0,4)
            self.create_blocks(idx,self.map)
            self.downposs = True
    def render_object(self, bloc) :
        pos = bloc.final_position()
        print(pos[1][0])
        for i in 4 :
            self.map[pos[i][0]][pos[i][1]] = 1

    def get_map(self) :
        return self.map

    def get_falling(self) :
        return self.falling
    def create_blocks(self, idx , map) :
        blc = block(BlockIndex[idx],map)
        self.set_failling_block(blc)
        self.downposs = True
        self.draw_falling_bloc()

    def fill_block(self, x , y) :
        self.map[x][y] = 1
    def transpose_block(self) :
        self.fblock_zero()
        self.falling.transpose()
        self.fblock_update()
        self.render_block()

    def fblock_zero(self) :
        fpos = self.falling.final_position()
        for k in range(0,4) :
            self.map[fpos[k][0]][fpos[k][1]] = 0
    def fblock_update(self) :
        fpos = self.falling.final_position()
        for k in range(0,4) :
            self.map[fpos[k][0]][fpos[k][1]] = 1
    def get_line(self) :
        return self.block_line
    def render_block(self) :
        self.block_line = ""
        for k in range( Y_VISUAL_MAX - 1 , -1 , -1) :
            for i in range( 0, X_MAX) :
                if (self.map[i][k] == 1) :
                    self.block_line += "■"
                else :
                    self.block_line += "□"
            self.block_line += '\n'
        self.master.render(self.block_line)
        if CONSOLE == 1 :
            print(self.block_line)
    def draw_falling_bloc(self) :
        poslist = self.falling.final_position()
        for i in poslist :
            self.map[i[0]][i[1]] = 1
    def fill_vertical(self, idx) :
        for i in range(0,Y_MAX) :
            self.map[idx][i] = 1

    def fill_horizen(self, idx) :
        for i in range(0,X_MAX) :
            self.map[i][idx] = 1

    def empty_vertical(self, idx) :
        for i in range(0,Y_MAX) :
            for k in range(0, X_MAX) :
                self.map[k][i] = 0

    def empty_horizen(self, idx) :
        for i in self.map[idx] :
            for k in range(0, Y_MAX) :
                i[k] = 0
    def left_move_poss(self, blc) :
        poslist = self.falling.final_position()
        inv = self.falling.get_inv_left_list()

        for i in range(0,4) :
            if poslist[i][0] == 0 :
                return False
            if inv[i] :
                if poslist[i][0] == 0 :
                    return False
                if self.map[poslist[i][0] - 1][ poslist[i][1]] :
                    return False
        return True
    def right_move_poss(self, blc) :
        poslist = self.falling.final_position()
        inv = self.falling.get_inv_right_list()
        for i in range(0,4) :
            if poslist[i][0] == X_VISUAL_MAX :
                return False
            if inv[i] :
                if poslist[i][0] == X_MAX :
                    return False
                if self.map[poslist[i][0] + 1][poslist[i][1]] :
                    return False
        return True
    def down_move_poss(self, blc) :
        poslist = self.falling.final_position()
        y = self.falling.get_y()
        inv = self.falling.get_inv_list()
        for i in range(0,4) :
            if poslist[i][1] == 0 :
                return False
            if inv[i] :
                if poslist[i][1] == 0 :
                    return False
                if self.map[poslist[i][0]][poslist[i][1] - 1] == 1:
                    return False
        return True
    def move_block_left(self) :
        if not self.left_move_poss(self.falling) :
            return
        self.fblock_zero()
        self.falling.move_left()
        self.fblock_update()
    def move_block_right(self) :
        if not self.right_move_poss(self.falling) :
            return
        self.fblock_zero()
        self.falling.move_right()
        self.fblock_update()
    def fall_down(self, blc, y) :
        self.fblock_zero()
        self.falling.set_y(y)
        self.falling.update_pos()
        self.fblock_update()
        self.render_block()
        self.inv_max_height()
        self.downposs = False
        self.arrange_after_clear()

        self.set_next_frame()
    def inv_max_height(self) :
        pos = self.falling.final_position()
        for i in pos :
            if i[1] > self.maxHeight :
                self.maxHeight = i[1]
    def move_block_bottom(self) :
        inv = self.falling.get_inv_list()
        pos = self.falling.final_position()
        mark = self.falling.get_mark()
        y_ = 0
        for k in range(mark[1] , -1 , -1) :
            for i in range(0 ,4) :
                if inv[i] :
                    k_ = k + pos[i][1] - mark[1]
                    if self.map[pos[i][0]][k_ - 1] == 1 :
                        y_ = k
                        self.fall_down(self.falling, y_)
                        return
                if k == 0 :
                        self.fall_down(self.falling, 0)
                        return
    def investigate_end(self) :
        for i in range(0, X_VISUAL_MAX) :
            if self.map[i][Y_VISUAL_MAX - 1] == 1 :
                print ("Game Ended")
                return True
        return False
    def activity(self,stop) :
        self.frame = 0
        if True:
            while True :
                if self.down_move_poss(self.falling) :
                    if self.falling.get_y() != 0 :
                        self.downposs = True
                else :
                    self.downposs = False
                self.render_block()
                time.sleep(0.009)
                self.frame += 1
                if self.frame >= 50 :
                    self.frame = 0
                    self.next_frame()
    def set_next_frame(self) :
        self.frame = 50
    def investigate_clear(self) :
        clear = [-1,0]
        for i in range(0, Y_VISUAL_MAX) :
            for k in range(0, X_VISUAL_MAX) :
                if self.map[k][i] == 0 :
                    break
                if k == X_VISUAL_MAX - 1  and self.map[k][i] == 1 :
                    clear[1] += 1
                    for y in range(0, X_VISUAL_MAX) :
                        if clear[0] == -1 :
                            clear[0] = i
                        self.map[y][i] = 0
        return clear
    def gravity(self, row, rng) :
        if row == -1 :
            return
        print (rng)
        for i in range(row , Y_VISUAL_MAX - rng) :
            for k in range(0, X_VISUAL_MAX) :
                if self.map[k][i+rng] == 1 :
                    self.map[k][i] = self.map[k][i+rng]
                    self.map[k][i + rng] = 0

    def arrange_after_clear(self) :
        clear = self.investigate_clear()
        self.gravity(clear[0],clear[1])

def possible_alloc_from_xy(blc, pmap, x , y) :
    blc.set_y(y)
    blc.set_x(x)
    pos = blc.final_position()
    inv = blc.get_inv_list()
    uphold = False
    for i in range(0,4) :
        if pos[i][0] < 0 or pos[i][0] >= X_MAX or pos[i][1] < 0 or pos[i][1] >= Y_VISUAL_MAX :
            return False
        if pmap[pos[i][0]][pos[i][1]] == 1 :
            return False
        if inv[i] :
            if pos[i][1] == 0 :
                uphold = True
            elif pmap[pos[i][0]][pos[i][1] - 1] == 1 :
                uphold = True
        if i == 3 and not uphold :
            return False
    return True

def find_all_possible_pos_by_idx(idx ,pmap , maxY):
    posAllList = list()
    name = BlockIndex[idx]
    blc = block(name,pmap)
    for t in range(0, FormCount[name]) :
        blc.set_trans(t)
        startX = MaxMinX[name][t][0]
        endX = MaxMinX[name][t][1]
        for y in range(0 , maxY + 1) :
            for x in range(startX, endX + 1) :
                if possible_alloc_from_xy(blc,pmap,x,y) :
                    elem = blc.final_position()
                    posAllList.append(elem)
    return posAllList

def find_all_possible_pos(blc, pmap ,maxY) :
    posAllList = list()
    name = blc.get_name()
    trans = blc.get_trans()
    for t in range(0, FormCount[name]) :
        blc.set_trans(t)
        startX = MaxMinX[name][t][0]
        endX = MaxMinX[name][t][1]
        for y in range(0 , maxY + 1) :
            for x in range(startX, endX + 1) :
                if possible_alloc_from_xy(blc,pmap,x,y) :
                    elem = blc.final_position()
                    posAllList.append(elem)
    return posAllList

def fall_block_straight( blc , mapp) :
    ipos = blc.get_inv_list()
    pos = blc.final_position()
    result = copy.deepcopy(pos)
    under = pos[0][1] - 1
    for y in range ( under , -1 , -1) :
        for k in range(0 , 4) :
            if ipos[k] == True :
                    if mapp[pos[k][0]][y] == 1 :
                        result[k][1] += 1
                        return update_pos_block(result)
    result[k][1] = 0
    return update_pos_block(result)
