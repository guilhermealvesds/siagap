try:                        # In order to be able to import tkinter for
    import tkinter as tk    # either in python 2 or in python 3
except:
    import Tkinter as tk
from PIL import Image, ImageTk
import os

def principal():
	dirAnterior = 'C:\\Python27\\'
	os.system(dirAnterior + "python " + os.getcwd() + "\\" + "main.py")			

root = tk.Tk()  # A root window for displaying objects
root.overrideredirect(1)

# open image
imageHead = Image.open('splash.png')

#imageHead.paste(imageHand, (0, 0, x, y), imageHand)
# Convert the Image object into a TkPhoto object
tkimage = ImageTk.PhotoImage(imageHead)

label = tk.Label(root, image=tkimage)
label.pack()

windowWidth, windowHeight = imageHead.size

positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)

root.geometry("+{}+{}".format(positionRight, positionDown))
root.after(5000, root.destroy)
root.after(4000, principal)
root.mainloop() 
