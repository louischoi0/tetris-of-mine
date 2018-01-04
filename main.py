import base
if __name__ == '__main__' :
    master = base.Tk()
    master.title("Tetris")
    master.geometry('400x630')

    mW = base.myWindow(master)
    def quit_callback() :
        master.quit()
    master.protocol("WM_DELETE_WINDOW", quit_callback)

    renderService = base.Render(mW)
    app = base.App(renderService)

    master.mainloop()
