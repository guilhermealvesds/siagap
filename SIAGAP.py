#!/usr/bin/env python
# -*- coding: latin-1 -*-
# main.py
 
# importa modulos
try:                        
    import tkinter as tk   
except:
    import Tkinter as tk

from PIL     import Image, ImageTk
from Tkinter import Tk,    Frame, Label, Message, StringVar, Canvas  
from Tkinter import Label, Button, LEFT, TOP, X, FLAT, RAISED, SUNKEN
from tkinter.colorchooser import askcolor
from tkinter import ttk
from tkinter import messagebox
from Tkconstants import *

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

cursor.execute("""CREATE TABLE IF NOT EXISTS CORES_AF (
            CODIGO INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            SIGLA CHARACTER(3)NOT NULL,
            DESCRICAO VARCHAR(20),
            INICIAL REAL NOT NULL,
            FINAL REAL NOT NULL,
            COR VARCHAR(7) NOT NULL,
            ORDENACAO CHARACTER(2) NOT NULL)""")
                        
cursor.execute("""CREATE TABLE IF NOT EXISTS CORES_PRODUTIVIDADE (
            CODIGO INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            SIGLA CHARACTER(4)NOT NULL,            
            INICIAL REAL NOT NULL,
            FINAL REAL NOT NULL,
            COR VARCHAR(7) NOT NULL,
            ORDENACAO CHARACTER(2) NOT NULL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS CORES_AG (
            CODIGO INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            SIGLA CHARACTER(4)NOT NULL,            
            INICIAL REAL NOT NULL,
            FINAL REAL NOT NULL,
            COR VARCHAR(7) NOT NULL,
            ORDENACAO CHARACTER(2) NOT NULL)""")
            
cursor.execute("""CREATE TABLE IF NOT EXISTS CORES_AV (
            SIGLA CHARACTER(5)NOT NULL PRIMARY KEY,
            DESCRICAO VARCHAR(25),
            COR VARCHAR(7) NOT NULL,
            ORDENACAO CHARACTER(2) NOT NULL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS CORES_ACASALAMENTO (
            SIGLA CHARACTER(1)NOT NULL PRIMARY KEY,
            COR VARCHAR(7) NOT NULL,
            ORDENACAO CHARACTER(2) NOT NULL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS CORCABECALHO (
            CORFUNDO VARCHAR(7) NOT NULL,            
            CORLETRA VARCHAR(7) NOT NULL)""")
            
cursor.execute("""CREATE TABLE IF NOT EXISTS SITUACOESBEZERRO (
            SIGLA CHARACTER(5)NOT NULL PRIMARY KEY,
            DESCRICAO VARCHAR(25))""")

cursor.execute("""CREATE TABLE IF NOT EXISTS CAUSASDESCARTE (
            SIGLA CHARACTER(3)NOT NULL PRIMARY KEY, 
            DESCRICAO VARCHAR(25))""")

cursor.execute("""CREATE TABLE IF NOT EXISTS RACAS (
            SIGLA CHARACTER(3)NOT NULL PRIMARY KEY, 
            DESCRICAO VARCHAR(25))""")

cursor.execute("""CREATE TABLE IF NOT EXISTS SITUACOESMATRIZES (
            SIGLA CHARACTER(3)NOT NULL PRIMARY KEY,
            COR VARCHAR(7), 
            SIT CHARACTER(3),
            SEXO CHARACTER(1),
            DESCRICAO VARCHAR(25))""")

# declaração variáveis

v_configura_tela_inicial = 0
v_cores_cdp = 0
v_cores_cdp_modo = 'INCLUSAO'

resolucao_tela = '640x320'
resolucao_width = 640
resolucao_height = 320

resolucao_tela_cadastro = '400x240'
resolucao_width_cadastro = 400
resolucao_height_cadastro = 240

resolucao_tela_cadastro2 = '400x280'
resolucao_width_cadastro2 = 400
resolucao_height_cadastro2 = 380

resolucao_tela_consulta = '680x320'
resolucao_width_consulta = 680
resolucao_height_consulta = 320

resolucao_tela_consulta2 = '790x320'
resolucao_width_consulta2 = 790
resolucao_height_consulta2 = 320

