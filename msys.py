import base
import win32api
from ctypes import Structure, c_short , windll , POINTER

from tkinter import *
from tkinter import messagebox

import sys,traceback
import threading

def keyPressed(event) :
    print(event.char)

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
        if base.EXIT :
            return
        self.sVar.set(str)
        self.mst.update()

    def set_callback(self,call) :
        self.frame.bind('<Key>', call)
        self.frame.focus_set()

def gotoxy(x,y) :
    class COORD(Structure) :
        _fields_ = [("X",c_short) , ("Y" ,c_short)]
    windll.kernel32.SetConsoleCursorPosition(win32api.GetStdHandle(win32api.STD_OUTPUT_HANDLE), (COORD(x,y)))
class App(threading.Thread):
    def __init__(self,render):
        threading.Thread.__init__(self)
        self.render = render
        self.start()
        self._stop = threading.Event()
    def get_service(self) :
        return self.mW
    def callback(self):
        self.master.quit()
    def run(self):
        self.render.activity(self._stop)
    def stop(self) :
        self._stop.set()
if __name__ == '__main__' :
    master = Tk()
    master.title("Tetris")
    master.geometry('400x630')

    mW = myWindow(master)
    renderService = base.Render(mW)
    app = App(renderService)

    def quit_callback() :
        sys.exit(0)

    master.protocol("WM_DELETE_WINDOW", quit_callback)

    def key_pressed(event) :
        if event.char == "l" :
            renderService.move_block_right()
        if event.char == "j" :
            renderService.move_block_left()
        if event.char == "m" :
            renderService.move_block_bottom()
        if event.char == 't' :
            renderService.transpose_block()

    mW.set_callback(key_pressed)
    master.mainloop()
