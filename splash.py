import os
from PIL import Image

try:                       
    import tkinter as tk   
except:
    import Tkinter as tk
import Tkinter, tkFileDialog

nomeArquivo = ''

def carregaPlanodeFundo():
	nomeArquivo = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
	lbDirplanodefundo.config(text = nomeArquivo)

def carregaLogo():
	nomeArquivo = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
	lbDirLogo.config(text = nomeArquivo)

def salvarImagens():
	if lbDirplanodefundo.cget("text") <> '' and lbDirLogo.cget("text") <> '':
		#dirAnterior = os.path.normpath(os.getcwd() + os.sep + os.pardir)
		background = Image.open(lbDirplanodefundo.cget("text"), 'r')
		foreground = Image.open(lbDirLogo.cget("text"), 'r')
		os.remove(os.getcwd() + '\\' + 'background.png')
		os.remove(os.getcwd() + '\\' + 'foreground.png')
		background.save(os.getcwd() + '\\' + 'background.png', format="png")
		foreground.save(os.getcwd() + '\\' + 'foreground.png', format="png")
		dirAnterior = 'C:\\Python27\\'
		os.system(dirAnterior + "python " + os.getcwd() + "\\" + "alphacomposite.py")	

root = tk.Tk()
root.resizable(width=tk.FALSE, height=tk.FALSE)
root.geometry('{}x{}'.format(700, 350))

frame1 = tk.Frame(root)

lbplanodefundo = tk.Label(frame1, text="Plano de fundo", fg="black", font="Verdana").grid(row=0)
botaoCarregaPlanoDeFundo = tk.Button(frame1, text='Upload', font=('Verdana','10'), fg='Black', command=carregaPlanodeFundo).grid(row=0, column = 1)
lbDirplanodefundo = tk.Label(frame1, text=nomeArquivo, fg="black", font="Verdana")
lbDirplanodefundo.grid(row=0, column=2)

lblogo = tk.Label(frame1, text="Logomarca", fg="black", font="Verdana").grid(row=1)
botaoCarregaLogo = tk.Button(frame1, text='Upload', font=('Verdana','10'), fg='Black', command=carregaLogo).grid(row=1, column=1)
lbDirLogo = tk.Label(frame1, text=nomeArquivo, fg="black", font="Verdana")
lbDirLogo.grid(row=1, column=2)

botaoSalvar = tk.Button(root, text='SALVAR', font=('Verdana','12'), fg='Black', command=salvarImagens).pack(side=tk.BOTTOM, pady=12)

frame1.pack(side=tk.LEFT, expand=tk.NO)

root.mainloop()
