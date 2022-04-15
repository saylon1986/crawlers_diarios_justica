# Imports de bibliotecas
import pandas as pd
from tqdm import tqdm
from PyPDF2 import PdfFileReader, PdfFileMerger
import os, re
import fitz
import random



##################################################################################################

							# Função para separar os textos das publicações

def Separar_textos_paginas(ano):

	# diretório com as pastas e os dados

	diret = r'./Diarios_MT_'+ano

	pastas = os.listdir(diret)


	# listas que receberão os dados

	numeros_paginas =[]
	nome_doc = []
	nomes_pastas =[]
	txt_unific = []
	sem_lines = []

	## lista para verificar as flags escolhidas
	caracteristicas =[]

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
					# print("\n\n\n Estamos na página",num_pag,"\n\n\n\n documento:",arquivos[a],"\n\n\n Na pasta:",nome_pasta,"\n\n\n")
					
					blocks = pagina.getText("dict")['blocks'] # método que divide o texto em blocos no formato dict
	
				
					for o in range(len(blocks)):
											
						# print(blocks[o])
						# z= input("")
						try: # elimina os blocos que não contém "lines" e consequentemente não tem textos
							
							lines = blocks[o]["lines"] # separa as linhas
							
							txt_block = []	
							
							for x in range(len(lines)):
								spans = lines[x]["spans"] # separa os spans
								
								for u in spans:
									tam = str(u['size']).split(".")[0]
									flag =str(u['flags'])

									## para o teste previo de verificar as flags	
									caracteristicas.append((tam,flag)) 
									
									if tam == "7" and flag == "0" or tam == "7" and flag =="16" or tam =="10" and flag == "0": 
										txt_block.append(u['text'].strip()) # separa todos os textos de cada bloco e salva na lista para unificação
								

									## para verificar o que aparece nos padrões das flags
							
									# if tam == "9" and flag == "4":
									# 	print("\n\n PADRÃO 2\n\n",u['text'])
									# 	z = input("")
									# # if tam == "9" and flag == "4":
									# 	print("\n\n PADRÃO 3\n\n",u['text'])	
									# 	z = input("")

							# unifica os textos de cada bloco e salva o número da página, nome do arquivo e a data
							if len(txt_block) > 0:
								txt_fim = " ".join(txt_block)
								txt_unific.append(str(txt_fim))
								numeros_paginas.append(num_pag)
								nomes_pastas.append(nome_pasta[-10:])
								nome_doc.append(arquivos[a])

							# caso o texto do bloco seja vazio, unifica um texto vazio para manter a mesma quantidade d eitens da lista
							else:
								txt_fim = " "
								txt_unific.append(txt_fim)
								numeros_paginas.append(num_pag)
								nomes_pastas.append(nome_pasta[-10:])
								nome_doc.append(arquivos[a])


					
							

						# se não tiver as linhas, salva em outra lista - somente para conferência, não tem utilidade.					
						
						except:
							sem_lines.append(blocks[o]["number"])



	## contabilização da quantidade de flags mais frequentes
							
	# nome_acao = pd.DataFrame()
	# nome_acao["Ação"] = caracteristicas							
	# nome_acao = pd.DataFrame(nome_acao.groupby(["Ação"])["Ação"].count())
	# nome_acao.columns = ["quantidade"]
	# nome_acao = nome_acao.reset_index()						

	# print(nome_acao.sort_values(by=['quantidade'],ascending=False))
	# z = input("")

	
	Juntar_blocks(numeros_paginas,nome_doc, nomes_pastas, txt_unific, ano)								
	return numeros_paginas,	nome_doc, nomes_pastas, txt_unific
	

###############################################################################

 			###### Função para separar, unificar e selecionar as publicações de interesse e Gerar um Banco de dados em excel #########


