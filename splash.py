try:                       
    import tkinter as tk   
except:
    import Tkinter as tk
import Tkinter, Tkconstants, tkFileDialog

root = tk.Tk()
root.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
print (root.filename)
