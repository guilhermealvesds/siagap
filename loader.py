try:                        # In order to be able to import tkinter for
    import tkinter as tk    # either in python 2 or in python 3
except:
    import Tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()  # A root window for displaying objects
# open image
imageHead = Image.open('splash.png')

#imageHead.paste(imageHand, (0, 0, x, y), imageHand)
# Convert the Image object into a TkPhoto object
tkimage = ImageTk.PhotoImage(imageHead)

label = tk.Label(root, image=tkimage)
label.pack()
root.mainloop() 
