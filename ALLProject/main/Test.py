from tkinter import *

class app:
    def __init__(self, master):
        self.master = master
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        self.master.title("DriveEase")
        self.master.geometry("%dx%d" % (width, height))
        self.master.state("zoomed")

    #def login(self):


root = Tk()
app(root)
root.mainloop()