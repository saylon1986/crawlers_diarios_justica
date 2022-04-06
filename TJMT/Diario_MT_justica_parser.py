# Imports de bibliotecas
import pandas as pd
from tqdm import tqdm
from PyPDF2 import PdfFileReader, PdfFileMerger
import os, re
import fitz




##################################################################################################

							# Função para separar os textos das publicações

def Separar_textos_paginas():

	# diretório com as pastas e os dados

	diret = r'./Diarios_MT_2019'

	pastas = os.listdir(diret)


	# listas que receberão os dados

	numeros_paginas =[]
	nome_doc = []
	nomes_pastas =[]
	txt_unific = []
	sem_lines = []


	# iteração das pastas para acessar os arquivos de PDF individualmente

	for b in tqdm(range(len(pastas))):
		nome_pasta = os.path.join(diret, pastas[b])
		arquivos = os.listdir(nome_pasta)
		for a in range(len(arquivos)):
			# print(arquivos[a])
			nome = os.path.join(nome_pasta, arquivos[a])


			# contagem dos números das páginas
			num_pag = 0


			with fitz.open(nome) as pdf:
				for pagina in pdf:
					num_pag = num_pag + 1
					
					blocks = pagina.getText("dict")['blocks'] # método que divide o texto em blocos no formato dict
					# blocks = pagina.getText('blocks')
					# for item in blocks:
					# 	print(item,'\n')
					# 	z= input("")
				
					for o in range(len(blocks)):
											

						try: # elimina os blocos que não contém "lines" e consequentemente não tem textos
							
							lines = blocks[o]["lines"] # separa as linhas
							
							txt_block = []	
							
							for x in range(len(lines)):
								spans = lines[x]["spans"] # separa os spans
								
								for u in spans:
									txt_block.append(u['text']) # separa todos os textos de cada bloco e salva na lista para unificação
									

							# unifica os textos de cada bloco e salva o número da página, nome do arquivo e a data

							txt_fim = " ".join(txt_block)
							txt_unific.append(str(txt_fim))
							# print(txt_fim)
							# print("______________________")
							numeros_paginas.append(num_pag)
							nomes_pastas.append(nome_pasta[-10:])
							nome_doc.append(arquivos[a])


							# PARA CONFERÊNCIA - DESCOMENTAR CASO QUEIRA VERIFICAR O CORTE DAS PUBLICAÇÕES (por seção)- APERTAR ENTER A CADA PUBLICAÇÃO

							# print('Pasta:',nome_pasta[-10:]," --- ", 'arquivo:', arquivos[a])
							# print("Estamos na página:", num_pag)
							# print("No bloco número:",o,"num total de", len(blocks))
							# print("Publicação:")
							# print(txt_fim)
							# print("------------------------\n")
							# z = input("")
							

						# se não tiver as linhas, salva em outra lista - somente para conferência, não tem utilidade.					
						
						except:
							sem_lines.append(blocks[o]["number"])

	
	Juntar_blocks(numeros_paginas,nome_doc, nomes_pastas, txt_unific)								
	return numeros_paginas,	nome_doc, nomes_pastas, txt_unific
	

###############################################################################

 			###### Função para separar as publicações de interesse e Gerar um Banco de dados e um excel #########


def Juntar_blocks(numeros_paginas,nome_doc, nomes_pastas, txt_unific):


	### Problemas:
	##### pensar como unificar as publis que excedem mais de uma página


	publicacoes = []
	num_pags = []
	nome_docs = []
	nome_pst = []
	x = 0


	print("temos", len(txt_unific), "publicações")

	for txt,num,doc,pst in zip(txt_unific,numeros_paginas,nome_doc,nomes_pastas):
		# txt ="Temos um numero 1001461-41.2022.8.11.0000" 
	# txt ="" Número:  1001461­41.2022.8.11.0000 
		if re.search(r'\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}',txt, re.IGNORECASE.MULTILINE):
			# print(txt)
			publicacoes.append(txt)
			num_pags.append(num)
			nome_docs.append(doc)
			nome_pst.append(pst)
			# print('Pasta:',pst," --- ", 'arquivo:', doc)
			# print("Estamos na página:", num)
			# print("Publicação:")
			# print(txt)
			# print("------------------------\n")
			# z = input("")
			x = 0
	
		else:
			if x <= 4 and len(publicacoes)>=1:
				txt = publicacoes[-1]+" "+txt
				del publicacoes[-1]
				publicacoes.append(txt)
				x = x+1
			else:
				pass



	for item,num in zip(publicacoes,num_pags):
		print("página", num)
		print(item)
		print("-----------------")
		z = input('')


	df_textos_paginas = pd.DataFrame()    
	df_textos_paginas["publicacoes"] = publicacoes
	df_textos_paginas["numeros_paginas"] = num_pags
	df_textos_paginas["nome_documento"] = nome_docs
	df_textos_paginas["nomes_pastas"] = nome_pst	

	df_textos_paginas.to_excel("Diarios_publicacoes.xlsx", index = False)



################################################################################################################

def Main_Separacao():

	data_frames = Separar_textos_paginas()

################################################################################################################


Main_Separacao()