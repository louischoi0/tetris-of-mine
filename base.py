import time
import win32api
from ctypes import Structure, c_short , windll , POINTER
import random
import copy

from tkinter import *
from tkinter import messagebox

import threading

class myWindow :
    def __init__(self, master) :
        score = Label()
        self.frame = Frame(master)
        self.frame.pack()

        self.mst = master
        self.sVar = StringVar()
        self.mainWindow = Label(self.frame,textvariable=self.sVar)
        self.mainWindow.pack()

    def render(self,str) :
        self.sVar.set(str)
        self.mst.update()


def gotoxy(x,y) :
    class COORD(Structure) :
        _fields_ = [("X",c_short) , ("Y" ,c_short)]
    windll.kernel32.SetConsoleCursorPosition(win32api.GetStdHandle(win32api.STD_OUTPUT_HANDLE), (COORD(x,y)))


X_START = 4
Y_START = 9

X_MAX = 9
Y_MAX = 13

X_VISUAL_MAX = 9
Y_VISUAL_MAX = 10

BlockIndex = [ "stick" , "cube", "mout" , "twizle" , "twizler" ]

BlockMap = {
    'stick' :  ( (0,0) , (0,1) , (0,2) , (0,3) ) ,
    'cube' :  ( (0, 0) , (1,0), (0,1) , (1,1) ) ,
    'mout' :  ( (0,0) ,(1,0) , ( 2,0) , ( 1 , 1)  , ( (-1,1) , (0,0), (1,-1), (-1 , -1) ) ),
    'twizle' : ( (0,0) ,(1,0), (1,1), (2,1) ),
    'twizler' :( (0,0) ,( -1 ,0) , (-1,1), (-2,1) )
}

TransMap = {
    'stick' : ( ( ( -2 , 2) , (-1, 1) , (0, 0) , (1 , -1) ) ,( ( 2 , -2) , ( 1, -1) , ( 0, 0 ) , ( -1, 1) )  ),
    'cube' : (
                ((0,0),(0,0),(0,0),(0,0)),
                ),
    'mout' : (
                ((1,1) ,(0,0),( -1 , -1), (1,-1)),
                ((1,-1),(0,0),(-1, 1), (-1,-1)),
                ((-1,-1),(0,0),(1,1),(-1,1)),
                ((-1,1),(0,0),(1,-1),(1,1))
              ),
    'twizle' : (
                ((1,1) , (0,0),(1,-1),(0,-2)),
                ((1,0) , (0,1),(-1,0),(-2,1))
                ),
    'twizler' : (
                    ((-1,-1),(0,0),(1,-1),(2,0)),
                    ((1,1),(0,0),(-1,1),(-2,0))
                )

}

TransPos = {
    'stick' : ( ( ( 0, -2) , (4,4) ) , ( (-2, 0) , (4,4) ) )
}

InvestigatePos = {
    'stick' : (( True, False, False, False) , (True , True, True, True)),
    'cube' : ( (True, True , False , False) ),
    'mout' : (()),
    'twizle' : ( (True, True, False, False) ),
    'twizler' : ( (True,True , False, False) )


}

InvestigateLeftPos = {
    'stick' : ((True, False, False, False), (True, True, True,True)),
    'cube' : ( (True,False,True,False)),
    'mout' : (()),
    'twizle' : (()),
    'twizler' : (())

}

InvestigateRightPos = {
    'stick' : ((False,False,False,True), (True,True,True,True)),
    'cube' : ( (False,True,False,True) )

}

FormCount = {
    'stick' : 2,
    'cube' : 1,
    'mout' : 4,
    'twizle' : 2,
    'twizler' : 2
}

def update_pos_block(blc) :
        finpos = [ [self.X + BlockMap[self.name][0][0] , self.Y + BlockMap[self.name][0][1]]
                        [self.X + BlockMap[self.name][1][0] , self.Y + BlockMap[self.name][1][1]] ,
                        [self.X + BlockMap[self.name][2][0] , self.Y + BlockMap[self.name][2][1]] ,
                        [self.X + BlockMap[self.name][3][0] , self.Y + BlockMap[self.name][3][1]] ]
        return finpos

