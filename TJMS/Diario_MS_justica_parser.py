# Imports de bibliotecas
import pandas as pd
from tqdm import tqdm
from PyPDF2 import PdfFileReader, PdfFileMerger
import os, re
import fitz




##################################################################################################

									# Função para separar os textos das publicações

def Separar_textos_paginas(ano):


	diret = r'./Diarios_MS_'+ano

	pastas = os.listdir(diret)

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
			print(arquivos[a])
			nome = os.path.join(nome_pasta, arquivos[a])


			# contagem dos números das páginas
			num_pag = 0


			with fitz.open(nome) as pdf:
				for pagina in pdf:
					num_pag = num_pag + 1
					blocks = pagina.getText("dict")['blocks'] # método que divide o texto em blocos no formato dict
				

					for o in range(len(blocks)):
				
						try: # elimina os blocos que não contém "lines" e consequentemente não tem textos

							lines = blocks[o]["lines"] # separa as linhas
							txt_block = []	
					
							for x in range(len(lines)):
								spans = lines[x]["spans"] # separa os spans
								for u in spans:
									txt_block.append(u['text']) # separa todos os textos de cada bloco e salva na lista para unificação
							

							# unifica os textos de cada bloco e salva o número da página, nome do arquivo e a data

							if len(txt_block) > 0:
								txt_fim = " ".join(txt_block)
								txt_unific.append(txt_fim)
								numeros_paginas.append(num_pag)
								nomes_pastas.append(nome_pasta[-10:])
								nome_doc.append(arquivos[a])
							

							# PARA CONFERÊNCIA - DESCOMENTAR CASO QUEIRA VERIFICAR O CORTE DAS PUBLICAÇÕES (por seção)- APERTAR ENTER A CADA PUBLICAÇÃO
							#### esse corte é o da estrutura do PDF - a separação é feita por outra função

							# print('Pasta:',nome_pasta[-10:]," --- ", 'arquivo:', arquivos[a])
							# print("Estamos na página:", num_pag)
							# print("No bloco número:",o,"num total de", len(blocks))
							# print("Publicação:")
							# print(txt_fim)
							# print("------------------------\n")
							# z = input("")
							
										
						except:
							sem_lines.append(blocks[o]["number"])	

	# print('Tinhamos', len(txt_unific))						
	Juntar_blocks(numeros_paginas,nome_doc, nomes_pastas, txt_unific)								
	return numeros_paginas,	nome_doc, nomes_pastas, txt_unific
	

###############################################################################

###### Função para separar, unificar e selecionar as publicações de interesse e Gerar um Banco de dados em excel #########

def Juntar_blocks(numeros_paginas,nome_doc, nomes_pastas, txt_unific):


	publicacoes = []
	num_pags = []
	nome_docs = []
	nome_pst = []
	x = 0



	for txt,num,doc,pst in zip(txt_unific,numeros_paginas,nome_doc,nomes_pastas):
		
	
		# caso encontra a o padrão CNJ na publicação ele separa a publicação, o número da página, documento e pasta.
		# pelo problema acima do encoding relatado acima adotei o regex somente da parte final do padrão CNJ (ex: 42.2021.8.11.0000)
		
		if re.search(r'\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}',txt, re.IGNORECASE.MULTILINE): # pesquisa o padrão em todas as linhas da publicação
			# print(txt)
			publicacoes.append(txt) 
			num_pags.append(num)
			nome_docs.append(doc)
			nome_pst.append(pst)
			x = 0 # contador da quantidade de unificações sem encontrar o padrão CNJ. Quando ele encontra a contagem é zerada


	
		# caso ele não encontre o padrão CNJ e essa publicação não seja a primeira da lista 
		else:
			if x <= 4 and len(publicacoes)>=1 and re.search("^Publicação Oficial do Tribunal de Justiça",txt,re.IGNORECASE) == None: #verifica se atingiu a quantidade máxima de unificações (4) sem encontrar um padrão CNJ ou se é a primeira da lista
				txt = publicacoes[-1]+" "+txt  # unifica o texto atual com a publicação anterior
				del publicacoes[-1] # deleta da lista a publicação anterior
				publicacoes.append(txt) # junta a nova publicação unificada na lista (o número da página e o nome do doc se mantém onde a publicação começa)
				x = x+1 # soma 1 no controle da quatidade de vezes seguidas que unificou sem achar o padrão CNJ
			
			# se atingiu as 4 seguidas ou é o primeiro elemento da lista das publicações ele abandona aquela publicação
			else:
				pass 



# PARA CONFERÊNCIA - DESCOMENTAR CASO QUEIRA VERIFICAR O CORTE FINAL DAS PUBLICAÇÕES - APERTAR ENTER A CADA PUBLICAÇÃO
	# print('temos',len(publicacoes))
	# for item,num in zip(publicacoes,num_pags):
	# 	print("página", num)
	# 	print(item)
	# 	print("-----------------")
	# 	z = input('')


	df_textos_paginas = pd.DataFrame()    
	df_textos_paginas["publicacoes"] = publicacoes
	df_textos_paginas["numeros_paginas"] = num_pags
	df_textos_paginas["nome_documento"] = nome_docs
	df_textos_paginas["nomes_pastas"] = nome_pst	

	df_textos_paginas.to_excel("Diarios_publicacoes_MS_"+ano+".xlsx", index = False)



################################################################################################################

def Main_Separacao():
	ano = input("Digite o ano com 4 dígitos (Ex:2012):")
	data_frames = Separar_textos_paginas(ano)

################################################################################################################


Main_Separacao()