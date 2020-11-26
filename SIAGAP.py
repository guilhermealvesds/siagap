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

# declaração variáveis

v_configura_tela_inicial = 0
v_cores = 0

resolucao_tela = '640x320'
resolucao_width = 640
resolucao_height = 320

# define e implementa as funções
def client_exit():
	exit()

def combine_funcs(*funcs):
	def combined_func(*args, **kwargs):
		for f in funcs:
			f(*args, **kwargs)
	return combined_func	

def cores():
	global v_cores
	def on_close():
		global v_cores
		v_cores = 0			
	if v_cores == 0:
		t = tk.Toplevel()
		t.geometry(resolucao_tela)
		t.title('Cores - Parametrização')
		Button(t, text='Cores - CDP', command=combine_funcs(on_close, t.destroy), width = 60).pack(padx=7, pady=7)
		Button(t, text='Cores - Avaliação Fenotípica', command=combine_funcs(on_close, t.destroy), width = 60).pack(padx=7, pady=7)
		Button(t, text='Cores - Produtividade', command=combine_funcs(on_close, t.destroy), width = 60).pack(padx=7, pady=7)
		Button(t, text='Cores - Avaliação Genética', command=combine_funcs(on_close, t.destroy), width = 60).pack(padx=7, pady=7)
		Button(t, text='Cores - Avaliação Visual - Bezerro', command=combine_funcs(on_close, t.destroy), width = 60).pack(padx=7, pady=7)
		Button(t, text='Cores - Acasalamentos', command=combine_funcs(on_close, t.destroy), width = 60).pack(padx=7, pady=7)
		Button(t, text='Cores - Cabeçalhos - Relatórios', command=combine_funcs(on_close, t.destroy), width = 60).pack(padx=7, pady=7)
		Button(t, text='FECHAR', command=combine_funcs(on_close, t.destroy)).pack(padx=7, pady=7)
		t.protocol("WM_DELETE_WINDOW", combine_funcs(on_close, t.destroy))
		t.iconbitmap(default='transparent.ico')
		windowWidth, windowHeight = resolucao_width, resolucao_height
		positionRight = int(t.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(t.winfo_screenheight()/2 - windowHeight/2)
		t.geometry("+{}+{}".format(positionRight, positionDown))
		t.attributes("-toolwindow", True)
		formulario.attributes("-topmost", False)
		t.attributes("-topmost", True)
		v_cores = 1
		
def configura_tela_inicial():
	global v_configura_tela_inicial
	def on_close():
		global v_configura_tela_inicial
		v_configura_tela_inicial = 0
	if v_configura_tela_inicial == 0:
		t = tk.Toplevel()
		t.geometry(resolucao_tela)
		t.title('Configurações do Sistema')
		Button(t, text='FECHAR', command=combine_funcs(on_close, t.destroy)).pack()
		t.protocol("WM_DELETE_WINDOW", combine_funcs(on_close, t.destroy))
		t.iconbitmap(default='transparent.ico')
		windowWidth, windowHeight = resolucao_width, resolucao_height
		positionRight = int(t.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(t.winfo_screenheight()/2 - windowHeight/2)
		t.geometry("+{}+{}".format(positionRight, positionDown))
		t.attributes("-toolwindow", True)
		formulario.attributes("-topmost", False)
		t.attributes("-topmost", True)
		v_configura_tela_inicial = 1					 

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
    
# Cria componentes    
ferramenta = Frame(height=130, bd=1, relief=RAISED)
 
# Carrega Ícones    
icone1 = Image.open("COR_64x64.png")
icone2 = Image.open("TOOLS_64x64.png")
icone3 = Image.open("EXIT_64x64.png")
 
# Cria Imagens
imagem1 = ImageTk.PhotoImage(icone1)
imagem2 = ImageTk.PhotoImage(icone2)
imagem3 = ImageTk.PhotoImage(icone3)
 
# Cria botões
botao1 = Button(ferramenta, image=imagem1,relief=FLAT, command=cores)

def on_enter_botao1(e):
	statusbarmenu['text'] = 'CORES'

def on_leave_botao1(e):
	statusbarmenu['text'] = ''

botao2 = Button(ferramenta, image=imagem2,relief=FLAT, command=configura_tela_inicial)

def on_enter_botao2(e):
	statusbarmenu['text'] = '                  CONFIGURAÇÕES'

def on_leave_botao2(e):
	statusbarmenu['text'] = ''

botao3 = Button(ferramenta, image=imagem3,relief=FLAT, command=client_exit)

def on_enter_botao3(e):
	statusbarmenu['text'] = '                                         SAIR'

def on_leave_botao3(e):
	statusbarmenu['text'] = ''

botao1.bind("<Enter>", on_enter_botao1)
botao1.bind("<Leave>", on_leave_botao1)

botao2.bind("<Enter>", on_enter_botao2)
botao2.bind("<Leave>", on_leave_botao2)

botao3.bind("<Enter>", on_enter_botao3)
botao3.bind("<Leave>", on_leave_botao3)

# Posiciona componentes
botao1.pack(side=LEFT, padx=2,pady=2)
botao2.pack(side=LEFT, padx=2,pady=2)
botao3.pack(side=LEFT, padx=2,pady=2)
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