# define e implementa as funções
def client_exit():
	formulario.destroy()

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
		formulario.grab_set()
	def cores_cdp():
		selecionado = {
		"sigla": "",
		"descrição": "",
		"cor": "",
		"ordenação": ""
			}
		def on_close_cores_cdp():
			menuCor.grab_set()
			u.destroy()																		
		def novo():
			global selecionado
			global v_cores_cdp_modo
			def escolhe_cor():
				color_code = askcolor(parent = t, title = "Selecionar cor")
				lblcor_v['bg'] = color_code[1]
			def consiste():
				global v_cores_cdp_modo
												
				v_sigla = etrSigla.get()
				v_descricao = etrDescricao.get()
				v_ordenacao = etrOrdenacao.get()
				lblMensagem['fg'] = 'red'
				
				if v_cores_cdp_modo == 'INCLUSAO':
					if v_sigla == '':
						lblMensagem['text'] = '*PREENCHA A SIGLA'
						etrSigla.focus()
						t.after(5000, apaga_mensagem)
						return 0						
					if len(v_sigla) > 1:
						lblMensagem['text'] = '*A SIGLA DEVE TER APENAS UM CARACTERE'
						etrSigla.focus()
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
						etrSigla.focus()
						t.after(5000, apaga_mensagem)
						return 0
						
				if len(v_descricao) > 20:
					lblMensagem['text'] = '*A DESCRIÇÃO DEVE TER NO MÁXIMO 20 CARACTERES'
					etrDescricao.focus()
					t.after(5000, apaga_mensagem)
					return 0
				
				if v_ordenacao == '':
					lblMensagem['text'] = '*PREENCHA A ORDENACAO'
					etrOrdenacao.focus()
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
						etrSigla.delete(0, tk.END)
						etrDescricao.delete(0, tk.END)
						lblcor_v['bg'] = 'white'
						etrOrdenacao.delete(0, tk.END)
						etrSigla.focus()
						v_cores_cdp_modo = 'INCLUSAO'
					combine_funcs(on_close_novo(), t.destroy())				
			def apaga_mensagem():
				lblMensagem['text'] = ''
			def on_close_novo():
				global v_cores_cdp_modo
				
				v_cores_cdp_modo = 'INCLUSAO'			
				popular_grid()
				u.grab_set()																						
			def limpa():
				global v_cores_cdp_modo
				
				etrSigla['state'] = 'normal'
				v_cores_cdp_modo = 'INCLUSAO'
				etrSigla.delete(0, tk.END)
				etrDescricao.delete(0, tk.END)
				lblcor_v['bg'] = '#FFFFFF'
				etrOrdenacao.delete(0, tk.END)
				etrSigla.focus()
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
			def on_enter_botaoSair(e):
				statusbarrodape['text'] = '                FECHAR'
			def on_leave_botaoSair(e):
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
			
			botaoSair = Button(footer, image=v_cores_cdp_icon_img_5, relief=FLAT, command = combine_funcs(on_close_novo, t.destroy))
			botaoSair.grid(column=2, row=8)
			botaoSair.bind("<Enter>", on_enter_botaoSair)
			botaoSair.bind("<Leave>", on_leave_botaoSair)						
					
			statusbarrodape = tk.Label(status, text="", font=("Verdana", 10), anchor=tk.W)
			statusbarrodape.pack(side=tk.BOTTOM, fill=tk.X)
			t.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_novo, t.destroy))
			t.iconbitmap(default='transparent.ico')
			windowWidth, windowHeight = resolucao_width_cadastro, resolucao_height_cadastro
			positionRight = int(menuCor.winfo_screenwidth()/2 - windowWidth/2)
			positionDown = int(menuCor.winfo_screenheight()/2 - windowHeight/2)
			t.geometry("+{}+{}".format(positionRight, positionDown))			
			if v_cores_cdp_modo == 'EDICAO':
				iniciaEdicao()
			if etrSigla['state'] == 'normal':
				etrSigla.focus()
				
			t.attributes("-toolwindow", True)
			t.attributes("-topmost", True)
			t.attributes("-topmost", False)
		def criacao():
			global selecionado
			global v_cores_cdp_modo
			
			selecionado = ()
			v_cores_cdp_modo = 'INCLUSAO'
			novo()
		def edicao(sigla, descricao, cor, ordenacao):
			global selecionado
			global v_cores_cdp_modo
			
			selecionado = (sigla, descricao, cor, ordenacao)
			
			if selecionado <> '':
				v_cores_cdp_modo = 'EDICAO'
				novo()			
		def popular_grid():
			global selecionado
			
			COORDS_LIST = []
			buttons_dict = {}
			
			columns = 6									
			query = "select SIGLA, DESCRICAO, COR, ORDENACAO, (SELECT COUNT(SIGLA) FROM CORES_CDP) AS LINHAS from CORES_CDP ORDER BY ORDENACAO"
			cursor.execute(query)
			resultado = cursor.fetchall()
			sigla = ""
			descricao = ""
			cor = ""
			ordenacao = ""
			
			k = 0
									
			for i in resultado:
				k = k + 1
				for j in range(0, columns):
					coord = str(k)+"_"+str(j)
					COORDS_LIST.append(coord)
					
					try:
						widget = frame_buttons.grid_slaves(row=k, column=j)[0]
						widget.destroy()
					except:
						pass
						
					try:
						widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row=k, column=j)[0]
						widget.destroy()
					except:
						pass
						
					sigla = i[0]
					descricao = i[1]
					cor  = i[2]
					ordenacao = i[3]
					linhas = i[4]
									
					if j == 4:						
						buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EDITAR', font=("Verdana", 8))
						buttons_dict[COORDS_LIST[-1]]["command"] = lambda vSigla = sigla, vDescricao = descricao, vCor = cor, vOrdenacao = ordenacao: edicao(vSigla, vDescricao, vCor, vOrdenacao)
						buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)
					elif j == 5:						
						buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EXCLUIR', font=("Verdana", 8))
						buttons_dict[COORDS_LIST[-1]]["command"] = lambda vSigla = sigla, vLinhas = linhas + 1, vColunas = columns: exclui(vSigla, vLinhas, vColunas)
						buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)						
					else:
						b = tk.Label(frame_buttons, anchor=W, text='', borderwidth=2, relief="groove")
						
						if j == 0:
							b['text'] = i[0]
							b['width'] = 10
						if j == 1:
							b['text'] = i[1]
							b['width'] = 30
						if j == 2:
							b['bg'] = i[2]
							b['width'] = 15
						if j == 3:
							b['text'] = i[3]
							b['width'] = 11
						if j == 4:
							b['width'] = 10						
						b.grid(row=k, column=j, sticky='news')		
										
			# Update buttons frames idle tasks to let tkinter calculate buttons sizes
			frame_buttons.update_idletasks()
		def exclui(sigla, linhas, colunas):
			MsgBox = tk.messagebox.askquestion ('Excluir Cor','Deseja excluir esse registro?',icon = 'warning', parent = u)
			if MsgBox == 'yes':			
				for i in range(1, linhas):
					for j in range(0, colunas):
						try:						
							widget = frame_buttons.grid_slaves(row = i, column = j)[0]
							widget.destroy()							
						except:
							pass						
						
						try:							
							widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row = i, column = j)[0]
							widget.destroy()
						except:
							pass						
				
				Delete = "delete from CORES_CDP where SIGLA='%s'" %(sigla)
				cursor.execute(Delete)
				con.commit()				
						
				popular_grid()														
		u = tk.Toplevel()
		u.grab_set()
		u.geometry(resolucao_tela_consulta)
		u.title('Consulta Cores - Cores CDP')
		
		frame_top = tk.Frame(u)
		frame_top.grid(sticky='news', padx=1)
		
		frame_main = tk.Frame(u)
		frame_main.grid(sticky='news')
		
		label1 = tk.Label(frame_top, text="SIGLA", fg="black", font=("Verdana", 8, 'bold'), width=9, relief="groove", anchor=W)
		label1.grid(row=0, column=0)
		
		label2 = tk.Label(frame_top, text="DESCRIÇÃO", fg="black", font=("Verdana", 8, 'bold'), width = 26, relief="groove", anchor=W)
		label2.grid(row=0, column=1)
		
		label3 = tk.Label(frame_top, text="COR", fg="black", font=("Verdana", 8, 'bold'), width=13, relief="groove", anchor=W)
		label3.grid(row=0, column=2)
		
		label4 = tk.Label(frame_top, text="ORDENAÇÃO", fg="black", font=("Verdana", 8, 'bold'), relief="groove", anchor=W)
		label4.grid(row=0, column=3)
	
		# Create a frame for the canvas with non-zero row&column weights
		frame_canvas = tk.Frame(frame_main)
		frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky='nw')
		frame_canvas.grid_rowconfigure(0, weight=1)
		frame_canvas.grid_columnconfigure(0, weight=1)
		# Set grid_propagate to False to allow 5-by-5 buttons resizing later
		frame_canvas.grid_propagate(False)
		
		# Add a canvas in that frame
		canvas = tk.Canvas(frame_canvas, bg = "#FFFFFF")
		canvas.grid(row=0, column=0, sticky="news")
		
		# Link a scrollbar to the canvas
		vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
		vsb.grid(row=0, column=1, sticky='ns')
		canvas.configure(yscrollcommand=vsb.set)
		
		# Create a frame to contain the buttons
		frame_buttons = tk.Frame(canvas, bg="#FFFFFF")
		canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
				
		popular_grid()
				
		# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
				
		frame_canvas.config(width=680, height=260)
		
		# Set the canvas scrolling region
		canvas.config(scrollregion=canvas.bbox("all"))
		
		frame_bottom = tk.Frame(u)
		frame_bottom.grid(sticky='news', padx=1)
		
		botaoNovo = tk.Button(frame_bottom, text='NOVO', font=("Verdana", 8), command=lambda : criacao())
		botaoNovo.grid(row=2, column=0)

		botaoFechar = tk.Button(frame_bottom, text='FECHAR', font=("Verdana", 8), command=lambda : on_close_cores_cdp())
		botaoFechar.grid(row=2, column=1)

		windowWidth, windowHeight = resolucao_width_consulta, resolucao_height_consulta
		positionRight = int(menuCor.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(menuCor.winfo_screenheight()/2 - windowHeight/2)
		u.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_cores_cdp, u.destroy))
		u.geometry("+{}+{}".format(positionRight, positionDown))			
		u.attributes("-toolwindow", True)
		u.attributes("-topmost", True)
		u.attributes("-topmost", False)
	def cores_avaliacao_fenotipica():
		selecionado = {
		"codigo": "",
		"sigla": "",
		"descrição": "",
		"cor": "",
		"inicial": "",
		"final": "",
		"ordenação": ""
			}
		def on_close_cores_avaliacao_fenotipica():
			menuCor.grab_set()
			u.destroy()																
		def novo():
			global selecionado
			global v_cores_cdp_modo
			def escolhe_cor():
				color_code = askcolor(parent = t, title = "Selecionar cor")
				lblcor_v['bg'] = color_code[1]
			def consiste():
				global v_cores_cdp_modo
												
				v_sigla = etrSigla.get()
				v_descricao = etrDescricao.get()
				v_inicial = etrInicial.get()
				v_final = etrFinal.get()
				v_ordenacao = etrOrdenacao.get()
				lblMensagem['fg'] = 'red'				
				
				if v_sigla == '':
					lblMensagem['text'] = '*PREENCHA A SIGLA'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)						
					return 0						
				if len(v_sigla) > 3:
					lblMensagem['text'] = '*A SIGLA DEVE TER NO MÁXIMO 3 CARACTERES'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)
					return 0
				
				if len(v_descricao) > 20:
					lblMensagem['text'] = '*A DESCRIÇÃO DEVE TER NO MÁXIMO 20 CARACTERES'
					etrDescricao.focus()
					t.after(5000, apaga_mensagem)
					return 0
					
				if v_ordenacao == '':
					lblMensagem['text'] = '*PREENCHA A ORDENACAO'
					etrOrdenacao.focus()
					t.after(5000, apaga_mensagem)
					return 0
				
				if v_inicial == '':
					lblMensagem['text'] = '*PREENCHA O VALOR INICIAL'
					etrInicial.focus()
					t.after(5000, apaga_mensagem)
					return 0
					
				if v_final == '':
					lblMensagem['text'] = '*PREENCHA O VALOR FINAL'
					etrFinal.focus()
					t.after(5000, apaga_mensagem)
					return 0

				dbRollNo = ""				
				if v_cores_cdp_modo == 'INCLUSAO':
					Select="select INICIAL, FINAL from CORES_AF"
				else:
					Select="select INICIAL, FINAL from CORES_AF WHERE CODIGO not in ('%s')"%(selecionado[0])
				cursor.execute(Select)
				result = cursor.fetchall()
				for i in result:
					inicial = i[0]
					final = i[1]					
					if ((float(v_inicial) >= float(inicial)) and (float(v_inicial) <= float(final))) or ((float(v_final) >= float(inicial)) and (float(v_final) <= float(final))):						
						lblMensagem['text'] = '*A FAIXA DE VALORES JÁ ESTÁ SENDO UTILIZADA'
						etrInicial.focus()
						t.after(5000, apaga_mensagem)
						return 0
					
				if float(v_inicial) > float(v_final):
					lblMensagem['text'] = '*VALOR INICIAL DEVE SER MENOR QUE VALOR FINAL'
					etrInicial.focus()
					t.after(5000, apaga_mensagem)
					return 0					
									
				return 1
				
			def insere():
				global v_cores_cdp_modo			
				
				r = consiste()
				
				if bool(r):
					etrSigla['state'] = 'normal'
					
					if v_cores_cdp_modo == 'INCLUSAO':
						Insert=''' Insert into CORES_AF(SIGLA, DESCRICAO, INICIAL, FINAL, COR, ORDENACAO) values(?,?,?,?,?,?) '''
						Sigla = etrSigla.get()
						Descricao = etrDescricao.get()
						Inicial = etrInicial.get()
						Final = etrFinal.get()
						Cor = lblcor_v['bg']
						Ordenacao = etrOrdenacao.get()
						Value=(Sigla, Descricao, Inicial, Final, Cor, Ordenacao)
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
						codigo = selecionado[0]
						sigla = etrSigla.get()
						descricao = etrDescricao.get()
						cor = lblcor_v['bg']
						inicial = etrInicial.get()
						final = etrFinal.get()
						ordenacao = etrOrdenacao.get()
						Update = "update CORES_AF set CODIGO='%s', SIGLA='%s', DESCRICAO='%s', COR='%s', INICIAL='%s', FINAL='%s', ORDENACAO='%s' where codigo = '%s'" %(codigo, sigla, descricao, cor, inicial, final, ordenacao, codigo)
						cursor.execute(Update)
						con.commit()
						etrSigla.delete(0, tk.END)
						etrDescricao.delete(0, tk.END)
						lblcor_v['bg'] = 'white'
						etrInicial.delete(0, tk.END)
						etrFinal.delete(0, tk.END)
						etrOrdenacao.delete(0, tk.END)
						etrSigla.focus()
						v_cores_cdp_modo = 'INCLUSAO'
					combine_funcs(on_close_novo(), t.destroy())				
			def apaga_mensagem():
				lblMensagem['text'] = ''
			def on_close_novo():
				global v_cores_cdp_modo
				
				v_cores_cdp_modo = 'INCLUSAO'			
				popular_grid()
				u.grab_set()																						
			def limpa():
				global v_cores_cdp_modo
				
				etrSigla['state'] = 'normal'
				v_cores_cdp_modo = 'INCLUSAO'
				etrSigla.delete(0, tk.END)
				etrDescricao.delete(0, tk.END)
				lblcor_v['bg'] = '#FFFFFF'
				etrInicial.delete(0, tk.END)
				etrFinal.delete(0, tk.END)
				etrOrdenacao.delete(0, tk.END)
				etrSigla.focus()
			def iniciaEdicao():
				etrSigla['state'] = 'normal'
				etrSigla.delete(0, tk.END)
				etrSigla.insert(0, selecionado[1])
				etrDescricao.delete(0, tk.END)
				etrDescricao.insert(0, selecionado[2])
				lblcor_v['bg'] = selecionado[3]
				etrInicial.delete(0, tk.END)
				etrInicial.insert(0, selecionado[4])				
				etrFinal.delete(0, tk.END)
				etrFinal.insert(0, selecionado[5])
				etrOrdenacao.delete(0, tk.END)
				etrOrdenacao.insert(0, selecionado[6])
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
			def on_enter_botaoSair(e):
				statusbarrodape['text'] = '                FECHAR'
			def on_leave_botaoSair(e):
				statusbarrodape['text'] = ''
			t = tk.Toplevel()
			t.grab_set()
			t.geometry(resolucao_tela_cadastro2)
			t.title('Cores - Avaliação Fenótipica')
			content = tk.Frame(t)
			lblClassificacaoDEP = tk.LabelFrame(t, text="Classificação com ênfase na DEP")
			messageBar = tk.Frame(t, height=30)
			footer = tk.Frame(t, height=30)
			status = tk.Frame(t, height=30)
			content.pack(fill='both')
			lblClassificacaoDEP.pack(fill='both')
			messageBar.pack(fill='both')
			footer.pack(fill='both', side='bottom')
			status.pack(fill='both', side = 'bottom')
			lblsigla = Label(content, text = "Sigla:", font=("Verdana", 8, 'bold'))
			lblsigla.grid(column=0, row=0, ipadx=5, pady=5, sticky=tk.W+tk.N)
			lbldescricao = tk.Label(content, text = "Descrição:", font=("Verdana", 8, 'bold'))
			lbldescricao.grid(column=0, row=1, ipadx=5, pady=5, sticky=tk.W+tk.S)
			lblinicial = tk.Label(lblClassificacaoDEP, text = "Inicial:", font=("Verdana", 8, 'bold'))
			lblinicial.grid(column=0, row=0, ipadx=5, pady=5, sticky=tk.W+tk.S)
			lblfinal = tk.Label(lblClassificacaoDEP, text = "Final:", font=("Verdana", 8, 'bold'))
			lblfinal.grid(column=2, row=0, ipadx=5, pady=5, sticky=tk.W+tk.S)					
			lblcor = tk.Label(lblClassificacaoDEP, text = "Cor:", font=("Verdana", 8, 'bold'))
			lblcor.grid(column=0, row=1, ipadx=5, pady=5, sticky=tk.W+tk.S)
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
			
			etrInicial = tk.Entry(lblClassificacaoDEP, font = "Verdana 12", width=5)
			etrInicial.grid(column=1, row=0, padx=10, pady=5, sticky=tk.S)
			etrFinal = tk.Entry(lblClassificacaoDEP, font = "Verdana 12", width=5)
			etrFinal.grid(column=3, row=0, padx=10, pady=5, sticky=tk.S)			
			lblcor_v = tk.Label(lblClassificacaoDEP, bg="white", width=7)
			lblcor_v.grid(column=1, row=1)
			
			varEtrOrdenacao = tk.StringVar()
			etrOrdenacao = tk.Entry(content, font = "Verdana 12", width=20, textvariable=varEtrOrdenacao)
			etrOrdenacao.grid(column=1, row=3, padx=10, pady=5, sticky=tk.S)
			try:
				varEtrOrdenacao.trace_add('write', to_uppercaseOrdenacao)
			except AttributeError:
				varEtrOrdenacao.trace('w', to_uppercaseOrdenacao)
			
			btncor = Button(lblClassificacaoDEP, image=v_cores_cdp_icon_img_1, relief=FLAT, command=escolhe_cor)
			btncor.grid(column=2, row=1, padx=5, pady=5, sticky=tk.S)
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
			
			botaoSair = Button(footer, image=v_cores_cdp_icon_img_5, relief=FLAT, command = combine_funcs(on_close_novo, t.destroy))
			botaoSair.grid(column=2, row=8)
			botaoSair.bind("<Enter>", on_enter_botaoSair)
			botaoSair.bind("<Leave>", on_leave_botaoSair)						
					
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
			if etrSigla['state'] == 'normal':
				etrSigla.focus()				
			t.attributes("-toolwindow", True)
		def criacao():
			global selecionado
			global v_cores_cdp_modo
			
			selecionado = ()
			v_cores_cdp_modo = 'INCLUSAO'
			novo()
		def edicao(codigo, sigla, descricao, cor, inicial, final, ordenacao):
			global selecionado
			global v_cores_cdp_modo
			
			selecionado = (codigo, sigla, descricao, cor, inicial, final, ordenacao)
			
			if selecionado <> '':
				v_cores_cdp_modo = 'EDICAO'
				novo()			
		def popular_grid():
			global selecionado
			
			COORDS_LIST = []
			buttons_dict = {}
			
			columns = 8									
			query = "select CODIGO, SIGLA, DESCRICAO, COR, INICIAL, FINAL, ORDENACAO, (SELECT COUNT(SIGLA) FROM CORES_AF) AS LINHAS from CORES_AF ORDER BY ORDENACAO"
			cursor.execute(query)
			resultado = cursor.fetchall()
			sigla = ""
			descricao = ""
			cor = ""
			ordenacao = ""
			
			k = 0
									
			for i in resultado:
				k = k + 1
				for j in range(0, columns):
					coord = str(k)+"_"+str(j)
					COORDS_LIST.append(coord)
					
					try:
						widget = frame_buttons.grid_slaves(row=k, column=j)[0]
						widget.destroy()
					except:
						pass
						
					try:
						widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row=k, column=j)[0]
						widget.destroy()
					except:
						pass
					
					codigo = i[0]	
					sigla = i[1]
					descricao = i[2]
					cor  = i[3]
					inicial = i[4]
					final = i[5]
					ordenacao = i[6]
					linhas = i[7]
									
					if j == 6:						
						buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EDITAR', font=("Verdana", 8))
						buttons_dict[COORDS_LIST[-1]]["command"] = lambda vCodigo = codigo, vSigla = sigla, vDescricao = descricao, vCor = cor, vInicial = inicial, vFinal = final, vOrdenacao = ordenacao: edicao(vCodigo, vSigla, vDescricao, vCor, vInicial, vFinal, vOrdenacao)
						buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)
					elif j == 7:						
						buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EXCLUIR', font=("Verdana", 8))
						buttons_dict[COORDS_LIST[-1]]["command"] = lambda vCodigo = codigo, vLinhas = linhas + 1, vColunas = columns: exclui(vCodigo, vLinhas, vColunas)
						buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)						
					else:
						b = tk.Label(frame_buttons, anchor=W, text='', borderwidth=2, relief="groove")
						
						if j == 0:
							b['text'] = i[1]
							b['width'] = 10
						if j == 1:
							b['text'] = i[2]
							b['width'] = 30
						if j == 2:
							b['bg'] = i[3]							
							b['width'] = 15
						if j == 3:
							b['text'] = i[4]
							b['width'] = 9
						if j == 4:
							b['text'] = i[5]							
							b['width'] = 9
						if j == 5:
							b['text'] = i[6]
							b['width'] = 12														
						if j == 6:
							b['width'] = 5						
						b.grid(row=k, column=j, sticky='news')		
										
			# Update buttons frames idle tasks to let tkinter calculate buttons sizes
			frame_buttons.update_idletasks()
		def exclui(codigo, linhas, colunas):
			MsgBox = tk.messagebox.askquestion ('Excluir Cor','Deseja excluir esse registro?',icon = 'warning', parent = u)
			if MsgBox == 'yes':			
				for i in range(1, linhas):
					for j in range(0, colunas):
						try:						
							widget = frame_buttons.grid_slaves(row = i, column = j)[0]
							widget.destroy()							
						except:
							pass						
						
						try:							
							widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row = i, column = j)[0]
							widget.destroy()
						except:
							pass						
				
				Delete = "delete from CORES_AF where CODIGO='%s'" %(codigo)
				cursor.execute(Delete)
				con.commit()				
						
				popular_grid()														
		u = tk.Toplevel()
		u.grab_set()
		u.geometry(resolucao_tela_consulta2)
		u.title('Consulta Cores - Avaliação Fenótipica')
		
		frame_top = tk.Frame(u)
		frame_top.grid(sticky='news', padx=1)
		
		frame_main = tk.Frame(u)
		frame_main.grid(sticky='news')
		
		label1 = tk.Label(frame_top, text="SIGLA", fg="black", font=("Verdana", 8, 'bold'), width=9, relief="groove", anchor=W)
		label1.grid(row=0, column=0)
		
		label2 = tk.Label(frame_top, text="DESCRIÇÃO", fg="black", font=("Verdana", 8, 'bold'), width=26, relief="groove", anchor=W)
		label2.grid(row=0, column=1)
		
		label3 = tk.Label(frame_top, text="COR", fg="black", font=("Verdana", 8, 'bold'), width=13, relief="groove", anchor=W)
		label3.grid(row=0, column=2)
		
		label4 = tk.Label(frame_top, text="ORDENAÇÃO", fg="black", font=("Verdana", 8, 'bold'), width=10, relief="groove", anchor=W)
		label4.grid(row=0, column=5)

		label5 = tk.Label(frame_top, text="INICIAL", fg="black", font=("Verdana", 8, 'bold'), width=8, relief="groove", anchor=W)
		label5.grid(row=0, column=3)
		
		label6 = tk.Label(frame_top, text="FINAL", fg="black", font=("Verdana", 8, 'bold'), width=8, relief="groove", anchor=W)
		label6.grid(row=0, column=4)	
	
		# Create a frame for the canvas with non-zero row&column weights
		frame_canvas = tk.Frame(frame_main)
		frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky='nw')
		frame_canvas.grid_rowconfigure(0, weight=1)
		frame_canvas.grid_columnconfigure(0, weight=1)
		# Set grid_propagate to False to allow 5-by-5 buttons resizing later
		frame_canvas.grid_propagate(False)
		
		# Add a canvas in that frame
		canvas = tk.Canvas(frame_canvas, bg = "#FFFFFF")
		canvas.grid(row=0, column=0, sticky="news")
		
		# Link a scrollbar to the canvas
		vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
		vsb.grid(row=0, column=1, sticky='ns')
		canvas.configure(yscrollcommand=vsb.set)
		
		# Create a frame to contain the buttons
		frame_buttons = tk.Frame(canvas, bg="#FFFFFF")
		canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
				
		popular_grid()
				
		# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
				
		frame_canvas.config(width=780, height=260)
		
		# Set the canvas scrolling region
		canvas.config(scrollregion=canvas.bbox("all"))
		
		frame_bottom = tk.Frame(u)
		frame_bottom.grid(sticky='news', padx=1)
		
		botaoNovo = tk.Button(frame_bottom, text='NOVO', font=("Verdana", 8), command=lambda : criacao())
		botaoNovo.grid(row=2, column=0)

		botaoFechar = tk.Button(frame_bottom, text='FECHAR', font=("Verdana", 8), command=lambda : on_close_cores_avaliacao_fenotipica())
		botaoFechar.grid(row=2, column=1)

		windowWidth, windowHeight = resolucao_width_consulta2, resolucao_height_consulta2
		positionRight = int(menuCor.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(menuCor.winfo_screenheight()/2 - windowHeight/2)
		u.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_cores_avaliacao_fenotipica, u.destroy))
		u.geometry("+{}+{}".format(positionRight, positionDown))			
		u.attributes("-toolwindow", True)		
	def cores_produtividade():
		selecionado = {
		"codigo": "",
		"sigla": "",
		"cor": "",
		"inicial": "",
		"final": "",
		"ordenação": ""
			}
		def on_close_cores_produtividade():
			menuCor.grab_set()
			u.destroy()															
		def novo():
			global selecionado
			global v_cores_cdp_modo
			def escolhe_cor():
				color_code = askcolor(parent = t, title = "Selecionar cor")
				lblcor_v['bg'] = color_code[1]
			def consiste():
				global v_cores_cdp_modo
												
				v_sigla = etrSigla.get()
				v_inicial = etrInicial.get()
				v_final = etrFinal.get()
				v_ordenacao = etrOrdenacao.get()
				lblMensagem['fg'] = 'red'				
				
				if v_sigla == '':
					lblMensagem['text'] = '*PREENCHA A SIGLA'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)						
					return 0						
				if len(v_sigla) > 3:
					lblMensagem['text'] = '*A SIGLA DEVE TER NO MÁXIMO 3 CARACTERES'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)
					return 0			
					
				if v_ordenacao == '':
					lblMensagem['text'] = '*PREENCHA A ORDENACAO'
					etrOrdenacao.focus()
					t.after(5000, apaga_mensagem)
					return 0
				
				if v_inicial == '':
					lblMensagem['text'] = '*PREENCHA O VALOR INICIAL'
					etrInicial.focus()
					t.after(5000, apaga_mensagem)
					return 0
					
				if v_final == '':
					lblMensagem['text'] = '*PREENCHA O VALOR FINAL'
					etrFinal.focus()
					t.after(5000, apaga_mensagem)
					return 0

				dbRollNo = ""
				if v_cores_cdp_modo == 'INCLUSAO':
					Select="select INICIAL, FINAL from CORES_PRODUTIVIDADE"
				else:
					Select="select INICIAL, FINAL from CORES_PRODUTIVIDADE WHERE CODIGO not in ('%s')"%(selecionado[0])
				cursor.execute(Select)
				result = cursor.fetchall()
				for i in result:
					inicial = i[0]
					final = i[1]					
					if ((float(v_inicial) >= float(inicial)) and (float(v_inicial) <= float(final))) or ((float(v_final) >= float(inicial)) and (float(v_final) <= float(final))):						
						lblMensagem['text'] = '*A FAIXA DE VALORES JÁ ESTÁ SENDO UTILIZADA'
						etrInicial.focus()
						t.after(5000, apaga_mensagem)
						return 0
					
				if float(v_inicial) > float(v_final):
					lblMensagem['text'] = '*VALOR INICIAL DEVE SER MENOR QUE VALOR FINAL'
					etrInicial.focus()
					t.after(5000, apaga_mensagem)
					return 0					
									
				return 1
				
			def insere():
				global v_cores_cdp_modo			
				
				r = consiste()
				
				if bool(r):
					etrSigla['state'] = 'normal'
					
					if v_cores_cdp_modo == 'INCLUSAO':
						Insert=''' Insert into CORES_PRODUTIVIDADE(SIGLA, INICIAL, FINAL, COR, ORDENACAO) values(?,?,?,?,?) '''
						Sigla = etrSigla.get()						
						Inicial = etrInicial.get()
						Final = etrFinal.get()
						Cor = lblcor_v['bg']
						Ordenacao = etrOrdenacao.get()
						Value=(Sigla, Inicial, Final, Cor, Ordenacao)
						cursor.execute(Insert, Value)
						con.commit()
						lblMensagem['fg'] = '#2D8C2B'
						lblMensagem['text'] = '*REGISTRO INCLUÍDO COM SUCESSO'
						etrSigla.delete(0, tk.END)
						lblcor_v['bg'] = 'white'
						etrOrdenacao.delete(0, tk.END)
						etrSigla.focus()
						t.after(4000, apaga_mensagem)						
					if v_cores_cdp_modo == 'EDICAO':
						codigo = selecionado[0]
						sigla = etrSigla.get()						
						cor = lblcor_v['bg']
						inicial = etrInicial.get()
						final = etrFinal.get()
						ordenacao = etrOrdenacao.get()
						Update = "update CORES_PRODUTIVIDADE set CODIGO='%s', SIGLA='%s', COR='%s', INICIAL='%s', FINAL='%s', ORDENACAO='%s' where codigo = '%s'" %(codigo, sigla, cor, inicial, final, ordenacao, codigo)
						cursor.execute(Update)
						con.commit()
						etrSigla.delete(0, tk.END)
						lblcor_v['bg'] = 'white'
						etrInicial.delete(0, tk.END)
						etrFinal.delete(0, tk.END)
						etrOrdenacao.delete(0, tk.END)
						etrSigla.focus()
						v_cores_cdp_modo = 'INCLUSAO'
					combine_funcs(on_close_novo(), t.destroy())				
			def apaga_mensagem():
				lblMensagem['text'] = ''
			def on_close_novo():
				global v_cores_cdp_modo
				
				v_cores_cdp_modo = 'INCLUSAO'			
				popular_grid()
				u.grab_set()																						
			def limpa():
				global v_cores_cdp_modo
				
				etrSigla['state'] = 'normal'
				v_cores_cdp_modo = 'INCLUSAO'
				etrSigla.delete(0, tk.END)
				lblcor_v['bg'] = '#FFFFFF'
				etrInicial.delete(0, tk.END)
				etrFinal.delete(0, tk.END)
				etrOrdenacao.delete(0, tk.END)
				etrSigla.focus()
			def iniciaEdicao():
				etrSigla['state'] = 'normal'
				etrSigla.delete(0, tk.END)
				etrSigla.insert(0, selecionado[1])
				lblcor_v['bg'] = selecionado[2]
				etrInicial.delete(0, tk.END)
				etrInicial.insert(0, selecionado[3])				
				etrFinal.delete(0, tk.END)
				etrFinal.insert(0, selecionado[4])
				etrOrdenacao.delete(0, tk.END)
				etrOrdenacao.insert(0, selecionado[5])
			def to_uppercaseSigla(*args):
				varEtrSigla.set(varEtrSigla.get().upper())
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
			def on_enter_botaoSair(e):
				statusbarrodape['text'] = '                FECHAR'
			def on_leave_botaoSair(e):
				statusbarrodape['text'] = ''
			t = tk.Toplevel()
			t.grab_set()
			t.geometry(resolucao_tela_cadastro2)
			t.title('Cores - Produtividade')
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
			lblinicial = tk.Label(content, text = "Inicial:", font=("Verdana", 8, 'bold'))
			lblinicial.grid(column=0, row=1, ipadx=5, pady=5, sticky=tk.W+tk.S)
			lblfinal = tk.Label(content, text = "Final:", font=("Verdana", 8, 'bold'))
			lblfinal.grid(column=2, row=1, ipadx=5, pady=5, sticky=tk.W+tk.S)					
			lblcor = tk.Label(content, text = "Cor:", font=("Verdana", 8, 'bold'))
			lblcor.grid(column=0, row=2, ipadx=5, pady=5, sticky=tk.W+tk.S)
			lblOrdenacao = tk.Label(content, text = "Ordenação:", font=("Verdana", 8, 'bold'))
			lblOrdenacao.grid(column=0, row=3, ipadx=5, pady=5, sticky=tk.W+tk.S)
			
			varEtrSigla = tk.StringVar()		
			etrSigla = tk.Entry(content, font = "Verdana 12", width=5, textvariable=varEtrSigla)
			etrSigla.grid(column=1, row=0, padx=10, pady=5, sticky=tk.N)			
			try:
				varEtrSigla.trace_add('write', to_uppercaseSigla)
			except AttributeError:
				varEtrSigla.trace('w', to_uppercaseSigla)
					
			etrInicial = tk.Entry(content, font = "Verdana 12", width=5)
			etrInicial.grid(column=1, row=1, padx=10, pady=5, sticky=tk.S)
			etrFinal = tk.Entry(content, font = "Verdana 12", width=5)
			etrFinal.grid(column=3, row=1, padx=10, pady=5, sticky=tk.S)			
			lblcor_v = tk.Label(content, bg="white", width=7)
			lblcor_v.grid(column=1, row=2)
			
			varEtrOrdenacao = tk.StringVar()
			etrOrdenacao = tk.Entry(content, font = "Verdana 12", width=5, textvariable=varEtrOrdenacao)
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
			
			botaoSair = Button(footer, image=v_cores_cdp_icon_img_5, relief=FLAT, command = combine_funcs(on_close_novo, t.destroy))
			botaoSair.grid(column=2, row=8)
			botaoSair.bind("<Enter>", on_enter_botaoSair)
			botaoSair.bind("<Leave>", on_leave_botaoSair)						
					
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
			if etrSigla['state'] == 'normal':
				etrSigla.focus()
				
			t.attributes("-toolwindow", True)			
		def criacao():
			global selecionado
			global v_cores_cdp_modo
			
			selecionado = ()
			v_cores_cdp_modo = 'INCLUSAO'
			novo()
		def edicao(codigo, sigla, cor, inicial, final, ordenacao):
			global selecionado
			global v_cores_cdp_modo
			
			selecionado = (codigo, sigla, cor, inicial, final, ordenacao)
			
			if selecionado <> '':
				v_cores_cdp_modo = 'EDICAO'
				novo()			
		def popular_grid():
			global selecionado
			
			COORDS_LIST = []
			buttons_dict = {}
			
			columns = 7									
			query = "select CODIGO, SIGLA, COR, INICIAL, FINAL, ORDENACAO, (SELECT COUNT(SIGLA) FROM CORES_PRODUTIVIDADE) AS LINHAS from CORES_PRODUTIVIDADE ORDER BY ORDENACAO"
			cursor.execute(query)
			resultado = cursor.fetchall()
			sigla = ""
			cor = ""
			ordenacao = ""
			
			k = 0
									
			for i in resultado:
				k = k + 1
				for j in range(0, columns):
					coord = str(k)+"_"+str(j)
					COORDS_LIST.append(coord)
					
					try:
						widget = frame_buttons.grid_slaves(row=k, column=j)[0]
						widget.destroy()
					except:
						pass
						
					try:
						widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row=k, column=j)[0]
						widget.destroy()
					except:
						pass
					
					codigo = i[0]	
					sigla = i[1]
					cor  = i[2]
					inicial = i[3]
					final = i[4]
					ordenacao = i[5]
					linhas = i[6]
									
					if j == 5:						
						buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EDITAR', font=("Verdana", 8))
						buttons_dict[COORDS_LIST[-1]]["command"] = lambda vCodigo = codigo, vSigla = sigla, vCor = cor, vInicial = inicial, vFinal = final, vOrdenacao = ordenacao: edicao(vCodigo, vSigla, vCor, vInicial, vFinal, vOrdenacao)
						buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)
					elif j == 6:						
						buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EXCLUIR', font=("Verdana", 8))
						buttons_dict[COORDS_LIST[-1]]["command"] = lambda vCodigo = codigo, vLinhas = linhas + 1, vColunas = columns: exclui(vCodigo, vLinhas, vColunas)
						buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)						
					else:
						b = tk.Label(frame_buttons, anchor=W, text='', borderwidth=2, relief="groove")
						
						if j == 0:
							b['text'] = i[1]
							b['width'] = 10
						if j == 1:
							b['bg'] = i[2]							
							b['width'] = 15
						if j == 2:
							b['text'] = i[3]
							b['width'] = 9
						if j == 3:
							b['text'] = i[4]							
							b['width'] = 9
						if j == 4:
							b['text'] = i[5]
							b['width'] = 12
						b.grid(row=k, column=j, sticky='news')		
										
			# Update buttons frames idle tasks to let tkinter calculate buttons sizes
			frame_buttons.update_idletasks()
		def exclui(codigo, linhas, colunas):
			MsgBox = tk.messagebox.askquestion ('Excluir Cor','Deseja excluir esse registro?',icon = 'warning', parent = u)
			if MsgBox == 'yes':			
				for i in range(1, linhas):
					for j in range(0, colunas):
						try:						
							widget = frame_buttons.grid_slaves(row = i, column = j)[0]
							widget.destroy()							
						except:
							pass						
						
						try:							
							widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row = i, column = j)[0]
							widget.destroy()
						except:
							pass						
				
				Delete = "delete from CORES_PRODUTIVIDADE where CODIGO='%s'" %(codigo)
				cursor.execute(Delete)
				con.commit()				
						
				popular_grid()														
		u = tk.Toplevel()
		u.grab_set()
		u.geometry(resolucao_tela_consulta2)
		u.title('Consulta Cores - Produtividade')
		
		frame_top = tk.Frame(u)
		frame_top.grid(sticky='news', padx=1)
		
		frame_main = tk.Frame(u)
		frame_main.grid(sticky='news')
		
		label1 = tk.Label(frame_top, text="SIGLA", fg="black", font=("Verdana", 8, 'bold'), width=9, relief="groove", anchor=W)
		label1.grid(row=0, column=0)
	
		label3 = tk.Label(frame_top, text="COR", fg="black", font=("Verdana", 8, 'bold'), width=13, relief="groove", anchor=W)
		label3.grid(row=0, column=1)
		
		label4 = tk.Label(frame_top, text="ORDENAÇÃO", fg="black", font=("Verdana", 8, 'bold'), width=10, relief="groove", anchor=W)
		label4.grid(row=0, column=4)

		label5 = tk.Label(frame_top, text="INICIAL", fg="black", font=("Verdana", 8, 'bold'), width=8, relief="groove", anchor=W)
		label5.grid(row=0, column=2)
		
		label6 = tk.Label(frame_top, text="FINAL", fg="black", font=("Verdana", 8, 'bold'), width=8, relief="groove", anchor=W)
		label6.grid(row=0, column=3)	
	
		# Create a frame for the canvas with non-zero row&column weights
		frame_canvas = tk.Frame(frame_main)
		frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky='nw')
		frame_canvas.grid_rowconfigure(0, weight=1)
		frame_canvas.grid_columnconfigure(0, weight=1)
		# Set grid_propagate to False to allow 5-by-5 buttons resizing later
		frame_canvas.grid_propagate(False)
		
		# Add a canvas in that frame
		canvas = tk.Canvas(frame_canvas, bg = "#FFFFFF")
		canvas.grid(row=0, column=0, sticky="news")
		
		# Link a scrollbar to the canvas
		vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
		vsb.grid(row=0, column=1, sticky='ns')
		canvas.configure(yscrollcommand=vsb.set)
		
		# Create a frame to contain the buttons
		frame_buttons = tk.Frame(canvas, bg="#FFFFFF")
		canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
				
		popular_grid()
				
		# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
				
		frame_canvas.config(width=780, height=260)
		
		# Set the canvas scrolling region
		canvas.config(scrollregion=canvas.bbox("all"))
		
		frame_bottom = tk.Frame(u)
		frame_bottom.grid(sticky='news', padx=1)
		
		botaoNovo = tk.Button(frame_bottom, text='NOVO', font=("Verdana", 8), command=lambda : criacao())
		botaoNovo.grid(row=2, column=0)

		botaoFechar = tk.Button(frame_bottom, text='FECHAR', font=("Verdana", 8), command=lambda : on_close_cores_produtividade())
		botaoFechar.grid(row=2, column=1)

		windowWidth, windowHeight = resolucao_width_consulta2, resolucao_height_consulta2
		positionRight = int(menuCor.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(menuCor.winfo_screenheight()/2 - windowHeight/2)
		u.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_cores_produtividade, u.destroy))
		u.geometry("+{}+{}".format(positionRight, positionDown))			
		u.attributes("-toolwindow", True)		
	def cores_avaliacao_genetica():
		selecionado = {
		"codigo": "",
		"sigla": "",
		"cor": "",
		"inicial": "",
		"final": "",
		"ordenação": ""
			}
		def on_close_cores_avaliacao_genetica():
			menuCor.grab_set()
			u.destroy()															
		def novo():
			global selecionado
			global v_cores_cdp_modo
			def escolhe_cor():
				color_code = askcolor(parent = t, title = "Selecionar cor")
				lblcor_v['bg'] = color_code[1]
			def consiste():
				global v_cores_cdp_modo
												
				v_sigla = etrSigla.get()
				v_inicial = etrInicial.get()
				v_final = etrFinal.get()
				v_ordenacao = etrOrdenacao.get()
				lblMensagem['fg'] = 'red'				
				
				if v_sigla == '':
					lblMensagem['text'] = '*PREENCHA A SIGLA'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)						
					return 0						
				if len(v_sigla) > 3:
					lblMensagem['text'] = '*A SIGLA DEVE TER NO MÁXIMO 3 CARACTERES'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)
					return 0			
					
				if v_ordenacao == '':
					lblMensagem['text'] = '*PREENCHA A ORDENACAO'
					etrOrdenacao.focus()
					t.after(5000, apaga_mensagem)
					return 0
				
				if v_inicial == '':
					lblMensagem['text'] = '*PREENCHA O VALOR INICIAL'
					etrInicial.focus()
					t.after(5000, apaga_mensagem)
					return 0
					
				if v_final == '':
					lblMensagem['text'] = '*PREENCHA O VALOR FINAL'
					etrFinal.focus()
					t.after(5000, apaga_mensagem)
					return 0

				dbRollNo = ""
				if v_cores_cdp_modo == 'INCLUSAO':
					Select="select INICIAL, FINAL from CORES_AG"
				else:
					Select="select INICIAL, FINAL from CORES_AG WHERE CODIGO not in ('%s')"%(selecionado[0])
				cursor.execute(Select)
				result = cursor.fetchall()
				for i in result:
					inicial = i[0]
					final = i[1]					
					if ((float(v_inicial) >= float(inicial)) and (float(v_inicial) <= float(final))) or ((float(v_final) >= float(inicial)) and (float(v_final) <= float(final))):						
						lblMensagem['text'] = '*A FAIXA DE VALORES JÁ ESTÁ SENDO UTILIZADA'
						etrInicial.focus()
						t.after(5000, apaga_mensagem)
						return 0
					
				if float(v_inicial) > float(v_final):
					lblMensagem['text'] = '*VALOR INICIAL DEVE SER MENOR QUE VALOR FINAL'
					etrInicial.focus()
					t.after(5000, apaga_mensagem)
					return 0					
									
				return 1
				
			def insere():
				global v_cores_cdp_modo			
				
				r = consiste()
				
				if bool(r):
					etrSigla['state'] = 'normal'
					
					if v_cores_cdp_modo == 'INCLUSAO':
						Insert=''' Insert into CORES_AG(SIGLA, INICIAL, FINAL, COR, ORDENACAO) values(?,?,?,?,?) '''
						Sigla = etrSigla.get()						
						Inicial = etrInicial.get()
						Final = etrFinal.get()
						Cor = lblcor_v['bg']
						Ordenacao = etrOrdenacao.get()
						Value=(Sigla, Inicial, Final, Cor, Ordenacao)
						cursor.execute(Insert, Value)
						con.commit()
						lblMensagem['fg'] = '#2D8C2B'
						lblMensagem['text'] = '*REGISTRO INCLUÍDO COM SUCESSO'
						etrSigla.delete(0, tk.END)
						lblcor_v['bg'] = 'white'
						etrOrdenacao.delete(0, tk.END)
						etrSigla.focus()
						t.after(4000, apaga_mensagem)						
					if v_cores_cdp_modo == 'EDICAO':
						codigo = selecionado[0]
						sigla = etrSigla.get()						
						cor = lblcor_v['bg']
						inicial = etrInicial.get()
						final = etrFinal.get()
						ordenacao = etrOrdenacao.get()
						Update = "update CORES_AG set CODIGO='%s', SIGLA='%s', COR='%s', INICIAL='%s', FINAL='%s', ORDENACAO='%s' where codigo = '%s'" %(codigo, sigla, cor, inicial, final, ordenacao, codigo)
						cursor.execute(Update)
						con.commit()
						etrSigla.delete(0, tk.END)
						lblcor_v['bg'] = 'white'
						etrInicial.delete(0, tk.END)
						etrFinal.delete(0, tk.END)
						etrOrdenacao.delete(0, tk.END)
						etrSigla.focus()
						v_cores_cdp_modo = 'INCLUSAO'
					combine_funcs(on_close_novo(), t.destroy())				
			def apaga_mensagem():
				lblMensagem['text'] = ''
			def on_close_novo():
				global v_cores_cdp_modo
				
				v_cores_cdp_modo = 'INCLUSAO'			
				popular_grid()
				u.grab_set()																						
			def limpa():
				global v_cores_cdp_modo
				
				etrSigla['state'] = 'normal'
				v_cores_cdp_modo = 'INCLUSAO'
				etrSigla.delete(0, tk.END)
				lblcor_v['bg'] = '#FFFFFF'
				etrInicial.delete(0, tk.END)
				etrFinal.delete(0, tk.END)
				etrOrdenacao.delete(0, tk.END)
				etrSigla.focus()
			def iniciaEdicao():
				etrSigla['state'] = 'normal'
				etrSigla.delete(0, tk.END)
				etrSigla.insert(0, selecionado[1])
				lblcor_v['bg'] = selecionado[2]
				etrInicial.delete(0, tk.END)
				etrInicial.insert(0, selecionado[3])				
				etrFinal.delete(0, tk.END)
				etrFinal.insert(0, selecionado[4])
				etrOrdenacao.delete(0, tk.END)
				etrOrdenacao.insert(0, selecionado[5])
			def to_uppercaseSigla(*args):
				varEtrSigla.set(varEtrSigla.get().upper())
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
			def on_enter_botaoSair(e):
				statusbarrodape['text'] = '                FECHAR'
			def on_leave_botaoSair(e):
				statusbarrodape['text'] = ''
			t = tk.Toplevel()
			t.grab_set()
			t.geometry(resolucao_tela_cadastro2)
			t.title('Cores - Avaliação Genética')
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
			lblinicial = tk.Label(content, text = "Inicial:", font=("Verdana", 8, 'bold'))
			lblinicial.grid(column=0, row=1, ipadx=5, pady=5, sticky=tk.W+tk.S)
			lblfinal = tk.Label(content, text = "Final:", font=("Verdana", 8, 'bold'))
			lblfinal.grid(column=2, row=1, ipadx=5, pady=5, sticky=tk.W+tk.S)					
			lblcor = tk.Label(content, text = "Cor:", font=("Verdana", 8, 'bold'))
			lblcor.grid(column=0, row=2, ipadx=5, pady=5, sticky=tk.W+tk.S)
			lblOrdenacao = tk.Label(content, text = "Ordenação:", font=("Verdana", 8, 'bold'))
			lblOrdenacao.grid(column=0, row=3, ipadx=5, pady=5, sticky=tk.W+tk.S)
			
			varEtrSigla = tk.StringVar()		
			etrSigla = tk.Entry(content, font = "Verdana 12", width=5, textvariable=varEtrSigla)
			etrSigla.grid(column=1, row=0, padx=10, pady=5, sticky=tk.N)			
			try:
				varEtrSigla.trace_add('write', to_uppercaseSigla)
			except AttributeError:
				varEtrSigla.trace('w', to_uppercaseSigla)
					
			etrInicial = tk.Entry(content, font = "Verdana 12", width=5)
			etrInicial.grid(column=1, row=1, padx=10, pady=5, sticky=tk.S)
			etrFinal = tk.Entry(content, font = "Verdana 12", width=5)
			etrFinal.grid(column=3, row=1, padx=10, pady=5, sticky=tk.S)			
			lblcor_v = tk.Label(content, bg="white", width=7)
			lblcor_v.grid(column=1, row=2)
			
			varEtrOrdenacao = tk.StringVar()
			etrOrdenacao = tk.Entry(content, font = "Verdana 12", width=5, textvariable=varEtrOrdenacao)
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
			
			botaoSair = Button(footer, image=v_cores_cdp_icon_img_5, relief=FLAT, command = combine_funcs(on_close_novo, t.destroy))
			botaoSair.grid(column=2, row=8)
			botaoSair.bind("<Enter>", on_enter_botaoSair)
			botaoSair.bind("<Leave>", on_leave_botaoSair)						
					
			statusbarrodape = tk.Label(status, text="", font=("Verdana", 10), anchor=tk.W)
			statusbarrodape.pack(side=tk.BOTTOM, fill=tk.X)
			t.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_novo, t.destroy))
			t.iconbitmap(default='transparent.ico')
			windowWidth, windowHeight = resolucao_width_cadastro, resolucao_height_cadastro
			positionRight = int(t.winfo_screenwidth()/2 - windowWidth/2)
			positionDown = int(t.winfo_screenheight()/2 - windowHeight/2)
			t.geometry("+{}+{}".format(positionRight, positionDown))
			t.attributes("-toolwindow", True)	
			if v_cores_cdp_modo == 'EDICAO':
				iniciaEdicao()
			if etrSigla['state'] == 'normal':
				etrSigla.focus()							
		def criacao():
			global selecionado
			global v_cores_cdp_modo
			
			selecionado = ()
			v_cores_cdp_modo = 'INCLUSAO'
			novo()
		def edicao(codigo, sigla, cor, inicial, final, ordenacao):
			global selecionado
			global v_cores_cdp_modo
			
			selecionado = (codigo, sigla, cor, inicial, final, ordenacao)
			
			if selecionado <> '':
				v_cores_cdp_modo = 'EDICAO'
				novo()			
		def popular_grid():
			global selecionado
			
			COORDS_LIST = []
			buttons_dict = {}
			
			columns = 7									
			query = "select CODIGO, SIGLA, COR, INICIAL, FINAL, ORDENACAO, (SELECT COUNT(SIGLA) FROM CORES_AG) AS LINHAS from CORES_AG ORDER BY ORDENACAO"
			cursor.execute(query)
			resultado = cursor.fetchall()
			sigla = ""
			cor = ""
			ordenacao = ""
			
			k = 0
									
			for i in resultado:
				k = k + 1
				for j in range(0, columns):
					coord = str(k)+"_"+str(j)
					COORDS_LIST.append(coord)
					
					try:
						widget = frame_buttons.grid_slaves(row=k, column=j)[0]
						widget.destroy()
					except:
						pass
						
					try:
						widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row=k, column=j)[0]
						widget.destroy()
					except:
						pass
					
					codigo = i[0]	
					sigla = i[1]
					cor  = i[2]
					inicial = i[3]
					final = i[4]
					ordenacao = i[5]
					linhas = i[6]
									
					if j == 5:						
						buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EDITAR', font=("Verdana", 8))
						buttons_dict[COORDS_LIST[-1]]["command"] = lambda vCodigo = codigo, vSigla = sigla, vCor = cor, vInicial = inicial, vFinal = final, vOrdenacao = ordenacao: edicao(vCodigo, vSigla, vCor, vInicial, vFinal, vOrdenacao)
						buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)
					elif j == 6:						
						buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EXCLUIR', font=("Verdana", 8))
						buttons_dict[COORDS_LIST[-1]]["command"] = lambda vCodigo = codigo, vLinhas = linhas + 1, vColunas = columns: exclui(vCodigo, vLinhas, vColunas)
						buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)						
					else:
						b = tk.Label(frame_buttons, anchor=W, text='', borderwidth=2, relief="groove")
						
						if j == 0:
							b['text'] = i[1]
							b['width'] = 10
						if j == 1:
							b['bg'] = i[2]							
							b['width'] = 15
						if j == 2:
							b['text'] = i[3]
							b['width'] = 9
						if j == 3:
							b['text'] = i[4]							
							b['width'] = 9
						if j == 4:
							b['text'] = i[5]
							b['width'] = 12
						b.grid(row=k, column=j, sticky='news')		
										
			# Update buttons frames idle tasks to let tkinter calculate buttons sizes
			frame_buttons.update_idletasks()
		def exclui(codigo, linhas, colunas):
			MsgBox = tk.messagebox.askquestion ('Excluir Cor','Deseja excluir esse registro?',icon = 'warning', parent = u)
			if MsgBox == 'yes':			
				for i in range(1, linhas):
					for j in range(0, colunas):
						try:						
							widget = frame_buttons.grid_slaves(row = i, column = j)[0]
							widget.destroy()							
						except:
							pass						
						
						try:							
							widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row = i, column = j)[0]
							widget.destroy()
						except:
							pass						
				
				Delete = "delete from CORES_AG where CODIGO='%s'" %(codigo)
				cursor.execute(Delete)
				con.commit()				
						
				popular_grid()														
		u = tk.Toplevel()
		u.grab_set()
		u.geometry(resolucao_tela_consulta2)
		u.title('Consulta Cores - Avaliação Genética')
		
		frame_top = tk.Frame(u)
		frame_top.grid(sticky='news', padx=1)
		
		frame_main = tk.Frame(u)
		frame_main.grid(sticky='news')
		
		label1 = tk.Label(frame_top, text="SIGLA", fg="black", font=("Verdana", 8, 'bold'), width=9, relief="groove", anchor=W)
		label1.grid(row=0, column=0)
	
		label3 = tk.Label(frame_top, text="COR", fg="black", font=("Verdana", 8, 'bold'), width=13, relief="groove", anchor=W)
		label3.grid(row=0, column=1)
		
		label4 = tk.Label(frame_top, text="ORDENAÇÃO", fg="black", font=("Verdana", 8, 'bold'), width=10, relief="groove", anchor=W)
		label4.grid(row=0, column=4)

		label5 = tk.Label(frame_top, text="INICIAL", fg="black", font=("Verdana", 8, 'bold'), width=8, relief="groove", anchor=W)
		label5.grid(row=0, column=2)
		
		label6 = tk.Label(frame_top, text="FINAL", fg="black", font=("Verdana", 8, 'bold'), width=8, relief="groove", anchor=W)
		label6.grid(row=0, column=3)	
	
		# Create a frame for the canvas with non-zero row&column weights
		frame_canvas = tk.Frame(frame_main)
		frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky='nw')
		frame_canvas.grid_rowconfigure(0, weight=1)
		frame_canvas.grid_columnconfigure(0, weight=1)
		# Set grid_propagate to False to allow 5-by-5 buttons resizing later
		frame_canvas.grid_propagate(False)
		
		# Add a canvas in that frame
		canvas = tk.Canvas(frame_canvas, bg = "#FFFFFF")
		canvas.grid(row=0, column=0, sticky="news")
		
		# Link a scrollbar to the canvas
		vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
		vsb.grid(row=0, column=1, sticky='ns')
		canvas.configure(yscrollcommand=vsb.set)
		
		# Create a frame to contain the buttons
		frame_buttons = tk.Frame(canvas, bg="#FFFFFF")
		canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
				
		popular_grid()
				
		# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
				
		frame_canvas.config(width=780, height=260)
		
		# Set the canvas scrolling region
		canvas.config(scrollregion=canvas.bbox("all"))
		
		frame_bottom = tk.Frame(u)
		frame_bottom.grid(sticky='news', padx=1)
		
		botaoNovo = tk.Button(frame_bottom, text='NOVO', font=("Verdana", 8), command=lambda : criacao())
		botaoNovo.grid(row=2, column=0)

		botaoFechar = tk.Button(frame_bottom, text='FECHAR', font=("Verdana", 8), command=lambda : on_close_cores_avaliacao_genetica())
		botaoFechar.grid(row=2, column=1)

		windowWidth, windowHeight = resolucao_width_consulta2, resolucao_height_consulta2
		positionRight = int(menuCor.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(menuCor.winfo_screenheight()/2 - windowHeight/2)
		u.geometry("+{}+{}".format(positionRight, positionDown))
		u.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_cores_avaliacao_genetica, u.destroy))
		u.attributes("-toolwindow", True)
	def cores_avaliacao_visual_bezerro():
		selecionado = {
		"sigla": "",
		"descrição": "",
		"cor": "",
		"ordenação": ""
			}
		def on_close_avaliacao_visual_bezerro():
			menuCor.grab_set()
			u.destroy()																		
		def novo():
			global selecionado
			global v_cores_cdp_modo
			def escolhe_cor():
				color_code = askcolor(parent = t, title = "Selecionar cor")
				lblcor_v['bg'] = color_code[1]
			def consiste():
				global v_cores_cdp_modo
												
				v_sigla = etrSigla.get()
				v_descricao = etrDescricao.get()
				v_ordenacao = etrOrdenacao.get()
				lblMensagem['fg'] = 'red'
				
				if v_cores_cdp_modo == 'INCLUSAO':
					if v_sigla == '':
						lblMensagem['text'] = '*PREENCHA A SIGLA'
						etrSigla.focus()
						t.after(5000, apaga_mensagem)
						return 0						
					if len(v_sigla) > 5:
						lblMensagem['text'] = '*A SIGLA DEVE TER NO MÁXIMO 5 CARACTERES'
						etrSigla.focus()
						t.after(5000, apaga_mensagem)
						return 0
					
					dbRollNo = ""
					Select="select SIGLA from CORES_AV where SIGLA='%s'" %(v_sigla)
					cursor.execute(Select)
					result = cursor.fetchall()
					for i in result:
						dbRollNo=i[0]
					if(v_sigla == dbRollNo):
						lblMensagem['text'] = '*REGISTRO JÁ EXISTE'
						etrSigla.focus()
						t.after(5000, apaga_mensagem)
						return 0
						
				if len(v_descricao) > 20:
					lblMensagem['text'] = '*A DESCRIÇÃO DEVE TER NO MÁXIMO 25 CARACTERES'
					etrDescricao.focus()
					t.after(5000, apaga_mensagem)
					return 0
				
				if v_ordenacao == '':
					lblMensagem['text'] = '*PREENCHA A ORDENACAO'
					etrOrdenacao.focus()
					t.after(5000, apaga_mensagem)
					return 0
					
				return 1
				
			def insere():
				global v_cores_cdp_modo			
				
				r = consiste()
				
				if bool(r):
					etrSigla['state'] = 'normal'
					
					if v_cores_cdp_modo == 'INCLUSAO':
						Insert=''' Insert into CORES_AV(SIGLA, DESCRICAO, COR, ORDENACAO) values(?,?,?,?) '''
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
						Update = "update CORES_AV set SIGLA='%s', DESCRICAO='%s', COR='%s', ORDENACAO='%s' where sigla='%s'" %(sigla, descricao, cor, ordenacao, sigla)
						cursor.execute(Update)
						con.commit()
						etrSigla.delete(0, tk.END)
						etrDescricao.delete(0, tk.END)
						lblcor_v['bg'] = 'white'
						etrOrdenacao.delete(0, tk.END)
						etrSigla.focus()
						v_cores_cdp_modo = 'INCLUSAO'
					combine_funcs(on_close_novo(), t.destroy())				
			def apaga_mensagem():
				lblMensagem['text'] = ''
			def on_close_novo():
				global v_cores_cdp_modo
				
				v_cores_cdp_modo = 'INCLUSAO'			
				popular_grid()
				u.grab_set()																						
			def limpa():
				global v_cores_cdp_modo
				
				etrSigla['state'] = 'normal'
				v_cores_cdp_modo = 'INCLUSAO'
				etrSigla.delete(0, tk.END)
				etrDescricao.delete(0, tk.END)
				lblcor_v['bg'] = '#FFFFFF'
				etrOrdenacao.delete(0, tk.END)
				etrSigla.focus()
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
			def on_enter_botaoSair(e):
				statusbarrodape['text'] = '                FECHAR'
			def on_leave_botaoSair(e):
				statusbarrodape['text'] = ''
			t = tk.Toplevel()
			t.grab_set()
			t.geometry(resolucao_tela_cadastro)
			t.title('Cores - Avaliação Visual Bezerro')
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
			
			botaoSair = Button(footer, image=v_cores_cdp_icon_img_5, relief=FLAT, command = combine_funcs(on_close_novo, t.destroy))
			botaoSair.grid(column=2, row=8)
			botaoSair.bind("<Enter>", on_enter_botaoSair)
			botaoSair.bind("<Leave>", on_leave_botaoSair)						
					
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
			if etrSigla['state'] == 'normal':
				etrSigla.focus()
				
			t.attributes("-toolwindow", True)			
		def criacao():
			global selecionado
			global v_cores_cdp_modo
			
			selecionado = ()
			v_cores_cdp_modo = 'INCLUSAO'
			novo()
		def edicao(sigla, descricao, cor, ordenacao):
			global selecionado
			global v_cores_cdp_modo
			
			selecionado = (sigla, descricao, cor, ordenacao)
			
			if selecionado <> '':
				v_cores_cdp_modo = 'EDICAO'
				novo()			
		def popular_grid():
			global selecionado
			
			COORDS_LIST = []
			buttons_dict = {}
			
			columns = 6									
			query = "select SIGLA, DESCRICAO, COR, ORDENACAO, (SELECT COUNT(SIGLA) FROM CORES_AV) AS LINHAS from CORES_AV ORDER BY ORDENACAO"
			cursor.execute(query)
			resultado = cursor.fetchall()
			sigla = ""
			descricao = ""
			cor = ""
			ordenacao = ""
			
			k = 0
									
			for i in resultado:
				k = k + 1
				for j in range(0, columns):
					coord = str(k)+"_"+str(j)
					COORDS_LIST.append(coord)
					
					try:
						widget = frame_buttons.grid_slaves(row=k, column=j)[0]
						widget.destroy()
					except:
						pass
						
					try:
						widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row=k, column=j)[0]
						widget.destroy()
					except:
						pass
						
					sigla = i[0]
					descricao = i[1]
					cor  = i[2]
					ordenacao = i[3]
					linhas = i[4]
									
					if j == 4:						
						buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EDITAR', font=("Verdana", 8))
						buttons_dict[COORDS_LIST[-1]]["command"] = lambda vSigla = sigla, vDescricao = descricao, vCor = cor, vOrdenacao = ordenacao: edicao(vSigla, vDescricao, vCor, vOrdenacao)
						buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)
					elif j == 5:						
						buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EXCLUIR', font=("Verdana", 8))
						buttons_dict[COORDS_LIST[-1]]["command"] = lambda vSigla = sigla, vLinhas = linhas + 1, vColunas = columns: exclui(vSigla, vLinhas, vColunas)
						buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)						
					else:
						b = tk.Label(frame_buttons, anchor=W, text='', borderwidth=2, relief="groove")
						
						if j == 0:
							b['text'] = i[0]
							b['width'] = 10
						if j == 1:
							b['text'] = i[1]
							b['width'] = 30
						if j == 2:
							b['bg'] = i[2]
							b['width'] = 15
						if j == 3:
							b['text'] = i[3]
							b['width'] = 11
						if j == 4:
							b['width'] = 10						
						b.grid(row=k, column=j, sticky='news')		
										
			# Update buttons frames idle tasks to let tkinter calculate buttons sizes
			frame_buttons.update_idletasks()
		def exclui(sigla, linhas, colunas):
			MsgBox = tk.messagebox.askquestion ('Excluir Cor','Deseja excluir esse registro?',icon = 'warning', parent = u)
			if MsgBox == 'yes':			
				for i in range(1, linhas):
					for j in range(0, colunas):
						try:						
							widget = frame_buttons.grid_slaves(row = i, column = j)[0]
							widget.destroy()							
						except:
							pass						
						
						try:							
							widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row = i, column = j)[0]
							widget.destroy()
						except:
							pass						
				
				Delete = "delete from CORES_AV where SIGLA='%s'" %(sigla)
				cursor.execute(Delete)
				con.commit()				
						
				popular_grid()														
		u = tk.Toplevel()
		u.grab_set()
		u.geometry(resolucao_tela_consulta)
		u.title('Consulta Cores - Cores Avaliação Visual Bezerro')
		
		frame_top = tk.Frame(u)
		frame_top.grid(sticky='news', padx=1)
		
		frame_main = tk.Frame(u)
		frame_main.grid(sticky='news')
		
		label1 = tk.Label(frame_top, text="SIGLA", fg="black", font=("Verdana", 8, 'bold'), width=9, relief="groove", anchor=W)
		label1.grid(row=0, column=0)
		
		label2 = tk.Label(frame_top, text="DESCRIÇÃO", fg="black", font=("Verdana", 8, 'bold'), width = 26, relief="groove", anchor=W)
		label2.grid(row=0, column=1)
		
		label3 = tk.Label(frame_top, text="COR", fg="black", font=("Verdana", 8, 'bold'), width=13, relief="groove", anchor=W)
		label3.grid(row=0, column=2)
		
		label4 = tk.Label(frame_top, text="ORDENAÇÃO", fg="black", font=("Verdana", 8, 'bold'), relief="groove", anchor=W)
		label4.grid(row=0, column=3)
	
		# Create a frame for the canvas with non-zero row&column weights
		frame_canvas = tk.Frame(frame_main)
		frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky='nw')
		frame_canvas.grid_rowconfigure(0, weight=1)
		frame_canvas.grid_columnconfigure(0, weight=1)
		# Set grid_propagate to False to allow 5-by-5 buttons resizing later
		frame_canvas.grid_propagate(False)
		
		# Add a canvas in that frame
		canvas = tk.Canvas(frame_canvas, bg = "#FFFFFF")
		canvas.grid(row=0, column=0, sticky="news")
		
		# Link a scrollbar to the canvas
		vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
		vsb.grid(row=0, column=1, sticky='ns')
		canvas.configure(yscrollcommand=vsb.set)
		
		# Create a frame to contain the buttons
		frame_buttons = tk.Frame(canvas, bg="#FFFFFF")
		canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
				
		popular_grid()
				
		# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
				
		frame_canvas.config(width=680, height=260)
		
		# Set the canvas scrolling region
		canvas.config(scrollregion=canvas.bbox("all"))
		
		frame_bottom = tk.Frame(u)
		frame_bottom.grid(sticky='news', padx=1)
		
		botaoNovo = tk.Button(frame_bottom, text='NOVO', font=("Verdana", 8), command=lambda : criacao())
		botaoNovo.grid(row=2, column=0)

		botaoFechar = tk.Button(frame_bottom, text='FECHAR', font=("Verdana", 8), command=lambda : on_close_avaliacao_visual_bezerro())
		botaoFechar.grid(row=2, column=1)

		windowWidth, windowHeight = resolucao_width_consulta, resolucao_height_consulta
		positionRight = int(menuCor.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(menuCor.winfo_screenheight()/2 - windowHeight/2)
		u.geometry("+{}+{}".format(positionRight, positionDown))
		u.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_avaliacao_visual_bezerro, u.destroy))			
		u.attributes("-toolwindow", True)
	def cores_acasalamento():
		selecionado = {
		"sigla": "",		
		"cor": "",
		"ordenação": ""
			}
		def on_close_acasalamento():
			menuCor.grab_set()
			u.destroy()																		
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
						etrSigla.focus()
						t.after(5000, apaga_mensagem)
						return 0						
					if len(v_sigla) > 1:
						lblMensagem['text'] = '*A SIGLA DEVE TER NO MÁXIMO 1 CARACTERE'
						etrSigla.focus()
						t.after(5000, apaga_mensagem)
						return 0
					if not v_sigla in ('1', '2', '3', 'D'):
						lblMensagem['text'] = '*A SIGLA DEVE SER (1, 2, 3, D)'
						etrSigla.focus()
						t.after(5000, apaga_mensagem)
						return 0				
					dbRollNo = ""
					Select="select SIGLA from CORES_ACASALAMENTO where SIGLA='%s'" %(v_sigla)
					cursor.execute(Select)
					result = cursor.fetchall()
					for i in result:
						dbRollNo=i[0]
					if(v_sigla == dbRollNo):
						lblMensagem['text'] = '*REGISTRO JÁ EXISTE'
						etrSigla.focus()
						t.after(5000, apaga_mensagem)
						return 0
										
				if v_ordenacao == '':
					lblMensagem['text'] = '*PREENCHA A ORDENACAO'
					etrOrdenacao.focus()
					t.after(5000, apaga_mensagem)
					return 0
					
				return 1
				
			def insere():
				global v_cores_cdp_modo			
				
				r = consiste()
				
				if bool(r):
					etrSigla['state'] = 'normal'
					
					if v_cores_cdp_modo == 'INCLUSAO':
						Insert=''' Insert into CORES_ACASALAMENTO(SIGLA, COR, ORDENACAO) values(?,?,?) '''
						Sigla = etrSigla.get()					
						Cor = lblcor_v['bg']
						Ordenacao = etrOrdenacao.get()
						Value=(Sigla, Cor, Ordenacao)
						cursor.execute(Insert, Value)
						con.commit()
						lblMensagem['fg'] = '#2D8C2B'
						lblMensagem['text'] = '*REGISTRO INCLUÍDO COM SUCESSO'
						etrSigla.delete(0, tk.END)
						lblcor_v['bg'] = 'white'
						etrOrdenacao.delete(0, tk.END)
						etrSigla.focus()
						t.after(4000, apaga_mensagem)						
					if v_cores_cdp_modo == 'EDICAO':
						sigla = etrSigla.get()
						cor = lblcor_v['bg']
						ordenacao = etrOrdenacao.get()
						Update = "update CORES_ACASALAMENTO set SIGLA='%s', COR='%s', ORDENACAO='%s' where sigla='%s'" %(sigla, cor, ordenacao, sigla)
						cursor.execute(Update)
						con.commit()
						etrSigla.delete(0, tk.END)
						lblcor_v['bg'] = 'white'
						etrOrdenacao.delete(0, tk.END)
						etrSigla.focus()
						v_cores_cdp_modo = 'INCLUSAO'
					combine_funcs(on_close_novo(), t.destroy())				
			def apaga_mensagem():
				lblMensagem['text'] = ''
			def on_close_novo():
				global v_cores_cdp_modo
				
				v_cores_cdp_modo = 'INCLUSAO'			
				popular_grid()
				u.grab_set()																						
			def limpa():
				global v_cores_cdp_modo
				
				etrSigla['state'] = 'normal'
				v_cores_cdp_modo = 'INCLUSAO'
				etrSigla.delete(0, tk.END)				
				lblcor_v['bg'] = '#FFFFFF'
				etrOrdenacao.delete(0, tk.END)
				etrSigla.focus()
			def iniciaEdicao():
				etrSigla['state'] = 'normal'
				etrSigla.delete(0, tk.END)
				etrSigla.insert(0, selecionado[0])
				etrSigla['state'] = 'disabled'
				lblcor_v['bg'] = selecionado[1]
				etrOrdenacao.delete(0, tk.END)
				etrOrdenacao.insert(0, selecionado[2])
			def to_uppercaseSigla(*args):
				varEtrSigla.set(varEtrSigla.get().upper())
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
			def on_enter_botaoSair(e):
				statusbarrodape['text'] = '                FECHAR'
			def on_leave_botaoSair(e):
				statusbarrodape['text'] = ''
			t = tk.Toplevel()
			t.grab_set()
			t.geometry(resolucao_tela_cadastro)
			t.title('Cores - Acasalamento')
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
			
			botaoSair = Button(footer, image=v_cores_cdp_icon_img_5, relief=FLAT, command = combine_funcs(on_close_novo, t.destroy))
			botaoSair.grid(column=2, row=8)
			botaoSair.bind("<Enter>", on_enter_botaoSair)
			botaoSair.bind("<Leave>", on_leave_botaoSair)						
					
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
			if etrSigla['state'] == 'normal':
				etrSigla.focus()
				
			t.attributes("-toolwindow", True)			
		def criacao():
			global selecionado
			global v_cores_cdp_modo
			
			selecionado = ()
			v_cores_cdp_modo = 'INCLUSAO'
			novo()
		def edicao(sigla, cor, ordenacao):
			global selecionado
			global v_cores_cdp_modo
			
			selecionado = (sigla, cor, ordenacao)
			
			if selecionado <> '':
				v_cores_cdp_modo = 'EDICAO'
				novo()			
		def popular_grid():
			global selecionado
			
			COORDS_LIST = []
			buttons_dict = {}
			
			columns = 5									
			query = "select SIGLA, COR, ORDENACAO, (SELECT COUNT(SIGLA) FROM CORES_ACASALAMENTO) AS LINHAS from CORES_ACASALAMENTO ORDER BY ORDENACAO"
			cursor.execute(query)
			resultado = cursor.fetchall()
			sigla = ""
			cor = ""
			ordenacao = ""
			
			k = 0
									
			for i in resultado:
				k = k + 1
				for j in range(0, columns):
					coord = str(k)+"_"+str(j)
					COORDS_LIST.append(coord)
					
					try:
						widget = frame_buttons.grid_slaves(row=k, column=j)[0]
						widget.destroy()
					except:
						pass
						
					try:
						widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row=k, column=j)[0]
						widget.destroy()
					except:
						pass
						
					sigla = i[0]
					cor  = i[1]
					ordenacao = i[2]
					linhas = i[3]
									
					if j == 3:						
						buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EDITAR', font=("Verdana", 8))
						buttons_dict[COORDS_LIST[-1]]["command"] = lambda vSigla = sigla, vCor = cor, vOrdenacao = ordenacao: edicao(vSigla, vCor, vOrdenacao)
						buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)
					elif j == 4:						
						buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EXCLUIR', font=("Verdana", 8))
						buttons_dict[COORDS_LIST[-1]]["command"] = lambda vSigla = sigla, vLinhas = linhas + 1, vColunas = columns: exclui(vSigla, vLinhas, vColunas)
						buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)						
					else:
						b = tk.Label(frame_buttons, anchor=W, text='', borderwidth=2, relief="groove")
						
						if j == 0:
							b['text'] = i[0]
							b['width'] = 10
						if j == 1:
							b['bg'] = i[1]
							b['width'] = 15
						if j == 2:
							b['text'] = i[2]
							b['width'] = 11					
						b.grid(row=k, column=j, sticky='news')		
										
			# Update buttons frames idle tasks to let tkinter calculate buttons sizes
			frame_buttons.update_idletasks()
		def exclui(sigla, linhas, colunas):
			MsgBox = tk.messagebox.askquestion ('Excluir Cor','Deseja excluir esse registro?',icon = 'warning', parent = u)
			if MsgBox == 'yes':			
				for i in range(1, linhas):
					for j in range(0, colunas):
						try:						
							widget = frame_buttons.grid_slaves(row = i, column = j)[0]
							widget.destroy()							
						except:
							pass						
						
						try:							
							widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row = i, column = j)[0]
							widget.destroy()
						except:
							pass						
				
				Delete = "delete from CORES_ACASALAMENTO where SIGLA='%s'" %(sigla)
				cursor.execute(Delete)
				con.commit()				
						
				popular_grid()														
		u = tk.Toplevel()
		u.grab_set()
		u.geometry(resolucao_tela_consulta)
		u.title('Consulta Cores - Cores Acasalamento')
		
		frame_top = tk.Frame(u)
		frame_top.grid(sticky='news', padx=1)
		
		frame_main = tk.Frame(u)
		frame_main.grid(sticky='news')
		
		label1 = tk.Label(frame_top, text="SIGLA", fg="black", font=("Verdana", 8, 'bold'), width=9, relief="groove", anchor=W)
		label1.grid(row=0, column=0)
	
		label3 = tk.Label(frame_top, text="COR", fg="black", font=("Verdana", 8, 'bold'), width=13, relief="groove", anchor=W)
		label3.grid(row=0, column=1)
		
		label4 = tk.Label(frame_top, text="ORDENAÇÃO", fg="black", font=("Verdana", 8, 'bold'), relief="groove", anchor=W)
		label4.grid(row=0, column=2)
	
		# Create a frame for the canvas with non-zero row&column weights
		frame_canvas = tk.Frame(frame_main)
		frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky='nw')
		frame_canvas.grid_rowconfigure(0, weight=1)
		frame_canvas.grid_columnconfigure(0, weight=1)
		# Set grid_propagate to False to allow 5-by-5 buttons resizing later
		frame_canvas.grid_propagate(False)
		
		# Add a canvas in that frame
		canvas = tk.Canvas(frame_canvas, bg = "#FFFFFF")
		canvas.grid(row=0, column=0, sticky="news")
		
		# Link a scrollbar to the canvas
		vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
		vsb.grid(row=0, column=1, sticky='ns')
		canvas.configure(yscrollcommand=vsb.set)
		
		# Create a frame to contain the buttons
		frame_buttons = tk.Frame(canvas, bg="#FFFFFF")
		canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
				
		popular_grid()
				
		# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
				
		frame_canvas.config(width=680, height=260)
		
		# Set the canvas scrolling region
		canvas.config(scrollregion=canvas.bbox("all"))
		
		frame_bottom = tk.Frame(u)
		frame_bottom.grid(sticky='news', padx=1)
		
		botaoNovo = tk.Button(frame_bottom, text='NOVO', font=("Verdana", 8), command=lambda : criacao())
		botaoNovo.grid(row=2, column=0)

		botaoFechar = tk.Button(frame_bottom, text='FECHAR', font=("Verdana", 8), command=lambda : on_close_acasalamento())
		botaoFechar.grid(row=2, column=1)

		windowWidth, windowHeight = resolucao_width_consulta, resolucao_height_consulta
		positionRight = int(menuCor.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(menuCor.winfo_screenheight()/2 - windowHeight/2)
		u.geometry("+{}+{}".format(positionRight, positionDown))
		u.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_acasalamento, u.destroy))			
		u.attributes("-toolwindow", True)
	def cores_cabecalho():
		def escolhe_cor():
			color_code = askcolor(parent = t, title = "Selecionar cor")
			lblcor_v['bg'] = color_code[1]
		def on_enter_botaoIncluir(e):
			statusbarrodape['text'] = 'SALVAR'
		def on_leave_botaoIncluir(e):
			statusbarrodape['text'] = ''
		def on_enter_botaoSair(e):
			statusbarrodape['text'] = '      FECHAR'
		def on_leave_botaoSair(e):
			statusbarrodape['text'] = ''			
		def insere():
			print('insere')
		def on_close_cabecalho():
			menuCor.grab_set()
		t = tk.Toplevel()
		t.grab_set()
		t.geometry(resolucao_tela_cadastro)
		t.title('Cor - Cabeçalho')
		content = tk.Frame(t)
		messageBar = tk.Frame(t, height=30)
		footer = tk.Frame(t, height=30)
		status = tk.Frame(t, height=30)
		content.pack(fill='both')
		messageBar.pack(fill='both')
		footer.pack(fill='both', side='bottom')
		status.pack(fill='both', side = 'bottom')
		statusbarrodape = tk.Label(status, text="", font=("Verdana", 10), anchor=tk.W)
		statusbarrodape.pack(side=tk.BOTTOM, fill=tk.X)		
		lblcorfundo = tk.Label(content, text = "Cor do fundo:", font=("Verdana", 8, 'bold'))
		lblcorfundo.grid(column=0, row=0, ipadx=5, pady=5, sticky=tk.W+tk.S)
		lblcor_v_fundo = tk.Label(content, bg="white", width=28)
		lblcor_v_fundo.grid(column=1, row=0)
		btncor_fundo = Button(content, image=v_cores_cdp_icon_img_1, relief=FLAT, command=escolhe_cor)
		btncor_fundo.grid(column=2, row=0, padx=5, pady=5, sticky=tk.S)
		lblcorletra = tk.Label(content, text = "Cor da letra:", font=("Verdana", 8, 'bold'))
		lblcorletra.grid(column=0, row=1, ipadx=5, pady=5, sticky=tk.W+tk.S)
		lblcor_v_letra = tk.Label(content, bg="white", width=28)
		lblcor_v_letra.grid(column=1, row=1)
		btncorletra = Button(content, image=v_cores_cdp_icon_img_1, relief=FLAT, command=escolhe_cor)
		btncorletra.grid(column=2, row=1, padx=5, pady=5, sticky=tk.S)		
		botaoIncluir = Button(footer, image=v_cores_cdp_icon_img_2, relief=FLAT, command=insere)
		botaoIncluir.grid(column=0, row=8)
		botaoIncluir.bind("<Enter>", on_enter_botaoIncluir)
		botaoIncluir.bind("<Leave>", on_leave_botaoIncluir)
		botaoSair = Button(footer, image=v_cores_cdp_icon_img_5, relief=FLAT, command = combine_funcs(on_close_cabecalho, t.destroy))
		botaoSair.grid(column=2, row=8)
		botaoSair.bind("<Enter>", on_enter_botaoSair)
		botaoSair.bind("<Leave>", on_leave_botaoSair)		
		t.iconbitmap(default='transparent.ico')
		windowWidth, windowHeight = resolucao_width_cadastro, resolucao_height_cadastro
		positionRight = int(menuCor.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(menuCor.winfo_screenheight()/2 - windowHeight/2)
		t.geometry("+{}+{}".format(positionRight, positionDown))
		t.attributes("-toolwindow", True)		
	menuCor = tk.Toplevel()
	menuCor.grab_set()
	menuCor.geometry(resolucao_tela)
	menuCor.title('Cores - Parametrização')
	Button(menuCor, text='Cores - CDP', command=cores_cdp, width = 60).pack(padx=7, pady=7)
	Button(menuCor, text='Cores - Avaliação Fenotípica', command=cores_avaliacao_fenotipica, width = 60).pack(padx=7, pady=7)
	Button(menuCor, text='Cores - Produtividade', command=cores_produtividade, width = 60).pack(padx=7, pady=7)
	Button(menuCor, text='Cores - Avaliação Genética', command=cores_avaliacao_genetica, width = 60).pack(padx=7, pady=7)
	Button(menuCor, text='Cores - Avaliação Visual - Bezerro', command=cores_avaliacao_visual_bezerro, width = 60).pack(padx=7, pady=7)
	Button(menuCor, text='Cores - Acasalamentos', command=cores_acasalamento, width = 60).pack(padx=7, pady=7)
	Button(menuCor, text='Cores - Cabeçalhos - Relatórios', command=cores_cabecalho, width = 60).pack(padx=7, pady=7)
	Button(menuCor, text='FECHAR', command=combine_funcs(on_close, menuCor.destroy)).pack(padx=7, pady=7)
	menuCor.protocol("WM_DELETE_WINDOW", combine_funcs(on_close, menuCor.destroy))
	menuCor.iconbitmap(default='transparent.ico')
	windowWidth, windowHeight = resolucao_width, resolucao_height
	positionRight = int(menuCor.winfo_screenwidth()/2 - windowWidth/2)
	positionDown = int(menuCor.winfo_screenheight()/2 - windowHeight/2)
	menuCor.geometry("+{}+{}".format(positionRight, positionDown))	
	menuCor.attributes("-toolwindow", True)
	formulario.attributes("-topmost", False)
	menuCor.attributes("-topmost", True)
	menuCor.attributes("-topmost", False)

def situacoes_bezerros():
	selecionado = {
	"sigla": "",
	"descrição": ""
		}
	def on_close_avaliacao_visual_bezerro():
		formulario.grab_set()
		u.destroy()																		
	def novo():
		global selecionado
		global v_cores_cdp_modo
		def consiste():
			global v_cores_cdp_modo
											
			v_sigla = etrSigla.get()
			v_descricao = etrDescricao.get()
			
			if v_cores_cdp_modo == 'INCLUSAO':
				if v_sigla == '':
					lblMensagem['text'] = '*PREENCHA A SIGLA'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)
					return 0						
				if len(v_sigla) > 5:
					lblMensagem['text'] = '*A SIGLA DEVE TER NO MÁXIMO 5 CARACTERES'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)
					return 0
				
				dbRollNo = ""
				Select="select SIGLA from SITUACOESBEZERRO where SIGLA='%s'" %(v_sigla)
				cursor.execute(Select)
				result = cursor.fetchall()
				for i in result:
					dbRollNo=i[0]
				if(v_sigla == dbRollNo):
					lblMensagem['text'] = '*REGISTRO JÁ EXISTE'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)
					return 0
					
			if len(v_descricao) > 20:
				lblMensagem['text'] = '*A DESCRIÇÃO DEVE TER NO MÁXIMO 25 CARACTERES'
				etrDescricao.focus()
				t.after(5000, apaga_mensagem)
				return 0
								
			return 1
			
		def insere():
			global v_cores_cdp_modo			
			
			r = consiste()
			
			if bool(r):
				etrSigla['state'] = 'normal'
				
				if v_cores_cdp_modo == 'INCLUSAO':
					Insert=''' Insert into SITUACOESBEZERRO(SIGLA, DESCRICAO) values(?,?) '''
					Sigla = etrSigla.get()
					Descricao = etrDescricao.get()
					Value=(Sigla, Descricao)
					cursor.execute(Insert, Value)
					con.commit()
					lblMensagem['fg'] = '#2D8C2B'
					lblMensagem['text'] = '*REGISTRO INCLUÍDO COM SUCESSO'
					etrSigla.delete(0, tk.END)
					etrDescricao.delete(0, tk.END)
					etrSigla.focus()
					t.after(4000, apaga_mensagem)						
				if v_cores_cdp_modo == 'EDICAO':
					sigla = etrSigla.get()
					descricao = etrDescricao.get()
					Update = "update SITUACOESBEZERRO set SIGLA='%s', DESCRICAO='%s' where sigla='%s'" %(sigla, descricao, sigla)
					cursor.execute(Update)
					con.commit()
					etrSigla.delete(0, tk.END)
					etrDescricao.delete(0, tk.END)
					etrSigla.focus()
					v_cores_cdp_modo = 'INCLUSAO'
				combine_funcs(on_close_novo(), t.destroy())				
		def apaga_mensagem():
			lblMensagem['text'] = ''
		def on_close_novo():
			global v_cores_cdp_modo
			
			v_cores_cdp_modo = 'INCLUSAO'			
			popular_grid()
			u.grab_set()																						
		def limpa():
			global v_cores_cdp_modo
			
			etrSigla['state'] = 'normal'
			v_cores_cdp_modo = 'INCLUSAO'
			etrSigla.delete(0, tk.END)
			etrDescricao.delete(0, tk.END)
			etrSigla.focus()
		def iniciaEdicao():
			etrSigla['state'] = 'normal'
			etrSigla.delete(0, tk.END)
			etrSigla.insert(0, selecionado[0])
			etrSigla['state'] = 'disabled'
			etrDescricao.delete(0, tk.END)
			etrDescricao.insert(0, selecionado[1])
		def to_uppercaseSigla(*args):
			varEtrSigla.set(varEtrSigla.get().upper())
		def to_uppercaseDescricao(*args):
			varEtrDescricao.set(varEtrDescricao.get().upper())
		def on_enter_botaoIncluir(e):
			statusbarrodape['text'] = 'SALVAR'
		def on_leave_botaoIncluir(e):
			statusbarrodape['text'] = ''
		def on_enter_botaoLimpar(e):
			statusbarrodape['text'] = '        LIMPAR'
		def on_leave_botaoLimpar(e):
			statusbarrodape['text'] = ''
		def on_enter_botaoSair(e):
			statusbarrodape['text'] = '                FECHAR'
		def on_leave_botaoSair(e):
			statusbarrodape['text'] = ''
		t = tk.Toplevel()
		t.grab_set()
		t.geometry(resolucao_tela_cadastro)
		t.title('Situações de Bezerros')
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
		
		botaoSair = Button(footer, image=v_cores_cdp_icon_img_5, relief=FLAT, command = combine_funcs(on_close_novo, t.destroy))
		botaoSair.grid(column=2, row=8)
		botaoSair.bind("<Enter>", on_enter_botaoSair)
		botaoSair.bind("<Leave>", on_leave_botaoSair)						
				
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
		if etrSigla['state'] == 'normal':
			etrSigla.focus()
			
		t.attributes("-toolwindow", True)			
	def criacao():
		global selecionado
		global v_cores_cdp_modo
		
		selecionado = ()
		v_cores_cdp_modo = 'INCLUSAO'
		novo()
	def edicao(sigla, descricao):
		global selecionado
		global v_cores_cdp_modo
		
		selecionado = (sigla, descricao)
		
		if selecionado <> '':
			v_cores_cdp_modo = 'EDICAO'
			novo()			
	def popular_grid():
		global selecionado
		
		COORDS_LIST = []
		buttons_dict = {}
		
		columns = 4									
		query = "select SIGLA, DESCRICAO, (SELECT COUNT(SIGLA) FROM SITUACOESBEZERRO) AS LINHAS from SITUACOESBEZERRO"
		cursor.execute(query)
		resultado = cursor.fetchall()
		sigla = ""
		descricao = ""
		
		k = 0
								
		for i in resultado:
			k = k + 1
			for j in range(0, columns):
				coord = str(k)+"_"+str(j)
				COORDS_LIST.append(coord)
				
				try:
					widget = frame_buttons.grid_slaves(row=k, column=j)[0]
					widget.destroy()
				except:
					pass
					
				try:
					widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row=k, column=j)[0]
					widget.destroy()
				except:
					pass
					
				sigla = i[0]
				descricao = i[1]
				linhas = i[2]
								
				if j == 2:						
					buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EDITAR', font=("Verdana", 8))
					buttons_dict[COORDS_LIST[-1]]["command"] = lambda vSigla = sigla, vDescricao = descricao: edicao(vSigla, vDescricao)
					buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)
				elif j == 3:						
					buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EXCLUIR', font=("Verdana", 8))
					buttons_dict[COORDS_LIST[-1]]["command"] = lambda vSigla = sigla, vLinhas = linhas + 1, vColunas = columns: exclui(vSigla, vLinhas, vColunas)
					buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)						
				else:
					b = tk.Label(frame_buttons, anchor=W, text='', borderwidth=2, relief="groove")
					
					if j == 0:
						b['text'] = i[0]
						b['width'] = 10
					if j == 1:
						b['text'] = i[1]
						b['width'] = 30						
					b.grid(row=k, column=j, sticky='news')		
									
		# Update buttons frames idle tasks to let tkinter calculate buttons sizes
		frame_buttons.update_idletasks()
	def exclui(sigla, linhas, colunas):
		MsgBox = tk.messagebox.askquestion ('Excluir Cor','Deseja excluir esse registro?',icon = 'warning', parent = u)
		if MsgBox == 'yes':			
			for i in range(1, linhas):
				for j in range(0, colunas):
					try:						
						widget = frame_buttons.grid_slaves(row = i, column = j)[0]
						widget.destroy()							
					except:
						pass						
					
					try:							
						widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row = i, column = j)[0]
						widget.destroy()
					except:
						pass						
			
			Delete = "delete from SITUACOESBEZERRO where SIGLA='%s'" %(sigla)
			cursor.execute(Delete)
			con.commit()				
					
			popular_grid()														
	u = tk.Toplevel()
	u.grab_set()
	u.geometry(resolucao_tela_consulta)
	u.title('Situações de Bezerros')
	
	frame_top = tk.Frame(u)
	frame_top.grid(sticky='news', padx=1)
	
	frame_main = tk.Frame(u)
	frame_main.grid(sticky='news')
	
	label1 = tk.Label(frame_top, text="SIGLA", fg="black", font=("Verdana", 8, 'bold'), width=9, relief="groove", anchor=W)
	label1.grid(row=0, column=0)
	
	label2 = tk.Label(frame_top, text="DESCRIÇÃO", fg="black", font=("Verdana", 8, 'bold'), width = 26, relief="groove", anchor=W)
	label2.grid(row=0, column=1)
		
	# Create a frame for the canvas with non-zero row&column weights
	frame_canvas = tk.Frame(frame_main)
	frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky='nw')
	frame_canvas.grid_rowconfigure(0, weight=1)
	frame_canvas.grid_columnconfigure(0, weight=1)
	# Set grid_propagate to False to allow 5-by-5 buttons resizing later
	frame_canvas.grid_propagate(False)
	
	# Add a canvas in that frame
	canvas = tk.Canvas(frame_canvas, bg = "#FFFFFF")
	canvas.grid(row=0, column=0, sticky="news")
	
	# Link a scrollbar to the canvas
	vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
	vsb.grid(row=0, column=1, sticky='ns')
	canvas.configure(yscrollcommand=vsb.set)
	
	# Create a frame to contain the buttons
	frame_buttons = tk.Frame(canvas, bg="#FFFFFF")
	canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
			
	popular_grid()
			
	# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
			
	frame_canvas.config(width=680, height=260)
	
	# Set the canvas scrolling region
	canvas.config(scrollregion=canvas.bbox("all"))
	
	frame_bottom = tk.Frame(u)
	frame_bottom.grid(sticky='news', padx=1)
	
	botaoNovo = tk.Button(frame_bottom, text='NOVO', font=("Verdana", 8), command=lambda : criacao())
	botaoNovo.grid(row=2, column=0)

	botaoFechar = tk.Button(frame_bottom, text='FECHAR', font=("Verdana", 8), command=lambda : on_close_avaliacao_visual_bezerro())
	botaoFechar.grid(row=2, column=1)

	windowWidth, windowHeight = resolucao_width_consulta, resolucao_height_consulta
	positionRight = int(formulario.winfo_screenwidth()/2 - windowWidth/2)
	positionDown = int(formulario.winfo_screenheight()/2 - windowHeight/2)
	u.geometry("+{}+{}".format(positionRight, positionDown))
	u.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_avaliacao_visual_bezerro, u.destroy))			
	u.attributes("-toolwindow", True)	

