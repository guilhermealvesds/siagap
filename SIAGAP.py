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
from tkinter import ttk
from tkinter import messagebox

import os
import tkFileDialog
import sqlite3
import xlwt

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
v_cores_cdp_modo = 'INCLUSAO'

resolucao_tela = '640x320'
resolucao_width = 640
resolucao_height = 320

resolucao_tela_cadastro = '400x250'
resolucao_width_cadastro = 400
resolucao_height_cadastro = 250

resolucao_tela_mensagem = '600x300'
resolucao_width_mensagem = 600
resolucao_height_mesagem = 300

# define e implementa as funções
def client_exit():
	exit()

def combine_funcs(*funcs):
	def combined_func(*args, **kwargs):
		for f in funcs:
			f(*args, **kwargs)
	return combined_func
	
def msgSimNao():
	a = tk.toplevel
	a.grab_set()	

def cores():
	global v_cores
	def on_close():
		global v_cores
		v_cores = 0
	def cores_cdp():
		selecionado = {
		"sigla": "",
		"descrição": "",
		"cor": "",
		"ordenação": ""
			}	
		def seleciona(event):
			global selecionado
			curItem = treev.focus()
			selecionado = treev.item(curItem)['values']
		def refresh_consulta():
			query = "select SIGLA, DESCRICAO, COR, ORDENACAO from CORES_CDP"
			cursor.execute(query)
			resultado = cursor.fetchall()
			sigla = ""
			descricao = ""
			cor = ""
			ordenacao = ""
			
			for i in resultado:
				sigla = i[0]
				descricao = i[1]
				cor = i[2]
				ordenacao = i[3]
				treev.tag_configure(cor, background=cor)
				treev.insert("", "end", text = sigla, values=(sigla, descricao, cor, ordenacao), tags = [cor])
		def novo():
			global selecionado
			global v_cores_cdp_modo
			def escolhe_cor():
				color_code = askcolor(parent = t, title = "Selecionar cor")
				lblcor_v['bg'] = color_code[1]
			def consiste():
				global v_cores_cdp_modo
												
				v_sigla = etrSigla.get()
				v_ordenacao = etrOrdenacao.get()
				lblMensagem['fg'] = 'red'
				
				if v_cores_cdp_modo == 'INCLUSAO':
					if v_sigla == '':
						lblMensagem['text'] = '*PREENCHA A SIGLA'
						t.after(5000, apaga_mensagem)
						return 0						
					if len(v_sigla) > 1:
						lblMensagem['text'] = '*A SIGLA DEVE TER APENAS UM CARACTERE'
						t.after(5000, apaga_mensagem)
						return 0
					
					dbRollNo = ""
					Select="select SIGLA from CORES_CDP where SIGLA='%s'" %(v_sigla)
					cursor.execute(Select)
					result = cursor.fetchall()
					for i in result:
						dbRollNo=i[0]
					if(v_sigla == dbRollNo):
						lblMensagem['text'] = '*REGISTRO JÁ EXISTE'
						t.after(5000, apaga_mensagem)
						return 0
				
				if v_ordenacao == '':
					lblMensagem['text'] = '*PREENCHA A ORDENACAO'
					t.after(5000, apaga_mensagem)
					return 0
					
				return 1
				
			def insere():
				global v_cores_cdp_modo			
				
				r = consiste()
				
				if bool(r):
					etrSigla['state'] = 'normal'
					
					if v_cores_cdp_modo == 'INCLUSAO':
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
						etrSigla.focus()
						t.after(4000, apaga_mensagem)
					if v_cores_cdp_modo == 'EDICAO':
						sigla = etrSigla.get()
						descricao = etrDescricao.get()
						cor = lblcor_v['bg']
						ordenacao = etrOrdenacao.get()
						Update = "update CORES_CDP set SIGLA='%s', DESCRICAO='%s', COR='%s', ORDENACAO='%s' where sigla='%s'" %(sigla, descricao, cor, ordenacao, sigla)
						cursor.execute(Update)
						con.commit()
						lblMensagem['fg'] = '#2D8C2B'
						lblMensagem['text'] = '*REGISTRO ATUALIZADO COM SUCESSO'
						etrSigla.delete(0, tk.END)
						etrDescricao.delete(0, tk.END)
						lblcor_v['bg'] = 'white'
						etrOrdenacao.delete(0, tk.END)
						etrSigla.focus()
						t.after(4000, apaga_mensagem)
						v_cores_cdp_modo = 'INCLUSAO'
			def modificaModoCadastro(value):
				global v_cores_cdp_modo
				v_cores_cdp_modo = value
			def apaga_mensagem():
				lblMensagem['text'] = ''
			def on_close_novo():
				treev.delete(*treev.get_children())
				refresh_consulta()
			def limpa():
				global v_cores_cdp_modo
				
				etrSigla['state'] = 'normal'
				v_cores_cdp_modo = 'INCLUSAO'
				etrSigla.delete(0, tk.END)
				etrDescricao.delete(0, tk.END)
				lblcor_v['bg'] = '#FFFFFF'
				etrOrdenacao.delete(0, tk.END)
				etrSigla.focus()
			def exclui():
				if v_cores_cdp_modo == 'EDICAO':
					MsgBox = tk.messagebox.askquestion ('Excluir Cor','Deseja excluir esse registro?',icon = 'warning', parent = t)
					if MsgBox == 'yes':
						etrSigla['state'] = 'normal'
						sigla = etrSigla.get()
						Delete = "delete from CORES_CDP where SIGLA='%s'" %(sigla)
						cursor.execute(Delete)
						con.commit()
						limpa()
						lblMensagem['fg'] = '#2D8C2B'
						lblMensagem['text'] = '*REGISTRO EXCLUÍDO COM SUCESSO'
						t.after(4000, apaga_mensagem)
			def iniciaEdicao():
				etrSigla['state'] = 'normal'
				etrSigla.delete(0, tk.END)
				etrSigla.insert(0, selecionado[0])
				etrSigla['state'] = 'disabled'
				etrDescricao.delete(0, tk.END)
				etrDescricao.insert(0, selecionado[1])
				lblcor_v['bg'] = selecionado[2]
				etrOrdenacao.delete(0, tk.END)
				etrOrdenacao.insert(0, selecionado[3])
			def to_uppercaseSigla(*args):
				varEtrSigla.set(varEtrSigla.get().upper())
			def to_uppercaseDescricao(*args):
				varEtrDescricao.set(varEtrDescricao.get().upper())
			def to_uppercaseOrdenacao(*args):
				varEtrOrdenacao.set(varEtrOrdenacao.get().upper())
			def on_enter_botaoIncluir(e):
				statusbarrodape['text'] = 'SALVAR'
			def on_leave_botaoIncluir(e):
				statusbarrodape['text'] = ''
			def on_enter_botaoLimpar(e):
				statusbarrodape['text'] = '        LIMPAR'
			def on_leave_botaoLimpar(e):
				statusbarrodape['text'] = ''
			def on_enter_botaoApagar(e):
				statusbarrodape['text'] = '                EXCLUIR'
			def on_leave_botaoApagar(e):
				statusbarrodape['text'] = ''
			t = tk.Toplevel()
			t.grab_set()
			t.geometry(resolucao_tela_cadastro)
			t.title('Cores - CDP')
			content = tk.Frame(t)
			messageBar = tk.Frame(t, height=30)
			footer = tk.Frame(t, height=30)
			status = tk.Frame(t, height=30)
			content.pack(fill='both')
			messageBar.pack(fill='both')
			footer.pack(fill='both', side='bottom')
			status.pack(fill='both', side = 'bottom')
			lblsigla = Label(content, text = "Sigla:", font=("Verdana", 8, 'bold'))
			lblsigla.grid(column=0, row=0, ipadx=5, pady=5, sticky=tk.W+tk.N)
			lbldescricao = tk.Label(content, text = "Descrição:", font=("Verdana", 8, 'bold'))
			lbldescricao.grid(column=0, row=1, ipadx=5, pady=5, sticky=tk.W+tk.S)
			lblcor = tk.Label(content, text = "Cor:", font=("Verdana", 8, 'bold'))
			lblcor.grid(column=0, row=2, ipadx=5, pady=5, sticky=tk.W+tk.S)
			lblOrdenacao = tk.Label(content, text = "Ordenação:", font=("Verdana", 8, 'bold'))
			lblOrdenacao.grid(column=0, row=3, ipadx=5, pady=5, sticky=tk.W+tk.S)
			
			varEtrSigla = tk.StringVar()		
			etrSigla = tk.Entry(content, font = "Verdana 12", width=20, textvariable=varEtrSigla)
			etrSigla.grid(column=1, row=0, padx=10, pady=5, sticky=tk.N)			
			try:
				varEtrSigla.trace_add('write', to_uppercaseSigla)
			except AttributeError:
				varEtrSigla.trace('w', to_uppercaseSigla)
			
			varEtrDescricao = tk.StringVar()
			etrDescricao = tk.Entry(content, font = "Verdana 12", width=20, textvariable=varEtrDescricao)
			etrDescricao.grid(column=1, row=1, padx=10, pady=5, sticky=tk.S)
			try:
				varEtrDescricao.trace_add('write', to_uppercaseDescricao)
			except AttributeError:
				varEtrDescricao.trace('w', to_uppercaseDescricao)			
			
			lblcor_v = tk.Label(content, bg="white", width=28)
			lblcor_v.grid(column=1, row=2)
			
			varEtrOrdenacao = tk.StringVar()
			etrOrdenacao = tk.Entry(content, font = "Verdana 12", width=20, textvariable=varEtrOrdenacao)
			etrOrdenacao.grid(column=1, row=3, padx=10, pady=5, sticky=tk.S)
			try:
				varEtrOrdenacao.trace_add('write', to_uppercaseOrdenacao)
			except AttributeError:
				varEtrOrdenacao.trace('w', to_uppercaseOrdenacao)
			
			btncor = Button(content, image=v_cores_cdp_icon_img_1, relief=FLAT, command=escolhe_cor)
			btncor.grid(column=2, row=2, padx=5, pady=5, sticky=tk.S)
			lblMensagem = tk.Label(messageBar, fg="red", text = "", font=("Verdana", 8, 'bold'))
			lblMensagem.grid(column=0, row=0, ipadx=5, pady=5, sticky=tk.W+tk.S)
			
			botaoIncluir = Button(footer, image=v_cores_cdp_icon_img_2, relief=FLAT, command=insere)
			botaoIncluir.grid(column=0, row=8)
			botaoIncluir.bind("<Enter>", on_enter_botaoIncluir)
			botaoIncluir.bind("<Leave>", on_leave_botaoIncluir)
			
			botaoLimpar = Button(footer, image=v_cores_cdp_icon_img_4, relief=FLAT, command=limpa)
			botaoLimpar.grid(column=1, row=8)
			botaoLimpar.bind("<Enter>", on_enter_botaoLimpar)
			botaoLimpar.bind("<Leave>", on_leave_botaoLimpar)			
			
			botaoApagar = Button(footer, image=v_cores_cdp_icon_img_5, relief=FLAT, command=exclui)
			botaoApagar.grid(column=2, row=8)
			botaoApagar.bind("<Enter>", on_enter_botaoApagar)
			botaoApagar.bind("<Leave>", on_leave_botaoApagar)			
			
			statusbarrodape = tk.Label(status, text="", font=("Verdana", 10), anchor=tk.W)
			statusbarrodape.pack(side=tk.BOTTOM, fill=tk.X)
			t.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_novo, t.destroy))
			t.iconbitmap(default='transparent.ico')
			windowWidth, windowHeight = resolucao_width_cadastro, resolucao_height_cadastro
			positionRight = int(t.winfo_screenwidth()/2 - windowWidth/2)
			positionDown = int(t.winfo_screenheight()/2 - windowHeight/2)
			t.geometry("+{}+{}".format(positionRight, positionDown))
			if v_cores_cdp_modo == 'EDICAO':
				iniciaEdicao()
			t.attributes("-toolwindow", True)
			t.attributes("-topmost", True)
		def edicao():
			global selecionado
			global v_cores_cdp_modo
			
			curItem = treev.focus()
			selecionado = treev.item(curItem)['values']
			
			if selecionado <> '':
				v_cores_cdp_modo = 'EDICAO'
				novo()
		def exportar():
			workbook = xlwt.Workbook()
			sheet = workbook.add_sheet("Sheet Name")
			query = "select SIGLA, DESCRICAO, COR, ORDENACAO from CORES_CDP"
			cursor.execute(query)
			resultado = cursor.fetchall()
			sigla = ""
			descricao = ""
			cor = ""
			ordenacao = ""
			
			k = 0
			for i in resultado:
				sigla = i[0]
				descricao = i[1]
				cor = i[2]
				ordenacao = i[3]
				
				RGB_1 = tuple(int(cor.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))[0]
				RGB_2 = tuple(int(cor.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))[1]
				RBG_3 = tuple(int(cor.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))[2]
				
				xlwt.add_palette_colour("custom_colour" + str(k), 0x21 + k)
				workbook.set_colour_RGB(0x21 + k, RGB_1, RGB_2, RBG_3)
					
				font = xlwt.Font()
				font.name = 'Times New Roman'				
					
				style = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour' + str(k))
				style.font = font
																			
				sheet.write(k, 0, sigla)
				sheet.write(k, 1, descricao)
				sheet.write(k, 2, cor, style)
				sheet.write(k, 3, ordenacao)
				k = k + 1
				 
			workbook.save("sample.xls")		
		u = tk.Toplevel()
		u.grab_set()
		footer = tk.Frame(u, height=30)
		footer.pack(fill='both', side='bottom')
		u.resizable(width = 1, height = 1)
		treev = ttk.Treeview(u, selectmode ='browse')
		treev.pack(side ='right')
		verscrlbar = ttk.Scrollbar(u, orient ="vertical", command = treev.yview)
		verscrlbar.pack(side ='right', fill ='x')
		treev.configure(xscrollcommand = verscrlbar.set)
		treev["columns"] = ("1", "2", "3", "4")
		treev['show'] = 'headings'
		treev.column("1", width = 90, anchor ='c')
		treev.column("2", width = 90, anchor ='se')
		treev.column("3", width = 90, anchor ='se')
		treev.column("4", width = 90, anchor ='se')
		treev.heading("1", text ="SIGLA")
		treev.heading("2", text ="DESCRIÇÂO")
		treev.heading("3", text ="COR")
		treev.heading("4", text ="ORDENAÇÃO")
		treev.bind("<<TreeviewSelect>>", seleciona)
		refresh_consulta()
		botaoFechar = Button(footer, text='FECHAR', command=u.destroy)
		botaoFechar.pack(side=tk.RIGHT, padx = 5, pady = 5)
		botaoEditar = Button(footer, text='EDITAR', command=edicao)
		botaoEditar.pack(side=tk.RIGHT, padx = 5, pady = 5)
		botaoExportar = Button(footer, text='EXPORTAR', command=exportar)
		botaoExportar.pack(side=tk.RIGHT, padx = 5, pady = 5)
		botaoNovo = Button(footer, text='NOVO', command=novo)
		botaoNovo.pack(side=tk.RIGHT, padx = 5, pady = 5)
		u.geometry(resolucao_tela_cadastro)
		u.title('Consulta cores - CDP')
		u.protocol("WM_DELETE_WINDOW", u.destroy)
		u.iconbitmap(default='transparent.ico')					
		windowWidth, windowHeight = resolucao_width_cadastro, resolucao_height_cadastro
		positionRight = int(u.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(u.winfo_screenheight()/2 - windowHeight/2)
		u.geometry("+{}+{}".format(positionRight, positionDown))
		u.attributes("-toolwindow", True)
		u.attributes("-topmost", True)		
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
v_cores_cdp_icon_2 = Image.open("ADD_32x32.png")
v_cores_cdp_icon_3 = Image.open("SEARCH_16x16.png")
v_cores_cdp_icon_4 = Image.open("CLEAR_32x32.png")
v_cores_cdp_icon_5 = Image.open("DELETE_32x32.png")
 
# Cria Imagens
imagem1 = ImageTk.PhotoImage(icone1)
imagem2 = ImageTk.PhotoImage(icone2)
imagem3 = ImageTk.PhotoImage(icone3)
v_cores_cdp_icon_img_1 = ImageTk.PhotoImage(v_cores_cdp_icon_1)
v_cores_cdp_icon_img_2 = ImageTk.PhotoImage(v_cores_cdp_icon_2)
v_cores_cdp_icon_img_3 = ImageTk.PhotoImage(v_cores_cdp_icon_3)
v_cores_cdp_icon_img_4 = ImageTk.PhotoImage(v_cores_cdp_icon_4)
v_cores_cdp_icon_img_5 = ImageTk.PhotoImage(v_cores_cdp_icon_5)
 
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
