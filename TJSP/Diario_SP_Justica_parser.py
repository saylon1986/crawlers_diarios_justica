# Imports de bibliotecas
import os
import pandas as pd
from requests.models import get_auth_from_url
from tqdm import tqdm
import requests
from pathlib import Path
import time
from bs4 import BeautifulSoup
from lxml import etree
from fake_useragent import UserAgent
import urllib.request

# Imports Selenium (Navegador Web)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PyPDF2 import PdfFileReader, PdfFileMerger
import shutil
import time

import os, re
import datetime
import pandas as pd
import numpy as np
import shutil
from bs4 import BeautifulSoup
import fitz
from tqdm import tqdm
# from PDF_diario import Baixar_diarios_ajuste
import time



#######################################################################################################################

def Separar_textos_paginas(nome, arquivo, pasta):

	# print(nome)
	# z = input("")
	with fitz.open(nome) as pdf:
		num_pag = 1
		textos_paginas =[]
		numeros_paginas =[]
		nome_doc = []
		nomes_pastas =[]
		for pagina in pdf:
			texto = pagina.getText()
			textos_paginas.append(texto)
			numeros_paginas.append(num_pag)
			nome_doc.append(arquivo)
			nomes_pastas.append(pasta)
			num_pag = num_pag+1
	    
	df_textos_paginas = pd.DataFrame()    
	df_textos_paginas["textos_paginas"] = textos_paginas
	df_textos_paginas["numeros_paginas"] = numeros_paginas
	df_textos_paginas["nome_documento"] = nome_doc
	df_textos_paginas["nomes_pastas"] = nomes_pastas
	# print(df_textos_paginas)
	# df_textos_paginas.to_excel("diario_cortado.xlsx", index = False)
	# data_frames.append(df_textos_paginas)

	
	# print("temos",len(df_textos_paginas),"data Frames")	    
	return df_textos_paginas


################################################################################################################