def causas():
	selecionado = {
	"sigla": "",
	"descrição": ""
		}
	def on_close_avaliacao_visual_bezerro():
		formulario.grab_set()
		u.destroy()																		
	def novo():
		global selecionado
		global v_cores_cdp_modo
		def consiste():
			global v_cores_cdp_modo
											
			v_sigla = etrSigla.get()
			v_descricao = etrDescricao.get()
			
			if v_cores_cdp_modo == 'INCLUSAO':
				if v_sigla == '':
					lblMensagem['text'] = '*PREENCHA A SIGLA'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)
					return 0						
				if len(v_sigla) > 3:
					lblMensagem['text'] = '*A SIGLA DEVE TER NO MÁXIMO 3 CARACTERES'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)
					return 0
				
				dbRollNo = ""
				Select="select SIGLA from CAUSASDESCARTE where SIGLA='%s'" %(v_sigla)
				cursor.execute(Select)
				result = cursor.fetchall()
				for i in result:
					dbRollNo=i[0]
				if(v_sigla == dbRollNo):
					lblMensagem['text'] = '*REGISTRO JÁ EXISTE'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)
					return 0
					
			if len(v_descricao) > 20:
				lblMensagem['text'] = '*A DESCRIÇÃO DEVE TER NO MÁXIMO 25 CARACTERES'
				etrDescricao.focus()
				t.after(5000, apaga_mensagem)
				return 0
								
			return 1
			
		def insere():
			global v_cores_cdp_modo			
			
			r = consiste()
			
			if bool(r):
				etrSigla['state'] = 'normal'
				
				if v_cores_cdp_modo == 'INCLUSAO':
					Insert=''' Insert into CAUSASDESCARTE(SIGLA, DESCRICAO) values(?,?) '''
					Sigla = etrSigla.get()
					Descricao = etrDescricao.get()
					Value=(Sigla, Descricao)
					cursor.execute(Insert, Value)
					con.commit()						
				if v_cores_cdp_modo == 'EDICAO':
					sigla = etrSigla.get()
					descricao = etrDescricao.get()
					Update = "update CAUSASDESCARTE set SIGLA='%s', DESCRICAO='%s' where sigla='%s'" %(sigla, descricao, sigla)
					cursor.execute(Update)
					con.commit()
					etrSigla.delete(0, tk.END)
					etrDescricao.delete(0, tk.END)
					etrSigla.focus()
					v_cores_cdp_modo = 'INCLUSAO'
				combine_funcs(on_close_novo(), t.destroy())				
		def apaga_mensagem():
			lblMensagem['text'] = ''
		def on_close_novo():
			global v_cores_cdp_modo
			
			v_cores_cdp_modo = 'INCLUSAO'			
			popular_grid()
			u.grab_set()																						
		def limpa():
			global v_cores_cdp_modo
			
			etrSigla['state'] = 'normal'
			v_cores_cdp_modo = 'INCLUSAO'
			etrSigla.delete(0, tk.END)
			etrDescricao.delete(0, tk.END)
			etrSigla.focus()
		def iniciaEdicao():
			etrSigla['state'] = 'normal'
			etrSigla.delete(0, tk.END)
			etrSigla.insert(0, selecionado[0])
			etrSigla['state'] = 'disabled'
			etrDescricao.delete(0, tk.END)
			etrDescricao.insert(0, selecionado[1])
		def to_uppercaseSigla(*args):
			varEtrSigla.set(varEtrSigla.get().upper())
		def to_uppercaseDescricao(*args):
			varEtrDescricao.set(varEtrDescricao.get().upper())
		def on_enter_botaoIncluir(e):
			statusbarrodape['text'] = 'SALVAR'
		def on_leave_botaoIncluir(e):
			statusbarrodape['text'] = ''
		def on_enter_botaoLimpar(e):
			statusbarrodape['text'] = '        LIMPAR'
		def on_leave_botaoLimpar(e):
			statusbarrodape['text'] = ''
		def on_enter_botaoSair(e):
			statusbarrodape['text'] = '                FECHAR'
		def on_leave_botaoSair(e):
			statusbarrodape['text'] = ''
		t = tk.Toplevel()
		t.grab_set()
		t.geometry(resolucao_tela_cadastro)
		t.title('Observações - Causas')
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
		
		botaoSair = Button(footer, image=v_cores_cdp_icon_img_5, relief=FLAT, command = combine_funcs(on_close_novo, t.destroy))
		botaoSair.grid(column=2, row=8)
		botaoSair.bind("<Enter>", on_enter_botaoSair)
		botaoSair.bind("<Leave>", on_leave_botaoSair)						
				
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
		if etrSigla['state'] == 'normal':
			etrSigla.focus()
			
		t.attributes("-toolwindow", True)			
	def criacao():
		global selecionado
		global v_cores_cdp_modo
		
		selecionado = ()
		v_cores_cdp_modo = 'INCLUSAO'
		novo()
	def edicao(sigla, descricao):
		global selecionado
		global v_cores_cdp_modo
		
		selecionado = (sigla, descricao)
		
		if selecionado <> '':
			v_cores_cdp_modo = 'EDICAO'
			novo()			
	def popular_grid():
		global selecionado
		
		COORDS_LIST = []
		buttons_dict = {}
		
		columns = 4									
		query = "select SIGLA, DESCRICAO, (SELECT COUNT(SIGLA) FROM CAUSASDESCARTE) AS LINHAS from CAUSASDESCARTE"
		cursor.execute(query)
		resultado = cursor.fetchall()
		sigla = ""
		descricao = ""
		
		k = 0
								
		for i in resultado:
			k = k + 1
			for j in range(0, columns):
				coord = str(k)+"_"+str(j)
				COORDS_LIST.append(coord)
				
				try:
					widget = frame_buttons.grid_slaves(row=k, column=j)[0]
					widget.destroy()
				except:
					pass
					
				try:
					widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row=k, column=j)[0]
					widget.destroy()
				except:
					pass
					
				sigla = i[0]
				descricao = i[1]
				linhas = i[2]
								
				if j == 2:						
					buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EDITAR', font=("Verdana", 8))
					buttons_dict[COORDS_LIST[-1]]["command"] = lambda vSigla = sigla, vDescricao = descricao: edicao(vSigla, vDescricao)
					buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)
				elif j == 3:						
					buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EXCLUIR', font=("Verdana", 8))
					buttons_dict[COORDS_LIST[-1]]["command"] = lambda vSigla = sigla, vLinhas = linhas + 1, vColunas = columns: exclui(vSigla, vLinhas, vColunas)
					buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)						
				else:
					b = tk.Label(frame_buttons, anchor=W, text='', borderwidth=2, relief="groove")
					
					if j == 0:
						b['text'] = i[0]
						b['width'] = 10
					if j == 1:
						b['text'] = i[1]
						b['width'] = 30						
					b.grid(row=k, column=j, sticky='news')		
									
		# Update buttons frames idle tasks to let tkinter calculate buttons sizes
		frame_buttons.update_idletasks()
	def exclui(sigla, linhas, colunas):
		MsgBox = tk.messagebox.askquestion ('Excluir Cor','Deseja excluir esse registro?',icon = 'warning', parent = u)
		if MsgBox == 'yes':			
			for i in range(1, linhas):
				for j in range(0, colunas):
					try:						
						widget = frame_buttons.grid_slaves(row = i, column = j)[0]
						widget.destroy()							
					except:
						pass						
					
					try:							
						widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row = i, column = j)[0]
						widget.destroy()
					except:
						pass						
			
			Delete = "delete from CAUSASDESCARTE where SIGLA='%s'" %(sigla)
			cursor.execute(Delete)
			con.commit()				
					
			popular_grid()														
	u = tk.Toplevel()
	u.grab_set()
	u.geometry(resolucao_tela_consulta)
	u.title('Observações - Causas')
	
	frame_top = tk.Frame(u)
	frame_top.grid(sticky='news', padx=1)
	
	frame_main = tk.Frame(u)
	frame_main.grid(sticky='news')
	
	label1 = tk.Label(frame_top, text="SIGLA", fg="black", font=("Verdana", 8, 'bold'), width=9, relief="groove", anchor=W)
	label1.grid(row=0, column=0)
	
	label2 = tk.Label(frame_top, text="DESCRIÇÃO", fg="black", font=("Verdana", 8, 'bold'), width = 26, relief="groove", anchor=W)
	label2.grid(row=0, column=1)
		
	# Create a frame for the canvas with non-zero row&column weights
	frame_canvas = tk.Frame(frame_main)
	frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky='nw')
	frame_canvas.grid_rowconfigure(0, weight=1)
	frame_canvas.grid_columnconfigure(0, weight=1)
	# Set grid_propagate to False to allow 5-by-5 buttons resizing later
	frame_canvas.grid_propagate(False)
	
	# Add a canvas in that frame
	canvas = tk.Canvas(frame_canvas, bg = "#FFFFFF")
	canvas.grid(row=0, column=0, sticky="news")
	
	# Link a scrollbar to the canvas
	vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
	vsb.grid(row=0, column=1, sticky='ns')
	canvas.configure(yscrollcommand=vsb.set)
	
	# Create a frame to contain the buttons
	frame_buttons = tk.Frame(canvas, bg="#FFFFFF")
	canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
			
	popular_grid()
			
	# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
			
	frame_canvas.config(width=680, height=260)
	
	# Set the canvas scrolling region
	canvas.config(scrollregion=canvas.bbox("all"))
	
	frame_bottom = tk.Frame(u)
	frame_bottom.grid(sticky='news', padx=1)
	
	botaoNovo = tk.Button(frame_bottom, text='NOVO', font=("Verdana", 8), command=lambda : criacao())
	botaoNovo.grid(row=2, column=0)

	botaoFechar = tk.Button(frame_bottom, text='FECHAR', font=("Verdana", 8), command=lambda : on_close_avaliacao_visual_bezerro())
	botaoFechar.grid(row=2, column=1)

	windowWidth, windowHeight = resolucao_width_consulta, resolucao_height_consulta
	positionRight = int(formulario.winfo_screenwidth()/2 - windowWidth/2)
	positionDown = int(formulario.winfo_screenheight()/2 - windowHeight/2)
	u.geometry("+{}+{}".format(positionRight, positionDown))
	u.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_avaliacao_visual_bezerro, u.destroy))			
	u.attributes("-toolwindow", True)