class block(object):

    def __init__(self, name):
        self.X = X_START
        self.Y = Y_START
        self.name = name
        self.trans = 0
        self.finpos = [ [self.X + BlockMap[name][0][0] , self.Y + BlockMap[self.name][0][1]]  ,
                        [self.X + BlockMap[name][1][0] , self.Y + BlockMap[self.name][1][1]] ,
                        [self.X + BlockMap[name][2][0] , self.Y + BlockMap[self.name][2][1]] ,
                        [self.X + BlockMap[name][3][0] , self.Y + BlockMap[self.name][3][1]] ]

    def update_pos(self) :
        self.finpos = [ [self.X + BlockMap[self.name][0][0] , self.Y + BlockMap[self.name][0][1]]  ,
                        [self.X + BlockMap[self.name][1][0] , self.Y + BlockMap[self.name][1][1]] ,
                        [self.X + BlockMap[self.name][2][0] , self.Y + BlockMap[self.name][2][1]] ,
                        [self.X + BlockMap[self.name][3][0] , self.Y + BlockMap[self.name][3][1]] ]

    def move(self , Xoff , Yoff):
        self.X -= Xoff
        self.Y -= Yoff
        self.update_pos()

    def transpose(self) :
        idx = 0
        print(TransMap[self.name][self.trans])
        for i in TransMap[self.name][self.trans] :
            self.finpos[idx][0] += i[0]
            self.finpos[idx][1] += i[1]
            idx += 1

        self.trans = (self.trans + 1) % FormCount[self.name]
    def get_y(self) :
        return self.Y

    def set_y(self, y) :
        self.Y = y
        self.update_pos()

    def final_position(self) :
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
        self.map = [[0 for row in range (Y_MAX)] for row in range(X_MAX)]
        self.falling = None
        self.block_line = ''
        self.master = master

    def set_failling_block(self, bloc) :
        self.falling = bloc

    def next_frame(self) :
        self.fblock_zero()
        self.falling.move_down()
        self.fblock_update()

    def render_object(self, bloc) :
        pos = bloc.final_position()
        print(pos[1][0])
        for i in 4 :
            self.map[pos[i][0]][pos[i][1]] = 1

    def get_map(self) :
        return self.map

    def get_falling(self) :
        return self.falling

    def create_blocks(self, idx) :
        blc = block(BlockIndex[0])
        self.set_failling_block(blc)
        self.draw_falling_bloc()

    def fill_block(self, x , y) :
        self.map[x][y] = 1

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
            if inv[i] :
                if poslist[i][0] == X_MAX :
                    return False
                if self.map[poslist[i][0] + 1][ poslist[i][1]] :
                    return False
        return True

    def down_move_poss(self, blc) :
        poslist = self.falling.final_position()
        y = self.falling.get_y()
        inv = self.falling.get_inv_list()

        for i in range(0,4) :
            if inv[i] :
                print(self.map[poslist[i][0]][poslist[i][1] - 1])
                if poslist[i][1] == 0 :
                    False

                if self.map[poslist[i][0]][poslist[i][1] - 1] == 1:
                    return False
        return True

    def activity(self) :
        idx = random.randrange(0,5)
        self.create_blocks(idx)

        while True :
            if self.down_move_poss(self.falling) :
                if self.falling.get_y() != 0 :
                    self.next_frame()
                else :
                    idx = random.randrange(0,5)
                    self.create_blocks(idx)

            else :
                idx = random.randrange(0,5)
                self.create_blocks(idx)

            self.render_block()
            self.master.render(self.block_line)
            time.sleep(1)


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

class App(threading.Thread):
    def __init__(self,render):
        threading.Thread.__init__(self)
        self.render = render
        self.start()

    def get_service(self) :
        return self.mW

    def callback(self):
        self.master.quit()

    def run(self):
        self.render.activity()