def Cortar_publicacoes(df_textos_paginas):


	datas = []
	numeros_paginas =[]
	numeros_certos =[]
	trechos_certos = []
	docs_certos = []
	paginas_erros = []
	publis_erros = []
	datas_erros = []
	docs_errados = []
	pastas = []

	qtdade_paginas = df_textos_paginas["textos_paginas"] 

	continuacao = ""
	for public, numero, doc, pasta in tqdm(zip(df_textos_paginas["textos_paginas"],df_textos_paginas["numeros_paginas"], df_textos_paginas["nome_documento"], df_textos_paginas["nomes_pastas"])):
		texto = str(public)
		num_pag = numero
		pasta = str(pasta)

		numer = re.findall("\n(\d{1,3}\. Processo \d{2,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})", texto)
		numer_2 = re.findall("(\nProcesso \d{2,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})", texto)
		numer_3 = re.findall("\nNº \d{2,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", texto)
		numer_4 = re.findall("(\nProcesso: \d{2,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})", texto)
		numer_5 = re.findall("\n\d{2,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}; Processo", texto)
		numer_6 = re.findall("\nN° \d{2,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", texto)
		numer_7 = re.findall("\nPROCESSO \n:\d{2,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", texto)
		numeros = numer + numer_2 + numer_3 +numer_4 + numer_5 + numer_6 + numer_7


		# print(texto.encode())
		# print("estamos na página", num_pag, "do documento", doc)
		# print(numeros)
		# print("temos", len(numeros),'nessa página')
		# z = input("paradinha")

		# encontra os numeros dos processos para fazer o corte
		num_caract = []
		for item in numeros:
			num_caracter = texto.find(item)
			if num_caracter not in num_caract:
				num_caract.append(num_caracter)
			else:
				num_caracter = texto.find(item,num_caracter+28,len(texto))
				num_caract.append(num_caracter)


		# insere o caracter final e orgniza a lista com os indices dos caracteres iniciais dos numeros dos processos
		num_caract.append(len(texto)-1)	
		num_caract.sort()
			

		df_caract = pd.DataFrame()
		df_caract ["caracter"] = num_caract
		df_caract = df_caract.drop_duplicates(subset = "caracter")

		num_caract = df_caract ["caracter"].to_list()

		# gera a lista com os números dos caracteres para fazer os cortes e gera a lista com as publis separadas
		publis = []
		num_comec = 0
		for h in range(len(num_caract)):
			trecho = texto [num_comec:num_caract[h]]
			trecho = trecho.strip()
			publis.append(trecho)
			num_comec = num_caract [h]



		# print("essa página tem", len(publis),"publicações")	
		# pega a data da publicação
		for item in publis:
			padr_data = "Disponibilização:.+\n"
			data_exte = re.findall(padr_data,item)
			if len(data_exte) > 0:
				nada, data = data_exte[0].split(":")
				data = data.strip()
				# print(data)
				break

		# limpa o cabeçalho
		padroes = ["Publicação Oficial do Tribunal de Justiça.+\n","Disponibilização:.+\n","Diário da Justiça.+\n",".+Edição.+"]
		for item in padroes:
			elim = re.findall(item,publis[0])
			if len(elim) > 0:
				for p in elim:
					publis[0] = publis[0].replace(p,"")	

		if num_pag == 1:
			del publis[0]
			data = "nada"
		elif num_pag == 2:
			for w in range(len(datas)):
				item = datas[w]
				if item == "nada":
					datas[w] = data
			
				
		if len(continuacao) > 2:
			publis[0] = continuacao + publis[0]
			# print("juntou o pedaço anterior")

		# if num_pag == 1079:	
		# 	for item in publis:
		# 		print(item)
		# 		print()
		# 		print("-------------------")
		# 		z = input('')	

		### separa os dados das publis cortadas
		for o in range(len(publis)):
			if num_pag != len(qtdade_paginas):
				if o != len(publis)-1:
					try:
						numer = re.search('\d{2,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}',publis[o]).group()
						# print(numer)
						numeros_certos.append(numer)
						datas.append(data)
						if o == 0 and num_pag != 1:
							numeros_paginas.append(num_pag_ant)
							# print("essa publis terá o número da página anterior", num_pag_ant)
						else:
							numeros_paginas.append(num_pag)
						trechos_certos.append(publis[o])
						docs_certos.append(doc)
						pastas.append(pasta)
						# print(publis[o])
						# z = input("Essa está certa!")
					except:
						# print(publis[o])
						publis_erros.append(publis[o])
						print("publicação", o)
						print("da página", num_pag)
						print("contem um erro")
						paginas_erros.append(num_pag)
						datas_erros.append(data)
						docs_errados.append(doc)
						# z = input("verificar")

				else:
					continuacao = publis[o]
					if len(publis) > 1:
						num_pag_ant = num_pag
					elif len(publis) == 1:
						pass
			
			else:
				numer = re.search('\d{2,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}',publis[o]).group()
				numeros_certos.append(numer)	
				datas.append(data)
				numeros_paginas.append(num_pag_ant)
				trechos_certos.append(publis[o])
				docs_certos.append(doc)
				pastas.append(pasta)		

	return trechos_certos, numeros_certos, datas, numeros_paginas, docs_certos, paginas_erros, publis_erros, datas_erros, docs_errados, pastas

##############################################################################################################

def Separacao(df):
	
	termos_1 = "prisão domiciliar|residência particular"
	termos_2 = "doença grave|moléstia grave|(70|80) anos|gestante(s)|gr(á|a)vida"
	termos_3 = "pena(l|is)|CPP|LEP|pena"
	indexes_ruins =[]
	# print("o DF tinha", len(df["Publicação"]))

	for i, texto_publi in enumerate(df["Publicação"]):
		if re.search(termos_1, texto_publi,re.IGNORECASE):
			if re.search(termos_2, texto_publi,re.IGNORECASE): 
				if re.search(termos_3, texto_publi,re.IGNORECASE):
					pass
				else:
					indexes_ruins.append(i)	
			else:
				indexes_ruins.append(i)		
		else:
			indexes_ruins.append(i)		


	df = df.drop(indexes_ruins)
	# print("agora o DF tem", len(df["Publicação"]))
	return df		