def situacoes_matrizes():
	selecionado = {
	"sigla": "",
	"descrição": "",
	"cor": "",
	"ordenação": ""
		}
	def on_close_cores_cdp():
		formulario.grab_set()
		u.destroy()																		
	def novo():
		global selecionado
		global v_cores_cdp_modo
		def escolhe_cor():
			color_code = askcolor(parent = t, title = "Selecionar cor")
			lblcor_v['bg'] = color_code[1]
		def consiste():
			global v_cores_cdp_modo
											
			v_sigla = etrSigla.get()
			v_descricao = etrDescricao.get()
			v_ordenacao = etrOrdenacao.get()
			lblMensagem['fg'] = 'red'
			
			if v_cores_cdp_modo == 'INCLUSAO':
				if v_sigla == '':
					lblMensagem['text'] = '*PREENCHA A SIGLA'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)
					return 0						
				if len(v_sigla) > 1:
					lblMensagem['text'] = '*A SIGLA DEVE TER APENAS UM CARACTERE'
					etrSigla.focus()
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
					etrSigla.focus()
					t.after(5000, apaga_mensagem)
					return 0
					
			if len(v_descricao) > 20:
				lblMensagem['text'] = '*A DESCRIÇÃO DEVE TER NO MÁXIMO 20 CARACTERES'
				etrDescricao.focus()
				t.after(5000, apaga_mensagem)
				return 0
			
			if v_ordenacao == '':
				lblMensagem['text'] = '*PREENCHA A ORDENACAO'
				etrOrdenacao.focus()
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
					etrSigla.delete(0, tk.END)
					etrDescricao.delete(0, tk.END)
					lblcor_v['bg'] = 'white'
					etrOrdenacao.delete(0, tk.END)
					etrSigla.focus()
					v_cores_cdp_modo = 'INCLUSAO'
				combine_funcs(on_close_novo(), t.destroy())				
		def apaga_mensagem():
			lblMensagem['text'] = ''
		def on_close_novo():
			global v_cores_cdp_modo
			
			v_cores_cdp_modo = 'INCLUSAO'			
			popular_grid()
			u.grab_set()																						
		def limpa():
			global v_cores_cdp_modo
			
			etrSigla['state'] = 'normal'
			v_cores_cdp_modo = 'INCLUSAO'
			etrSigla.delete(0, tk.END)
			etrDescricao.delete(0, tk.END)
			lblcor_v['bg'] = '#FFFFFF'
			etrOrdenacao.delete(0, tk.END)
			etrSigla.focus()
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
		def on_enter_botaoSair(e):
			statusbarrodape['text'] = '                FECHAR'
		def on_leave_botaoSair(e):
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
		
		botaoSair = Button(footer, image=v_cores_cdp_icon_img_5, relief=FLAT, command = combine_funcs(on_close_novo, t.destroy))
		botaoSair.grid(column=2, row=8)
		botaoSair.bind("<Enter>", on_enter_botaoSair)
		botaoSair.bind("<Leave>", on_leave_botaoSair)						
				
		statusbarrodape = tk.Label(status, text="", font=("Verdana", 10), anchor=tk.W)
		statusbarrodape.pack(side=tk.BOTTOM, fill=tk.X)
		t.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_novo, t.destroy))
		t.iconbitmap(default='transparent.ico')
		windowWidth, windowHeight = resolucao_width_cadastro, resolucao_height_cadastro
		positionRight = int(formulario.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(formulario.winfo_screenheight()/2 - windowHeight/2)
		t.geometry("+{}+{}".format(positionRight, positionDown))			
		if v_cores_cdp_modo == 'EDICAO':
			iniciaEdicao()
		if etrSigla['state'] == 'normal':
			etrSigla.focus()
			
		t.attributes("-toolwindow", True)
		t.attributes("-topmost", True)
		t.attributes("-topmost", False)
	def criacao():
		global selecionado
		global v_cores_cdp_modo
		
		selecionado = ()
		v_cores_cdp_modo = 'INCLUSAO'
		novo()
	def edicao(sigla, descricao, cor, ordenacao):
		global selecionado
		global v_cores_cdp_modo
		
		selecionado = (sigla, descricao, cor, ordenacao)
		
		if selecionado <> '':
			v_cores_cdp_modo = 'EDICAO'
			novo()			
	def popular_grid():
		global selecionado
		
		COORDS_LIST = []
		buttons_dict = {}
		
		columns = 6									
		query = "select SIGLA, DESCRICAO, COR, ORDENACAO, (SELECT COUNT(SIGLA) FROM CORES_CDP) AS LINHAS from CORES_CDP ORDER BY ORDENACAO"
		cursor.execute(query)
		resultado = cursor.fetchall()
		sigla = ""
		descricao = ""
		cor = ""
		ordenacao = ""
		
		k = 0
								
		for i in resultado:
			k = k + 1
			for j in range(0, columns):
				coord = str(k)+"_"+str(j)
				COORDS_LIST.append(coord)
				
				try:
					widget = frame_buttons.grid_slaves(row=k, column=j)[0]
					widget.destroy()
				except:
					pass
					
				try:
					widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row=k, column=j)[0]
					widget.destroy()
				except:
					pass
					
				sigla = i[0]
				descricao = i[1]
				cor  = i[2]
				ordenacao = i[3]
				linhas = i[4]
								
				if j == 4:						
					buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EDITAR', font=("Verdana", 8))
					buttons_dict[COORDS_LIST[-1]]["command"] = lambda vSigla = sigla, vDescricao = descricao, vCor = cor, vOrdenacao = ordenacao: edicao(vSigla, vDescricao, vCor, vOrdenacao)
					buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)
				elif j == 5:						
					buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EXCLUIR', font=("Verdana", 8))
					buttons_dict[COORDS_LIST[-1]]["command"] = lambda vSigla = sigla, vLinhas = linhas + 1, vColunas = columns: exclui(vSigla, vLinhas, vColunas)
					buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)						
				else:
					b = tk.Label(frame_buttons, anchor=W, text='', borderwidth=2, relief="groove")
					
					if j == 0:
						b['text'] = i[0]
						b['width'] = 10
					if j == 1:
						b['text'] = i[1]
						b['width'] = 30
					if j == 2:
						b['bg'] = i[2]
						b['width'] = 15
					if j == 3:
						b['text'] = i[3]
						b['width'] = 11
					if j == 4:
						b['width'] = 10						
					b.grid(row=k, column=j, sticky='news')		
									
		# Update buttons frames idle tasks to let tkinter calculate buttons sizes
		frame_buttons.update_idletasks()
	def exclui(sigla, linhas, colunas):
		MsgBox = tk.messagebox.askquestion ('Excluir Cor','Deseja excluir esse registro?',icon = 'warning', parent = u)
		if MsgBox == 'yes':			
			for i in range(1, linhas):
				for j in range(0, colunas):
					try:						
						widget = frame_buttons.grid_slaves(row = i, column = j)[0]
						widget.destroy()							
					except:
						pass						
					
					try:							
						widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row = i, column = j)[0]
						widget.destroy()
					except:
						pass						
			
			Delete = "delete from CORES_CDP where SIGLA='%s'" %(sigla)
			cursor.execute(Delete)
			con.commit()				
					
			popular_grid()														
	u = tk.Toplevel()
	u.grab_set()
	u.geometry(resolucao_tela_consulta)
	u.title('Consulta Cores - Cores CDP')
	
	frame_top = tk.Frame(u)
	frame_top.grid(sticky='news', padx=1)
	
	frame_main = tk.Frame(u)
	frame_main.grid(sticky='news')
	
	label1 = tk.Label(frame_top, text="SIGLA", fg="black", font=("Verdana", 8, 'bold'), width=9, relief="groove", anchor=W)
	label1.grid(row=0, column=0)
	
	label2 = tk.Label(frame_top, text="DESCRIÇÃO", fg="black", font=("Verdana", 8, 'bold'), width = 26, relief="groove", anchor=W)
	label2.grid(row=0, column=1)
	
	label3 = tk.Label(frame_top, text="COR", fg="black", font=("Verdana", 8, 'bold'), width=13, relief="groove", anchor=W)
	label3.grid(row=0, column=2)
	
	label4 = tk.Label(frame_top, text="ORDENAÇÃO", fg="black", font=("Verdana", 8, 'bold'), relief="groove", anchor=W)
	label4.grid(row=0, column=3)

	# Create a frame for the canvas with non-zero row&column weights
	frame_canvas = tk.Frame(frame_main)
	frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky='nw')
	frame_canvas.grid_rowconfigure(0, weight=1)
	frame_canvas.grid_columnconfigure(0, weight=1)
	# Set grid_propagate to False to allow 5-by-5 buttons resizing later
	frame_canvas.grid_propagate(False)
	
	# Add a canvas in that frame
	canvas = tk.Canvas(frame_canvas, bg = "#FFFFFF")
	canvas.grid(row=0, column=0, sticky="news")
	
	# Link a scrollbar to the canvas
	vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
	vsb.grid(row=0, column=1, sticky='ns')
	canvas.configure(yscrollcommand=vsb.set)
	
	# Create a frame to contain the buttons
	frame_buttons = tk.Frame(canvas, bg="#FFFFFF")
	canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
			
	popular_grid()
			
	# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
			
	frame_canvas.config(width=680, height=260)
	
	# Set the canvas scrolling region
	canvas.config(scrollregion=canvas.bbox("all"))
	
	frame_bottom = tk.Frame(u)
	frame_bottom.grid(sticky='news', padx=1)
	
	botaoNovo = tk.Button(frame_bottom, text='NOVO', font=("Verdana", 8), command=lambda : criacao())
	botaoNovo.grid(row=2, column=0)

	botaoFechar = tk.Button(frame_bottom, text='FECHAR', font=("Verdana", 8), command=lambda : on_close_cores_cdp())
	botaoFechar.grid(row=2, column=1)

	windowWidth, windowHeight = resolucao_width_consulta, resolucao_height_consulta
	positionRight = int(formulario.winfo_screenwidth()/2 - windowWidth/2)
	positionDown = int(formulario.winfo_screenheight()/2 - windowHeight/2)
	u.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_cores_cdp, u.destroy))
	u.geometry("+{}+{}".format(positionRight, positionDown))			
	u.attributes("-toolwindow", True)
	u.attributes("-topmost", True)
	u.attributes("-topmost", False)

