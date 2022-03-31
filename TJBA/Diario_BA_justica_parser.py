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
from tika import parser
import json
import charade



#######################################################################################################################

def Separar_textos_paginas():
	diret = r'C:\Users\saylo\Documents\crawlers_diarios_justica\TJBA\Diarios_BA' #input("insira o diretório com as pastas:")

	pastas = os.listdir(diret)

	numeros_paginas =[]
	nome_doc = []
	nomes_pastas =[]
	vlrs_unific= []
	flags = []
	txt_unific = []
	sem_lines = []

	for b in tqdm(range(len(pastas))):
		nome_pasta = os.path.join(diret, pastas[b])
		# arquivos = os.listdir(nome_pasta)
		# for a in range(len(arquivos)):
		# 	print(arquivos[a])
		# 	nome = os.path.join(nome_pasta, arquivos[a])

		num_pag = 0
		with fitz.open(nome_pasta) as pdf:
			for pagina in pdf:
				num_pag = num_pag + 1
				# print()
				# print()
				# print()
				# print("               --------------------------------")
				# print()
				# print()
				# print()
				# print("                        Página", num_pag,"                ")
				# # print(                   "tamanho da lista:", len(txt_unific))
				# # print(txt_unific)
				# # print(nome_doc)
				# # print(nomes_pastas)
				# # print(vlrs_unific)
				# # print(numeros_paginas)
				# print()
				# print()
				# print("               --------------------------------")
				# print()
				# z = input("")
				blocks = pagina.getText("dict")['blocks']
				for o in range(len(blocks)):
					# print()
					# print("--------------------")
					# print('nesta página temos',len(blocks)," blocos")		
					# print('Estamos no blocos', blocks[o]["number"])
					# print(blocks[o])
					# z = input("")
					
					
					txt_unificp = []		
					try:
						lines = blocks[o]["lines"]
						# print("neste bloco temos", len(lines),"linhas")
						textos = []
						for x in range(len(lines)):
							spans = lines[x]["spans"]
							# print("nessa linha temos", len(spans),"spans")
							for u in spans:
								flag = str(u['flags'])
								tam = str(u["size"])
								tam = tam.split(".")
								te = str(u['bbox'][0])
								ta = te.split(".")
								dist = int(ta[0])
								if tam [0] == "9" and flag == "0" and dist == 42:
									## colocar na unificação provisória e depois na final, texto da publi já vai separado
									txt_unificp.append(u['text'].strip())
									# vlrs_unific.append(dist)
									# numeros_paginas.append(num_pag)
									# nome_doc.append(nome_pasta)
						# print(txt_unificp)
						# z = input("")
						# print(vlrs_unific)
						# print("-------------")
						# z = input("")
							# try:
							# 	textos = " ".join(textos)
							# 	txt_unificp.append(textos)
							# except:
							# 	pass


						txt_unificp = " ".join(txt_unificp)
						if len(txt_unificp) > 150: #### pensar melhor nessa regra, talvez o critério melhor seja unificar com o anterior ou posterior			
							txt_unific.append(txt_unificp)
							numeros_paginas.append(num_pag)
							# nomes_pastas.append(nomes_pastas)
							nome_doc.append(nomes_pasta)
					
					except:
						# print("deu algum erro")
						sem_lines.append(blocks[o]["number"])
			

						
				
				##  Problemas:
				
				### verificar a numeração
				#### ver com o Gui como pegar os cadernos separados pra não ter o aDM

	
	# df_textos_paginas = pd.DataFrame()    
	# df_textos_paginas["valores"] = vlrs_unific


	# df_textos_paginas = pd.DataFrame(df_textos_paginas.groupby(["valores"])["valores"].count())
	# df_textos_paginas.columns = ["quantidade"]


	# df_textos_paginas = df_textos_paginas.reset_index()
	# df_textos_paginas.to_excel("Quantidade_prgf.xlsx", index = False)
	# for item in txt_unific:
	# 	print(item)
	# 	print("-----------------")
	# 	z = input("")			


	# Juntar_blocks(numeros_paginas,nome_doc, nomes_pastas, vlrs_unific, txt_unific)								
	# return numeros_paginas,	nome_doc, nomes_pastas,	vlrs_unific, txt_unific


###############################################################################

def Juntar_blocks(numeros_paginas,nome_doc, nomes_pastas, vlrs_unific, txt_unific):


		prgf = []
		num_paginas= []		
		nom_pastas = []
		nom_docs = []
		for k in range(len(vlrs_unific)):
			if vlrs_unific[k] == 70 or vlrs_unific[k] == 316 or vlrs_unific[k] == 317:
				pos = vlrs_unific.index(vlrs_unific[k],k)
				prgf.append(pos)
				# print(pos)
				# print(numeros_paginas[pos])
				# z= input("")
				# num_paginas.append(numeros_paginas[pos])
				# nom_pastas.append(nomes_pastas[pos])
				# nom_docs.append(nome_doc[pos])

		# print(prgf)
		# print(num_paginas)

				
		publicacoes = []
		for z in range(len(prgf)):
			atual = prgf[z]
			try:
				final = prgf[z+1]
				publi = txt_unific[atual:final]
				if len(publi)> 1:
					txt_publi = " ".join(publi)
					if len(txt_publi) > 150:
						publicacoes.append(txt_publi)
						num_paginas.append(numeros_paginas[atual])
						nom_pastas.append(nomes_pastas[atual][-10:])
						nom_docs.append(str(nome_doc[atual]))
			except:
				pass	

		# for j in range(len(num_paginas)):
		# 	print(num_paginas [j])
		# 	print(publicacoes [j])
		# 	print(nom_pastas[j])
		# 	print(nom_docs[j])
		# 	print()
		# 	print('---------------------')
			# z = input('')


		df_textos_paginas = pd.DataFrame()    
		df_textos_paginas["publicacoes"] = publicacoes
		df_textos_paginas["numeros_paginas"] = num_paginas
		df_textos_paginas["nome_documento"] = nom_docs
		df_textos_paginas["nomes_pastas"] = nom_pastas	


		df_textos_paginas.to_excel("Diarios_publicacoes.xlsx", index = False)



################################################################################################################



# ################################################### ***********  ###########################################

def Main_Separacao():

	data_frames = Separar_textos_paginas()

Main_Separacao()