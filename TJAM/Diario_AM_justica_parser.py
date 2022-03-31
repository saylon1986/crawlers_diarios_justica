# Imports de bibliotecas
import pandas as pd
from tqdm import tqdm
from PyPDF2 import PdfFileReader, PdfFileMerger
import os, re
import fitz




############################## função para cortar os textos dos diários ####################################################



def Separar_textos_paginas():

	# seleciona a pasta de acordo com o ano
	anos_di = input("Digite o ano(ex: 2003):")
	diret = r'.\Diarios_AM_'+anos_di


	# listas as pastas
	pastas = os.listdir(diret)


	# prepara as listas com os valores a serem usados
	numeros_paginas =[]
	nome_doc = []
	nomes_pastas =[]
	vlrs_unific= [] # lista que salva os valores que identificam os parágrafos
	txt_unific = []
	sem_lines = []


	# iteração sobre os arquivos dentro das pastas

	for b in tqdm(range(len(pastas))):
		nome_pasta = os.path.join(diret, pastas[b])
		arquivos = os.listdir(nome_pasta)
		for a in range(len(arquivos)):
			print(arquivos[a])
			nome = os.path.join(nome_pasta, arquivos[a])


			num_pag = 0 # inicio da contagem da página

			with fitz.open(nome) as pdf:
				for pagina in pdf:
					num_pag = num_pag + 1
					blocks = pagina.getText("dict")['blocks'] # organiza o texto na forma de dict e separa nas seções do documento

					# itera para cada seção

					for o in range(len(blocks)):

						# só faz isso para as seções que possuem a subseção "lines"		
						try:
							lines = blocks[o]["lines"]

								# itera para cada linha

							for x in range(len(lines)):

								# dentro das linhas seleciona os spans

								spans = lines[x]["spans"]
								
								# para cada spam:

								for u in spans:
									te = str(u['bbox'][0]) # seleciona o valor do parágrafo
									ta = te.split(".") # corta no decimal
									dist = int(ta[0]) # separa apenas os primeiros dígitos antes do ponto
									vlrs_unific.append(dist) # coloca esse valor na lista
									txt_unific.append(u['text'].strip()) # coloca também o texto na lista
									numeros_paginas.append(num_pag) # salva o número da página desse texto
									nomes_pastas.append(nome_pasta) # salva o nome da pasta 
									nome_doc.append(arquivos[a]) # salva o nome do documento
						
						# caso não tenha a seção lines salva nessa outra lista o número do bloco (sem utilidade)
						except:
							sem_lines.append(blocks[o]["number"])


	# função que faz a junção dos blocos com base no valor do parágrafo

	Juntar_blocks(numeros_paginas,nome_doc, nomes_pastas, vlrs_unific, txt_unific)								
	
	# retorna as listas (antes de fazer a junção)
	# return numeros_paginas, nome_doc, nomes_pastas, vlrs_unific, txt_unific
	


###############################  Função para juntar os blocos dos textos ################################################

def Juntar_blocks(numeros_paginas,nome_doc, nomes_pastas, vlrs_unific, txt_unific):

		#listas com os valores a serem aproveitados
		prgf = [] # index da lista com os textos das publicações que são parágrafos


		for k in range(len(vlrs_unific)): # itera sobre a lista com os valores dos parágrafos
			if vlrs_unific[k] == 70 or vlrs_unific[k] == 316 or vlrs_unific[k] == 317: # se forem estes valores (valores dos parágrafos)
				pos = vlrs_unific.index(vlrs_unific[k],k) # verifica o index daquele elemento, sempre começando a buscar a partir dele na lista 
				prgf.append(pos) # coloca o index numa lista

		
		# listas com os dados finais a serem incluídos no BD

		publicacoes = [] 
		num_paginas= []		
		nom_pastas = []
		nom_docs = []
		

		# itera sobre a lista com os index dos parágrafos

		z = 0
		while True:

			if z >= len(prgf)-1:
				break
			else:

				atual = prgf[z] # recebe o index do primeiros
				seguinte = prgf[z+1] # recebe o index do segundo


				if seguinte == atual+1: # se o segundo for consecutivo do primeiro
					# print(atual, seguinte,"são consecutivos! O z valia",z)
					# s = input("")

					while True: 
					
						z = z+1 # z aumenta um elemento
						teste = prgf[z] # teste recebe novo elemento
						if z >= len(prgf)-1:
							break
						else:
							seguinte = prgf[z+1] # #seguinte recebe o elemento seguinte ao anterior
							# print(teste,seguinte,"são os atuais. O Z vale",z)
							if teste+1 != seguinte: # verifica se ainda são consecutivos
								# print("acabaram os consecutivos")
								# print("o atual será cortado", atual,"e o seguinte será cortado em", 
								# 	seguinte)
								# s = input("")
								break 


					publi = txt_unific[atual:seguinte] # corta a lista entre esses elementos
					txt_publi = " ".join(publi) #unifica os textos nesse intervalo

					# if len(txt_publi) > 150: # eliminar parágrafos e outras coisas que não são publicações
					publicacoes.append(txt_publi) # salva o texto da publicação
					num_paginas.append(numeros_paginas[atual]) # o número da pagina onde começa
					nom_pastas.append(nomes_pastas[atual][-10:]) # o nome da pasta
					nom_docs.append(str(nome_doc[atual])) # e do documento
					z = z+1


				else:
					publi = txt_unific[atual:seguinte] # corta a lista entre esses elementos
					txt_publi = " ".join(publi) #unifica os textos nesse intervalo

					# if len(txt_publi) > 150: # eliminar parágrafos e outras coisas que não são publicações
					publicacoes.append(txt_publi) # salva o texto da publicação
					num_paginas.append(numeros_paginas[atual]) # o número da pagina onde começa
					nom_pastas.append(nomes_pastas[atual][-10:]) # o nome da pasta
					nom_docs.append(str(nome_doc[atual])) # e do documento
					z = z+1


		### conferir o número das páginas		

		# for item in publicacoes:
		# 	print("------------------------")
		# 	print(item)
		# 	s = input("")



		# Transforma num DF		

		df_textos_paginas = pd.DataFrame()    
		df_textos_paginas["publicacoes"] = publicacoes
		df_textos_paginas["numeros_paginas"] = num_paginas
		df_textos_paginas["nome_documento"] = nom_docs
		df_textos_paginas["nomes_pastas"] = nom_pastas	

		try:
			antigos = pd.read_excel("Diarios_publicacoes.xlsx", engine ='openpyxl')
			# print("já temos uma planilha!")
			df_textos_paginas = pd.concat([antigos,df_textos_paginas])
			df_textos_paginas.to_excel("Diarios_publicacoes.xlsx", index = False)
		except:
			df_textos_paginas.to_excel("Diarios_publicacoes.xlsx", index = False)
		
	



################################################################################################################

def Main_Separacao():

	data_frames = Separar_textos_paginas()

################################################################################################################


Main_Separacao()