# ################################################### ***********  ###########################################

def Main_Separacao():

	
	anterior_certos = pd.DataFrame()
	anterior_errados = pd.DataFrame()

	diret = input("insira o diretório com as pastas:")

	pastas = os.listdir(diret)
	# pastas = pastas_x[0:3]
	# pastas.sort()
	# print(pastas)

	# data_frames=[]	
	for pasta in tqdm(pastas):#len(pastas))):
		print("*************************************")
		print()
		print("estamos na pasta", pasta)
		print()
		print("*************************************")
		# z = input("")

		# '''
		nome_pasta = os.path.join(diret, pasta)
		arquivos = os.listdir(nome_pasta)
		for a in range(len(arquivos)):
			try:
				print(arquivos[a])
				nome = os.path.join(nome_pasta, arquivos[a])

				# Separar_textos_paginas()
				data_frames = []
				data_frame = Separar_textos_paginas(nome, arquivos[a], pasta)
				data_frames.append(data_frame)


				for m in range(len(data_frames)):
					trechos_certos, numeros_certos, datas, numeros_paginas, docs_certos, paginas_erros, publis_erros, datas_erros, docs_errados, pastas = Cortar_publicacoes(data_frames[m])


					#criando o objeto dataframe
					df_certos = pd.DataFrame()
					r = pd.Series(numeros_certos)
					y = pd.Series(trechos_certos)
					x = pd.Series(numeros_paginas)
					h = pd.Series(docs_certos)
					i = pd.Series(pastas)
					g = pd.Series(datas)
					df_certos = pd.concat([r,y,x,h,i,g], axis=1,keys=["Número do Processo","Publicação","Numero da página","Nome do documento", "Nome da Pasta","Data do diário"])

					
					# ajuste da data

					cortados = df_certos["Data do diário"].str.split(",", n =1, expand = True)

					df_certos ["Dia da semana"] = cortados [0]

					frag = cortados[1].str.split("de ", n=2, expand = True)

					df_certos ["Dia"] = frag[0]
					df_certos ["Mês"] = frag[1]
					df_certos ["Ano"] = frag[2]
					df_certos ["Estado"] = "SP"
					df_certos["Instância"] = np.where(df_certos["Nome do documento"].str.contains("2ªInstancia"), "2ª Instancia", "1ª Instancia")

					#############################
					

					separados = Separacao(df_certos)



					if len(anterior_certos) >= 1:
						try:
							anterior_certos = pd.concat([separados,anterior_certos])
							print("temos", len(anterior_certos), "certos")
					
						except:
							anterior_certos.to_excel("Diarios_publicacoes_separados_2021_.xlsx", index = False)
							print("erro no DF", m)
					else:
						anterior_certos = separados
			except:
				print(" **********  ")
				print()
				print("erro na pasta", pasta,"e no arquivo:", arquivos[a])
				print()
				print(" **********  ")
				pass			
		
	try:
		antigos = pd.read_excel("Diarios_publicacoes_separados_2021_.xlsx", engine ='openpyxl')
		# print("Já temos a planilha certos!")
		# print(anterior_certos)
		# print()
		# print()
		# print()
		# print(df_certos)
		# print()
		# print()
		# print()
		anterior_certos = pd.concat([antigos,anterior_certos])
		# print(df_certos)
		anterior_certos.to_excel("Diarios_publicacoes_separados_2021_.xlsx", index = False)
	except:
		anterior_certos.to_excel("Diarios_publicacoes_separados_2021_.xlsx", index = False)
		

	# anterior_certos.to_excel("Diarios_publicacoes_separados.xlsx", index = False)
			
# '''
Main_Separacao()