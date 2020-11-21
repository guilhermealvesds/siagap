# coding: latin1
# Simple enough, just import everything from tkinter.
from tkinter import *
import os

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
        self.master.title("SIAGAP - Sistema Integrado de Avaliação Genética e Acasalamento Produtivo")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu, tearoff=0)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Tela Inicial", command=self.tela_inicial)
        file.add_command(label="Sair", command=self.client_exit)

        #added "file" to our menu
        menu.add_cascade(label="Sistema", menu=file)

    def client_exit(self):
        exit()
        
    def tela_inicial(self):
		dirAnterior = 'C:\\Python27\\'
		os.system(dirAnterior + "python " + os.getcwd() + "\\" + "splash.py")

        
# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

root.attributes('-fullscreen',True)

#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()