def racas():
	selecionado = {
	"sigla": "",
	"descrição": ""
		}
	def on_close_avaliacao_visual_bezerro():
		formulario.grab_set()
		u.destroy()																		
	def novo():
		global selecionado
		global v_cores_cdp_modo
		def consiste():
			global v_cores_cdp_modo
											
			v_sigla = etrSigla.get()
			v_descricao = etrDescricao.get()
			
			if v_cores_cdp_modo == 'INCLUSAO':
				if v_sigla == '':
					lblMensagem['text'] = '*PREENCHA A SIGLA'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)
					return 0						
				if len(v_sigla) > 3:
					lblMensagem['text'] = '*A SIGLA DEVE TER NO MÁXIMO 3 CARACTERES'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)
					return 0
				
				dbRollNo = ""
				Select="select SIGLA from RACAS where SIGLA='%s'" %(v_sigla)
				cursor.execute(Select)
				result = cursor.fetchall()
				for i in result:
					dbRollNo=i[0]
				if(v_sigla == dbRollNo):
					lblMensagem['text'] = '*REGISTRO JÁ EXISTE'
					etrSigla.focus()
					t.after(5000, apaga_mensagem)
					return 0
					
			if len(v_descricao) > 20:
				lblMensagem['text'] = '*A DESCRIÇÃO DEVE TER NO MÁXIMO 25 CARACTERES'
				etrDescricao.focus()
				t.after(5000, apaga_mensagem)
				return 0
								
			return 1
			
		def insere():
			global v_cores_cdp_modo			
			
			r = consiste()
			
			if bool(r):
				etrSigla['state'] = 'normal'
				
				if v_cores_cdp_modo == 'INCLUSAO':
					Insert=''' Insert into RACAS(SIGLA, DESCRICAO) values(?,?) '''
					Sigla = etrSigla.get()
					Descricao = etrDescricao.get()
					Value=(Sigla, Descricao)
					cursor.execute(Insert, Value)
					con.commit()						
				if v_cores_cdp_modo == 'EDICAO':
					sigla = etrSigla.get()
					descricao = etrDescricao.get()
					Update = "update RACAS set SIGLA='%s', DESCRICAO='%s' where sigla='%s'" %(sigla, descricao, sigla)
					cursor.execute(Update)
					con.commit()
					etrSigla.delete(0, tk.END)
					etrDescricao.delete(0, tk.END)
					etrSigla.focus()
					v_cores_cdp_modo = 'INCLUSAO'
				combine_funcs(on_close_novo(), t.destroy())				
		def apaga_mensagem():
			lblMensagem['text'] = ''
		def on_close_novo():
			global v_cores_cdp_modo
			
			v_cores_cdp_modo = 'INCLUSAO'			
			popular_grid()
			u.grab_set()																						
		def limpa():
			global v_cores_cdp_modo
			
			etrSigla['state'] = 'normal'
			v_cores_cdp_modo = 'INCLUSAO'
			etrSigla.delete(0, tk.END)
			etrDescricao.delete(0, tk.END)
			etrSigla.focus()
		def iniciaEdicao():
			etrSigla['state'] = 'normal'
			etrSigla.delete(0, tk.END)
			etrSigla.insert(0, selecionado[0])
			etrSigla['state'] = 'disabled'
			etrDescricao.delete(0, tk.END)
			etrDescricao.insert(0, selecionado[1])
		def to_uppercaseSigla(*args):
			varEtrSigla.set(varEtrSigla.get().upper())
		def to_uppercaseDescricao(*args):
			varEtrDescricao.set(varEtrDescricao.get().upper())
		def on_enter_botaoIncluir(e):
			statusbarrodape['text'] = 'SALVAR'
		def on_leave_botaoIncluir(e):
			statusbarrodape['text'] = ''
		def on_enter_botaoLimpar(e):
			statusbarrodape['text'] = '        LIMPAR'
		def on_leave_botaoLimpar(e):
			statusbarrodape['text'] = ''
		def on_enter_botaoSair(e):
			statusbarrodape['text'] = '                FECHAR'
		def on_leave_botaoSair(e):
			statusbarrodape['text'] = ''
		t = tk.Toplevel()
		t.grab_set()
		t.geometry(resolucao_tela_cadastro)
		t.title('Raças')
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
		
		botaoSair = Button(footer, image=v_cores_cdp_icon_img_5, relief=FLAT, command = combine_funcs(on_close_novo, t.destroy))
		botaoSair.grid(column=2, row=8)
		botaoSair.bind("<Enter>", on_enter_botaoSair)
		botaoSair.bind("<Leave>", on_leave_botaoSair)						
				
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
		if etrSigla['state'] == 'normal':
			etrSigla.focus()
			
		t.attributes("-toolwindow", True)			
	def criacao():
		global selecionado
		global v_cores_cdp_modo
		
		selecionado = ()
		v_cores_cdp_modo = 'INCLUSAO'
		novo()
	def edicao(sigla, descricao):
		global selecionado
		global v_cores_cdp_modo
		
		selecionado = (sigla, descricao)
		
		if selecionado <> '':
			v_cores_cdp_modo = 'EDICAO'
			novo()			
	def popular_grid():
		global selecionado
		
		COORDS_LIST = []
		buttons_dict = {}
		
		columns = 4									
		query = "select SIGLA, DESCRICAO, (SELECT COUNT(SIGLA) FROM RACAS) AS LINHAS from RACAS"
		cursor.execute(query)
		resultado = cursor.fetchall()
		sigla = ""
		descricao = ""
		
		k = 0
								
		for i in resultado:
			k = k + 1
			for j in range(0, columns):
				coord = str(k)+"_"+str(j)
				COORDS_LIST.append(coord)
				
				try:
					widget = frame_buttons.grid_slaves(row=k, column=j)[0]
					widget.destroy()
				except:
					pass
					
				try:
					widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row=k, column=j)[0]
					widget.destroy()
				except:
					pass
					
				sigla = i[0]
				descricao = i[1]
				linhas = i[2]
								
				if j == 2:						
					buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EDITAR', font=("Verdana", 8))
					buttons_dict[COORDS_LIST[-1]]["command"] = lambda vSigla = sigla, vDescricao = descricao: edicao(vSigla, vDescricao)
					buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)
				elif j == 3:						
					buttons_dict[COORDS_LIST[-1]] = tk.Button(frame_buttons, text='EXCLUIR', font=("Verdana", 8))
					buttons_dict[COORDS_LIST[-1]]["command"] = lambda vSigla = sigla, vLinhas = linhas + 1, vColunas = columns: exclui(vSigla, vLinhas, vColunas)
					buttons_dict[COORDS_LIST[-1]].grid(row = k, column = j, sticky = 'news', padx = 1, pady = 1)						
				else:
					b = tk.Label(frame_buttons, anchor=W, text='', borderwidth=2, relief="groove")
					
					if j == 0:
						b['text'] = i[0]
						b['width'] = 10
					if j == 1:
						b['text'] = i[1]
						b['width'] = 30						
					b.grid(row=k, column=j, sticky='news')		
									
		# Update buttons frames idle tasks to let tkinter calculate buttons sizes
		frame_buttons.update_idletasks()
	def exclui(sigla, linhas, colunas):
		MsgBox = tk.messagebox.askquestion ('Excluir Cor','Deseja excluir esse registro?',icon = 'warning', parent = u)
		if MsgBox == 'yes':			
			for i in range(1, linhas):
				for j in range(0, colunas):
					try:						
						widget = frame_buttons.grid_slaves(row = i, column = j)[0]
						widget.destroy()							
					except:
						pass						
					
					try:							
						widget = buttons_dict[COORDS_LIST[-1]].grid_slaves(row = i, column = j)[0]
						widget.destroy()
					except:
						pass						
			
			Delete = "delete from RACAS where SIGLA='%s'" %(sigla)
			cursor.execute(Delete)
			con.commit()				
					
			popular_grid()														
	u = tk.Toplevel()
	u.grab_set()
	u.geometry(resolucao_tela_consulta)
	u.title('Raças')
	
	frame_top = tk.Frame(u)
	frame_top.grid(sticky='news', padx=1)
	
	frame_main = tk.Frame(u)
	frame_main.grid(sticky='news')
	
	label1 = tk.Label(frame_top, text="SIGLA", fg="black", font=("Verdana", 8, 'bold'), width=9, relief="groove", anchor=W)
	label1.grid(row=0, column=0)
	
	label2 = tk.Label(frame_top, text="DESCRIÇÃO", fg="black", font=("Verdana", 8, 'bold'), width = 26, relief="groove", anchor=W)
	label2.grid(row=0, column=1)
		
	# Create a frame for the canvas with non-zero row&column weights
	frame_canvas = tk.Frame(frame_main)
	frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky='nw')
	frame_canvas.grid_rowconfigure(0, weight=1)
	frame_canvas.grid_columnconfigure(0, weight=1)
	# Set grid_propagate to False to allow 5-by-5 buttons resizing later
	frame_canvas.grid_propagate(False)
	
	# Add a canvas in that frame
	canvas = tk.Canvas(frame_canvas, bg = "#FFFFFF")
	canvas.grid(row=0, column=0, sticky="news")
	
	# Link a scrollbar to the canvas
	vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
	vsb.grid(row=0, column=1, sticky='ns')
	canvas.configure(yscrollcommand=vsb.set)
	
	# Create a frame to contain the buttons
	frame_buttons = tk.Frame(canvas, bg="#FFFFFF")
	canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
			
	popular_grid()
			
	# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
			
	frame_canvas.config(width=680, height=260)
	
	# Set the canvas scrolling region
	canvas.config(scrollregion=canvas.bbox("all"))
	
	frame_bottom = tk.Frame(u)
	frame_bottom.grid(sticky='news', padx=1)
	
	botaoNovo = tk.Button(frame_bottom, text='NOVO', font=("Verdana", 8), command=lambda : criacao())
	botaoNovo.grid(row=2, column=0)

	botaoFechar = tk.Button(frame_bottom, text='FECHAR', font=("Verdana", 8), command=lambda : on_close_avaliacao_visual_bezerro())
	botaoFechar.grid(row=2, column=1)

	windowWidth, windowHeight = resolucao_width_consulta, resolucao_height_consulta
	positionRight = int(formulario.winfo_screenwidth()/2 - windowWidth/2)
	positionDown = int(formulario.winfo_screenheight()/2 - windowHeight/2)
	u.geometry("+{}+{}".format(positionRight, positionDown))
	u.protocol("WM_DELETE_WINDOW", combine_funcs(on_close_avaliacao_visual_bezerro, u.destroy))			
	u.attributes("-toolwindow", True)
		
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
icone4 = Image.open("BZ_64x64.png")
icone5 = Image.open("M_64x64.png")
icone6 = Image.open("CD_64x64.png")
icone7 = Image.open("RACAS_64x64.png")
v_cores_cdp_icon_1 = Image.open("COLOR_16x16.png")
v_cores_cdp_icon_2 = Image.open("ADD_32x32.png")
v_cores_cdp_icon_4 = Image.open("CLEAR_32x32.png")
v_cores_cdp_icon_5 = Image.open("EXIT_32x32.png")
 