def Juntar_blocks(numeros_paginas,nome_doc, nomes_pastas, txt_unific,ano):

	num_process =[]
	publicacoes = []
	num_pags = []
	nome_docs = []
	nome_pst = []
	



	for txt,num,doc,pst in zip(txt_unific,numeros_paginas,nome_doc,nomes_pastas):
		
		####        identifiquei esse problema de encoding do traço (-) no texto em alguns números cnj no pdf, o que enganava o regex  #########

								
											#  Número:  1001461­41.2022.8.11.0000 

								
										########                                 ###########

		
		# caso encontra a o padrão CNJ na publicação ele separa a publicação, o número da página, documento e pasta.
		# pelo problema acima do encoding relatado acima adotei o regex somente da parte final do padrão CNJ (ex: 42.2021.8.11.0000)


		## regra da pesquisa do número CNJ dentro do texto da publicação

		if len(txt) <= 1000: # se a publicação tiver até 1000 caracteres, procura no texto todo
			text = txt
		else:	
			vlr = int(len(txt)*0.10)
			if vlr < 350: # se tiver mais de mil até 3500, procura nos 350 primeiro caracteres
				vlr = 350
			text = txt[0:vlr] # fora isso, pesquisar nos 10% primeiros caracteres da publicação


		## incício da busca

		if re.search(r'\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}',text, re.IGNORECASE.MULTILINE): # pesquisa o padrão em todas as linhas da publicação (dentro do limite de caracteres)
			try:
				nm_proc = re.search(r'\d{2,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}',text, re.IGNORECASE.MULTILINE).group() # se encontrar o padrão completo, separa o número
				num_process.append(nm_proc) # salva na lista

			# se encontrou so o padrão parcial por causa do problema acima
			except:
				posic = re.search(r'\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}',text, re.IGNORECASE.MULTILINE).span() # pega os caracter do início e o fim do padrão parcial 
				
				# se o número do caracter não foi menor do que o início da publicação
				if posic [0] - 10 >= 0:
					trecho = text[posic [0] - 10:posic[1]].strip() # separa o trecho voltando 10 caracteres do início encontrado (a parte inicial do nº cnj tem até 7 digitos)
				else:
					# se for menor e houve algum erro na quebra da página, recebe o número parcial mesmo
					trecho =  re.search(r'\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}',text, re.IGNORECASE.MULTILINE).group()

				nm_proc = re.search('(\d.*\.\d{4})',trecho).group() # elimina eventuais sobras de texto que tenham sido captadas
				num_process.append(nm_proc)  # salva na lista o número limpo

			# salva nas listas a publicação e as demais informações dela (página, documento, pasta)	
			publicacoes.append(txt) 
			num_pags.append(num)
			nome_docs.append(doc)
			nome_pst.append(pst)


			## comparação das duas últimas publicações:
			if len(num_process) >= 2: # só da pra fazer isso depois que tivermos pelo menos dois números na lista
				ultimo = num_process[-1]
				penultimo = num_process [-2]
				if ultimo == penultimo: # se as duas tiverem o mesmo número CNJ
					unif = publicacoes[-2]+' '+publicacoes[-1] #unifica as duas na penúltima
					
					#deleta tudo da última publicação inserida
					del num_process [-1] 
					del publicacoes [-1]
					del num_pags [-1]
					del nome_docs [-1]
					del nome_pst [-1]		
	
	
		# caso ele não encontre o padrão CNJ e essa publicação não seja a primeira da lista 
		else:
			if len(publicacoes)>=1 and re.search("^Disponibilizado -",txt,re.IGNORECASE) == None: #verifica se atingiu a quantidade máxima de unificações (4) sem encontrar um padrão CNJ ou se é a primeira da lista
				txt = publicacoes[-1]+" "+txt  # unifica o texto atual com a publicação anterior
				del publicacoes[-1] # deleta da lista a publicação anterior
				publicacoes.append(txt) # junta a nova publicação unificada na lista (o número da página e o nome do doc se mantém onde a publicação começa)
				
		


# PARA CONFERÊNCIA - DESCOMENTAR CASO QUEIRA VERIFICAR O CORTE FINAL DAS PUBLICAÇÕES NA ORDEM - APERTAR ENTER A CADA PUBLICAÇÃO
	# qtdade = 0
	# for item,num in zip(publicacoes,num_pags):
	# 	qtdade = qtdade+1
	# 	print("Quantidade avaliada:",qtdade)
	# 	print("página", num)
	# 	print(item)
	# 	print("-----------------")
	# 	z = input('')



	# gera o DF com as publicações e as demais informações

	df_textos_paginas = pd.DataFrame()
	df_textos_paginas["Número do processo"] = num_process
	df_textos_paginas["publicacoes"] = publicacoes
	df_textos_paginas["numeros_paginas"] = num_pags
	df_textos_paginas["nome_documento"] = nome_docs
	df_textos_paginas["nomes_pastas"] = nome_pst	

	


	### CONFERÊNCIA AMOSTRAL ALEATÓRIA - DESCOMENTAR CASO QUEIRA UMA AMOSTRA ALEATÓRIA DOS RECORTES  - APERTAR ENTER A CADA PUBLICAÇÃO


	# # agrupa por nome do documento
	# doc_agrup = pd.DataFrame(df_textos_paginas.groupby(["nome_documento"])["nome_documento"].count())
	# doc_agrup.columns = ["quantidade"]
	# doc_agrup = doc_agrup.reset_index()

	# # converte os nomes em uma lista e depois embaralha os nomes em uma ordem indeterminada
	# lista_nomes_docs = doc_agrup["nome_documento"].tolist()
	# random.shuffle(lista_nomes_docs)


	# # Gera uma amostra aleatória de X publicações por documento para facilitar a conferência
	# for docu in lista_nomes_docs :
	# 	df_filter = df_textos_paginas["nome_documento"] == docu
	# 	amostra_trib = df_textos_paginas[df_filter]

	# 	amostra_trib = amostra_trib.sample(10)  # escolher a quantidade da amostra
	# 	for pub,doc,pag in zip(amostra_trib["publicacoes"],amostra_trib["nome_documento"],amostra_trib["numeros_paginas"]):
	# 		print("documento:\t",doc,"\nPágina:\t",pag,"\nTexto publicação:\n",pub,"\n--------------")
	# 		z= input("")





	# gera o excel com o DF final

	df_textos_paginas.to_excel("Diarios_publicacoes_MT_"+ano+".xlsx", index = False)



########################################      Funçao principal    ########################################################################

def Main_Separacao():

	ano = input("digite o ano com 4 dígitos (ex: 2016):") # escolhe o ano para iniciar o processo
	data_frames = Separar_textos_paginas(ano)

################################################################################################################


Main_Separacao()