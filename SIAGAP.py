#!/usr/bin/env python
# -*- coding: latin-1 -*-
# main.py
 
# importa modulos
try:                        
    import tkinter as tk   
except:
    import Tkinter as tk

from PIL     import Image, ImageTk
from Tkinter import Tk,    Frame
from Tkinter import Label, Button, LEFT, TOP, X, FLAT, RAISED, SUNKEN

import os
import tkFileDialog

# define e implementa as funções
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
	def salvarImagens():
		if lbDirplanodefundo.cget("text") <> '' and lbDirLogo.cget("text") <> '':
			background = Image.open(lbDirplanodefundo.cget("text"), 'r')
			foreground = Image.open(lbDirLogo.cget("text"), 'r')
			os.remove(os.getcwd() + '\\' + 'background.png')
			os.remove(os.getcwd() + '\\' + 'foreground.png')
			background.save(os.getcwd() + '\\' + 'background.png', format="png")
			foreground.save(os.getcwd() + '\\' + 'foreground.png', format="png")
			foreground = os.getcwd() + '\\' + 'foreground.png'
			foreground = Image.open(foreground, 'r')
			background = os.getcwd() + '\\' + 'background.png'
			background = Image.open(background, 'r')
			x, y = background.size
			z, a = foreground.size
			text_img = Image.new('RGBA', (x,y), (0, 0, 0, 0))
			text_img.paste(background, (0,0))
			try:
				text_img.paste(foreground, ((x/2)-(z/2),(y/2)-(a/2)), mask=foreground)
			except:
				text_img.paste(foreground, ((x/2)-(z/2),(y/2)-(a/2)))
			text_img.save("splash.png", format="png")
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
		botaoSalvar = tk.Button(t, text='SALVAR', font=('Verdana','12'), fg='Black', command=salvarImagens).pack(side=tk.BOTTOM, pady=12)
		frame1.pack(side=tk.LEFT, expand=tk.NO)
		windowWidth = 500
		windowHeight = 500
		positionRight = int(t.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(t.winfo_screenheight()/2 - windowHeight/2)
		t.geometry("+{}+{}".format(positionRight, positionDown))
		t.mainloop()		 

def executa_tela_inicial():
	t = Tk()
	t.wm_title("Window")
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

# splash screen
executa_tela_inicial()
  
# Cria formulario
formulario = Tk()
formulario.title = "Desenvolvimento Aberto"      
      
# Cria componentes    
ferramenta = Frame(height=130, bd=1, relief=RAISED)
 
# Carrega Ícones    
icone1 = Image.open("TOOLS_64x64.png")
icone2 = Image.open("EXIT_64x64.png")
 
# Cria Imagens
imagem1 = ImageTk.PhotoImage(icone1)
imagem2 = ImageTk.PhotoImage(icone2)
 
# Cria botões
botao1 = Button(ferramenta, image=imagem1,relief=FLAT)

def on_enter_botao1(e):
	statusbarmenu['text'] = 'CONFIGURAÇÕES'

def on_leave_botao1(e):
	statusbarmenu['text'] = ''

botao2 = Button(ferramenta, image=imagem2,relief=FLAT)

def on_enter_botao2(e):
	statusbarmenu['text'] = '                      SAIR'

def on_leave_botao2(e):
	statusbarmenu['text'] = ''

botao1.bind("<Enter>", on_enter_botao1)
botao1.bind("<Leave>", on_leave_botao1)

botao2.bind("<Enter>", on_enter_botao2)
botao2.bind("<Leave>", on_leave_botao2)

# Posiciona componentes
botao1.pack(side=LEFT, padx=2,pady=2)
botao2.pack(side=LEFT, padx=2,pady=2)
ferramenta.pack(side=TOP, fill=X)

# barra de status no rodapé
statusbarmenu = tk.Label(formulario, text="", bd=0, font=("Verdana", 8, 'bold'), relief=tk.SUNKEN, anchor=tk.W)
statusbarmenu.pack(side=tk.TOP, fill=tk.X)

statusbarrodape = tk.Label(formulario, text="SIAGAP - Sistema Integrado de Avaliação Genética e Agropecuária", bd=1, font=("Verdana", 10), relief=tk.SUNKEN, anchor=tk.W)
statusbarrodape.pack(side=tk.BOTTOM, fill=tk.X)
 
# Loop do tcl
formulario.attributes("-topmost", True)
formulario.attributes('-fullscreen',  True)
formulario.mainloop()