# Cria Imagens
imagem1 = ImageTk.PhotoImage(icone1)
imagem2 = ImageTk.PhotoImage(icone2)
imagem3 = ImageTk.PhotoImage(icone3)
imagem4 = ImageTk.PhotoImage(icone4)
imagem5 = ImageTk.PhotoImage(icone5)
imagem6 = ImageTk.PhotoImage(icone6)
imagem7 = ImageTk.PhotoImage(icone7)
v_cores_cdp_icon_img_1 = ImageTk.PhotoImage(v_cores_cdp_icon_1)
v_cores_cdp_icon_img_2 = ImageTk.PhotoImage(v_cores_cdp_icon_2)
v_cores_cdp_icon_img_4 = ImageTk.PhotoImage(v_cores_cdp_icon_4)
v_cores_cdp_icon_img_5 = ImageTk.PhotoImage(v_cores_cdp_icon_5)
 
# Cria botões
botao1 = Button(ferramenta, image=imagem1, relief=FLAT, command=cores)

def on_enter_botao1(e):
	statusbarmenu['text'] = 'CORES'

def on_leave_botao1(e):
	statusbarmenu['text'] = ''

botao2 = Button(ferramenta, image=imagem2, relief=FLAT, command=configura_tela_inicial)

def on_enter_botao2(e):
	statusbarmenu['text'] = '                                                                                             CONFIGURAÇÕES'

