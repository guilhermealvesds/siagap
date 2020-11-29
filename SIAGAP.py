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
from tkinter.colorchooser import askcolor

import os
import tkFileDialog
import sqlite3

# banco de dados

con = sqlite3.connect('avalgen.db')
cursor = con.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS CORES_CDP (
            SIGLA CHARACTER(1)NOT NULL PRIMARY KEY,
            DESCRICAO VARCHAR(20),
            COR VARCHAR(7) NOT NULL,
            ORDENACAO CHARACTER(2) NOT NULL)""")

# declaração variáveis

v_configura_tela_inicial = 0
v_cores = 0
v_cores_cdp = 0

resolucao_tela = '640x320'
resolucao_width = 640
resolucao_height = 320

resolucao_tela_cadastro = '400x250'
resolucao_width_cadastro = 400
resolucao_height_cadastro = 250

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
	def cores_cdp():
		global v_cores_cdp
		def on_close_cdp():
			global v_cores_cdp
			v_cores_cdp = 0
		def escolhe_cor():
			color_code = askcolor(parent = t, title = "Selecionar cor")
			lblcor_v['bg'] = color_code[1]
		def apaga_mensagem():
			lblMensagem['text'] = ''
		def consiste():
			v_sigla = etrSigla.get()
			v_ordenacao = etrOrdenacao.get()
			lblMensagem['fg'] = 'red'
			
			if v_sigla == '':				
				lblMensagem['text'] = '*PREENCHA A SIGLA'
				return 0
			
			if len(v_sigla) > 1:							
				lblMensagem['text'] = '*A SIGLA DEVE TER APENAS UM CARACTERE'
				return 0
				
			dbRollNo = ""
			Select="select SIGLA from CORES_CDP where SIGLA='%s'" %(v_sigla)
			cursor.execute(Select)
			result = cursor.fetchall()
			for i in result:
				dbRollNo=i[0]
			if(v_sigla == dbRollNo):
				lblMensagem['text'] = '*REGISTRO JÁ EXISTE'
				return 0
				
			if v_ordenacao == '':
				lblMensagem['text'] = '*PREENCHA A ORDENACAO'
				return 0
				
			return 1
		def incluir():
			r = consiste()
			if bool(r):
				Insert=''' Insert into CORES_CDP(SIGLA, DESCRICAO, COR, ORDENACAO) values(?,?,?,?) '''
				Sigla = etrSigla.get()
				Descricao = etrDescricao.get()
				Cor = lblcor_v['bg']
				Ordenacao = etrOrdenacao.get()
				Value=(Sigla, Descricao, Cor, Ordenacao)
				cursor.execute(Insert, Value)
				con.commit()
				lblMensagem['fg'] = '#2D8C2B'
				lblMensagem['text'] = '*REGISTRO INCLUÍDO COM SUCESSO'
				etrSigla.delete(0, tk.END)
				etrDescricao.delete(0, tk.END)
				lblcor_v['bg'] = 'white'
				etrOrdenacao.delete(0, tk.END)
				t.after(5000, apaga_mensagem)								
		if v_cores_cdp == 0:
			t = tk.Toplevel()
			t.geometry(resolucao_tela_cadastro)
			t.title('Cores - CDP')			
			content = tk.Frame(t)
			messageBar = tk.Frame(t, height=30)
			footer = tk.Frame(t, height=30)			
			content.pack(fill='both')
			messageBar.pack(fill='both')
			footer.pack(fill='both', side='bottom')
			lblsigla = Label(content, text = "Sigla:", font=("Verdana", 8, 'bold'))
			lblsigla.grid(column=0, row=0, ipadx=5, pady=5, sticky=tk.W+tk.N)
			lbldescricao = tk.Label(content, text = "Descrição:", font=("Verdana", 8, 'bold'))
			lbldescricao.grid(column=0, row=1, ipadx=5, pady=5, sticky=tk.W+tk.S)
			lblcor = tk.Label(content, text = "Cor:", font=("Verdana", 8, 'bold'))
			lblcor.grid(column=0, row=2, ipadx=5, pady=5, sticky=tk.W+tk.S)
			lblOrdenacao = tk.Label(content, text = "Ordenação:", font=("Verdana", 8, 'bold'))
			lblOrdenacao.grid(column=0, row=3, ipadx=5, pady=5, sticky=tk.W+tk.S)
			etrSigla = tk.Entry(content, width=20)
			etrSigla.grid(column=1, row=0, padx=10, pady=5, sticky=tk.N)
			etrDescricao = tk.Entry(content, width=20)
			etrDescricao.grid(column=1, row=1, padx=10, pady=5, sticky=tk.S)
			lblcor_v = tk.Label(content, bg="white", width=17)
			lblcor_v.grid(column=1, row=2)
			etrOrdenacao = tk.Entry(content, width=20)
			etrOrdenacao.grid(column=1, row=3, padx=10, pady=5, sticky=tk.S)
			btncor = Button(content, image=v_cores_cdp_icon_img_1, relief=FLAT, command=escolhe_cor)
			btncor.grid(column=2, row=2, padx=5, pady=5, sticky=tk.S)
			lblMensagem = tk.Label(messageBar, fg="red", text = "", font=("Verdana", 8, 'bold'))
			lblMensagem.grid(column=0, row=0, ipadx=5, pady=5, sticky=tk.W+tk.S)
			botao1 = Button(footer, image=v_cores_cdp_icon_img_2, relief=FLAT, command=incluir)
			botao1.grid(column=0, row=8)	
			t.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_cdp, t.destroy))
			t.iconbitmap(default='transparent.ico')
			windowWidth, windowHeight = resolucao_width_cadastro, resolucao_height_cadastro
			positionRight = int(t.winfo_screenwidth()/2 - windowWidth/2)
			positionDown = int(t.winfo_screenheight()/2 - windowHeight/2)
			t.geometry("+{}+{}".format(positionRight, positionDown))
			t.attributes("-toolwindow", True)
			t.attributes("-topmost", True)
			v_cores_cdp = 1
	if v_cores == 0:
		t = tk.Toplevel()
		t.geometry(resolucao_tela)
		t.title('Cores - Parametrização')
		Button(t, text='Cores - CDP', command=cores_cdp, width = 60).pack(padx=7, pady=7)
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
v_cores_cdp_icon_1 = Image.open("COLOR_16x16.png")
v_cores_cdp_icon_2 = Image.open("ADD_16x16.png")
 
# Cria Imagens
imagem1 = ImageTk.PhotoImage(icone1)
imagem2 = ImageTk.PhotoImage(icone2)
imagem3 = ImageTk.PhotoImage(icone3)
v_cores_cdp_icon_img_1 = ImageTk.PhotoImage(v_cores_cdp_icon_1)
v_cores_cdp_icon_img_2 = ImageTk.PhotoImage(v_cores_cdp_icon_2)
 
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
