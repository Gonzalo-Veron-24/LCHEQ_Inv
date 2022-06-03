from mainFrame_LCHEQ import MainFrame
from tkinter import Tk

def main():
    root = Tk()
    root.wm_title("LCHEQ 1.1")
    root.resizable(0,0)
    app = MainFrame(root)
    app.mainloop()

if __name__=='__main__':
    main()