def on_leave_botao2(e):
	statusbarmenu['text'] = ''

botao3 = Button(ferramenta, image=imagem3, relief=FLAT, command=client_exit)

def on_enter_botao3(e):
	statusbarmenu['text'] = '                                                                                                                   SAIR'

def on_leave_botao3(e):
	statusbarmenu['text'] = ''

botao4 = Button(ferramenta, image=imagem4, relief=FLAT, command=situacoes_bezerros)

def on_enter_botao4(e):
	statusbarmenu['text'] = '                                       SITUAÇÕES BEZERROS'

def on_leave_botao4(e):
	statusbarmenu['text'] = ''
	
botao5 = Button(ferramenta, image=imagem5, relief=FLAT, command=situacoes_matrizes)

def on_enter_botao5(e):
	statusbarmenu['text'] = '                                                         SITUAÇÕES MATRIZES E/OU REPRODUTORES'

def on_leave_botao5(e):
	statusbarmenu['text'] = ''

botao6 = Button(ferramenta, image=imagem6, relief=FLAT, command=causas)

def on_enter_botao6(e):
	statusbarmenu['text'] = '                                                                            CAUSAS (1, 2, 3)'

def on_leave_botao6(e):
	statusbarmenu['text'] = ''
	
botao7 = Button(ferramenta, image=imagem7, relief=FLAT, command=racas)

