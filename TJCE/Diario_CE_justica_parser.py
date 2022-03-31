# Imports de bibliotecas
import pandas as pd
from tqdm import tqdm
from PyPDF2 import PdfFileReader, PdfFileMerger
import os, re
import fitz




##################################################################################################

def Separar_textos_paginas():
	diret = input("insira o diretório com as pastas:")

	pastas = os.listdir(diret)

	numeros_paginas =[]
	nome_doc = []
	nomes_pastas =[]
	txt_unific = []
	sem_lines = []

	for b in tqdm(range(len(pastas))):
		nome_pasta = os.path.join(diret, pastas[b])
		arquivos = os.listdir(nome_pasta)
		for a in range(len(arquivos)):
			print(arquivos[a])
			nome = os.path.join(nome_pasta, arquivos[a])

			num_pag = 0
			with fitz.open(nome) as pdf:
				for pagina in pdf:
					num_pag = num_pag + 1
					blocks = pagina.getText("dict")['blocks']
					# print("essa página tem", len(blocks),'blocos')
					for o in range(len(blocks)):
						try:
							lines = blocks[o]["lines"]
							txt_block = []	
							if len(lines) > 0: #### eliminar essa regra depois de fazer o limpador dos cabeçalhos
								for x in range(len(lines)):
									spans = lines[x]["spans"]
									for u in spans:
										tam = str(u["size"])
										flag = str(u["flags"])
										tam = tam.split(".")
										if tam [0] == "7" and flag == "4":
											txt_block.append(u['text'])
											
								if len(txt_block) > 0:
									txt_fim = " ".join(txt_block)
									txt_unific.append(txt_fim)
									numeros_paginas.append(num_pag)
									nomes_pastas.append(nome_pasta[-10:])
									nome_doc.append(arquivos[a])
								
										
						except:
							sem_lines.append(blocks[o]["number"])	



	Juntar_blocks(numeros_paginas,nome_doc, nomes_pastas, txt_unific)								
	return numeros_paginas,	nome_doc, nomes_pastas, txt_unific
	

###############################################################################

def Juntar_blocks(numeros_paginas,nome_doc, nomes_pastas, txt_unific):


	### Problemas:
	##### pensar como unificar as publis que excedem mais de uma página
	


	publicacoes = []
	num_pags = []
	nome_docs = []
	nome_pst = []
	for txt,num,doc,pst in zip(txt_unific,numeros_paginas,nome_doc,nomes_pastas):
		# print(txt,num,doc,pst)
		if len(txt) > 100:
			publicacoes.append(txt)
			num_pags.append(num)
			nome_docs.append(doc)
			nome_pst.append(pst)


	df_textos_paginas = pd.DataFrame()    
	df_textos_paginas["publicacoes"] = publicacoes
	df_textos_paginas["numeros_paginas"] = num_pags
	df_textos_paginas["nome_documento"] = nome_docs
	df_textos_paginas["nomes_pastas"] = nome_pst	

	df_textos_paginas.to_excel("Diarios_publicacoes.xlsx", index = False)


	for item in publicacoes:
		print(item)
		z = input("")

		### problema: processos com o número em negrito...verificar
		### o que fazer com os que excedem uma página



################################################################################################################

def Main_Separacao():

	data_frames = Separar_textos_paginas()

################################################################################################################


Main_Separacao()