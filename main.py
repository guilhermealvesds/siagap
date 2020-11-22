# coding: latin1
# Simple enough, just import everything from tkinter.
try:                        
    import tkinter as tk   
except:
    import Tkinter as tk

from PIL import Image, ImageTk

import os

import tkFileDialog

# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(tk.Frame):
    # Variável da classe Window 
    counter = 0
    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        tk.Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()
        
        self.executa_tela_inicial()
        # parameters that you want to send through the Frame class.
        #tk.Frame.__init__(self, master)
        #reference to the master widget, which is the tk window
        #self.master = master
        #with that, we want to then run init_window, which doesn't yet exist
        #self.init_window() 

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("SIAGAP - Sistema Integrado de Avaliação Genética e Acasalamento Produtivo")

        # allowing the widget to take the full space of the root window
        self.pack(fill=tk.BOTH, expand=1)

        # creating a menu instance
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = tk.Menu(menu, tearoff=0)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Tela Inicial", command=self.configura_tela_inicial)
        file.add_command(label="Sair", command=self.client_exit)

        #added "file" to our menu
        menu.add_cascade(label="Sistema", menu=file)        

    def client_exit(self):
        exit()
        
    def configura_tela_inicial(self):
		t = tk.Toplevel(self)
		t.geometry("500x500")
		def carregaPlanoDeFundo():
			nomeArquivo = tkFileDialog.askopenfilename(parent = t, initialdir = "/",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
			lbDirplanodefundo.config(text = nomeArquivo)
		def carregaLogo():
			nomeLogo = tkFileDialog.askopenfilename(parent = t, initialdir = "/",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
			lbDirLogo.config(text = nomeLogo)
		self.counter += 1	
		t.wm_title("Window #%s" % self.counter)		
		t.resizable(width=tk.FALSE, height=tk.FALSE)
		frame1 = tk.Frame(t)
		lbplanodefundo = tk.Label(frame1, text="Plano de fundo", fg="black", font="Verdana").grid(row=0)
		botaoCarregaPlanoDeFundo = tk.Button(frame1, text='Upload', font=('Verdana','10'), fg='Black', command=carregaPlanoDeFundo)
		botaoCarregaPlanoDeFundo.grid(row=0, column = 1)
		lbDirplanodefundo = tk.Label(frame1, text='', fg="black", font="Verdana")		
		lbDirplanodefundo.grid(row=0, column=2)
		lblogo = tk.Label(frame1, text="Logomarca", fg="black", font="Verdana").grid(row=1)
		botaoCarregaLogo = tk.Button(frame1, text='Upload', font=('Verdana','10'), fg='Black', command=carregaLogo).grid(row=1, column=1)
		lbDirLogo = tk.Label(frame1, text='', fg="black", font="Verdana")
		lbDirLogo.grid(row=1, column=2)
		#botaoSalvar = tk.Button(t, text='SALVAR', font=('Verdana','12'), fg='Black', command=salvarImagens).pack(side=tk.BOTTOM, pady=12)
		frame1.pack(side=tk.LEFT, expand=tk.NO)
		windowWidth = 500
		windowHeight = 500
		positionRight = int(t.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(t.winfo_screenheight()/2 - windowHeight/2)
		t.geometry("+{}+{}".format(positionRight, positionDown))
		t.mainloop()

    def executa_tela_inicial(self):
		self.counter += 1
		t = tk.Toplevel(self)
		t.wm_title("Window #%s" % self.counter)
		t.overrideredirect(1)
		imageHead = Image.open(os.getcwd() + '\\' + 'splash.png')
		tkimage = ImageTk.PhotoImage(imageHead)
		label = tk.Label(t, image=tkimage)
		label.pack()
		windowWidth, windowHeight = imageHead.size
		positionRight = int(t.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(t.winfo_screenheight()/2 - windowHeight/2)
		t.geometry("+{}+{}".format(positionRight, positionDown))
		t.attributes("-topmost", True)
		t.after(5000, t.destroy)
		t.mainloop()

# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = tk.Tk()

root.attributes('-fullscreen',True)

#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()
