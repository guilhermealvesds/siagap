import os
from PIL import Image

filename = os.getcwd() + '\\' + 'foreground.png'
ironman = Image.open(filename, 'r')
filename1 = os.getcwd() + '\\' + 'background.png'
bg = Image.open(filename1, 'r')
x, y = bg.size
z, a = ironman.size
text_img = Image.new('RGBA', (x,y), (0, 0, 0, 0))
text_img.paste(bg, (0,0))

try:
	text_img.paste(ironman, ((x/2)-(z/2),(y/2)-(a/2)), mask=ironman)
except:
	text_img.paste(ironman, ((x/2)-(z/2),(y/2)-(a/2)))
	
text_img.save("splash.png", format="png")
