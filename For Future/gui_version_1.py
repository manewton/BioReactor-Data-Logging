from Tkinter import *


# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):

        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        #reference to the master widget, which is the tk window
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a button instance
        addins1Button = Button(self, text="add instrument 1 data",command=self.client_exit)

        # placing the button on my window
        addins1Button.place(x=10, y=10)

        addins2Button = Button(self, text="add instrument 2 data",command=self.client_exit)
        addins2Button.place(x=10, y=50)

        plotButton = Button(self, text="plot data",command=self.client_exit)
        plotButton.place(x=10, y=90)

    def client_exit(self):
        exit()

# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

root.geometry("400x300")

#creation of an instance
app = Window(root)

#mainloop
root.mainloop()