def on_enter_botao7(e):
	statusbarmenu['text'] = '                    RAÇAS'

def on_leave_botao7(e):
	statusbarmenu['text'] = ''	

botao1.bind("<Enter>", on_enter_botao1)
botao1.bind("<Leave>", on_leave_botao1)

botao2.bind("<Enter>", on_enter_botao2)
botao2.bind("<Leave>", on_leave_botao2)

botao3.bind("<Enter>", on_enter_botao3)
botao3.bind("<Leave>", on_leave_botao3)

botao4.bind("<Enter>", on_enter_botao4)
botao4.bind("<Leave>", on_leave_botao4)

botao5.bind("<Enter>", on_enter_botao5)
botao5.bind("<Leave>", on_leave_botao5)

botao6.bind("<Enter>", on_enter_botao6)
botao6.bind("<Leave>", on_leave_botao6)

botao7.bind("<Enter>", on_enter_botao7)
botao7.bind("<Leave>", on_leave_botao7)

statusbartitulo = tk.Label(formulario, text="SIAGAP - Sistema Integrado de Avaliação Genética e Acasalamento Produtivo", bd=1, font=("Verdana", 12), relief=RAISED, anchor="center")
statusbartitulo.pack(side=tk.TOP, fill=tk.X)

# Posiciona componentes
botao1.pack(side=LEFT, padx=2, pady=2)
botao7.pack(side=LEFT, padx=2, pady=2)
botao4.pack(side=LEFT, padx=2, pady=2)
botao5.pack(side=LEFT, padx=2, pady=2)
botao6.pack(side=LEFT, padx=2, pady=2)
botao2.pack(side=LEFT, padx=2, pady=2)
botao3.pack(side=LEFT, padx=2, pady=2)
ferramenta.pack(side=TOP, fill=X)

# barra de status no rodapé
statusbarmenu = tk.Label(formulario, text="", bd=0, font=("Verdana", 8, 'bold'), relief=tk.SUNKEN, anchor=tk.W)
statusbarmenu.pack(side=tk.TOP, fill=tk.X)

statusbarrodape = tk.Label(formulario, text="Versão 6.0", bd=1, font=("Verdana", 12), relief=tk.SUNKEN, anchor=tk.W)
statusbarrodape.pack(side=tk.BOTTOM, fill=tk.X) 
 
# Loop do tcl
formulario.attributes("-topmost", True)
formulario.attributes("-topmost", False)
formulario.attributes('-fullscreen',  True)
formulario.mainloop()
