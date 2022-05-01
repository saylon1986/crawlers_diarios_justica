# Imports de bibliotecas
import pandas as pd
from tqdm import tqdm
from PyPDF2 import PdfFileReader, PdfFileMerger
import os, re
import fitz
import random
import json
from array_Estados import Comarcas
from tipos_processuais import tipos_processuais
from assuntos import assuntos_proc


############################## função para separar os representantes (AOB/Estado) ####################################################

def sep_representante(public):

	rgx_estad = "(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO|DP)"

	# limpar o texto do ponto para separar melhor o número da OAB
	text_ajust = public.replace(".","")
	text_ajust = text_ajust.replace("\n","")
	# print(text_ajust)


	oabs = []
	# print(public)

	oab_compile = re.compile("\d{3,10}(?:[A-Z]/|/.|/|[A-Z]/.)[A-Z][A-Z]")
	oab_comp = oab_compile.findall(public)
	# print(len(oab_comp))
	# z=input("")
	if len(oab_comp) > 0:
		for item in oab_comp:
			oabs.append(item)
	else:
		partes = re.split("oab",text_ajust, flags=re.IGNORECASE)[1:]
		# print(partes)
		# z=input("")
		for item in partes:
			item = item.strip()
			try:
				# print("o item é:\n",item[:10],"\n ***************")
				num_oab = re.findall('\d{3,10}',item[:14])
				estado_oab = re.findall(rgx_estad,item[:14])
				# print("a OAB é:",num_oab,"\nE o Estado é:",estado_oab,"\n ----------------")
				oabs.append(str(num_oab[0]+"/"+estado_oab[0]))
			except:
				try:
					# print("o item é:\n",item[:],"\n ***************")
					num_oab = re.findall('\d{3,10}',item[:])
					estado_oab = re.findall(rgx_estad,item[:])
					# print("a OAB é:",num_oab,"\nE o Estado é:",estado_oab,"\n ----------------")		
					oabs.append(str(num_oab[0]+"/"+estado_oab[0]))
				except:
					pass
	

	# print(oabs)
	return oabs


############################## função para classificar os tipos processuais e as comarcas ####################################################

	
def classificacao_quali(planilha):


	comarcas = []
	tipos_proces =[]
	oabs =[]
	assuntos =[]

	# recebe as listas do arrays dos tipos processuais e dos assuntos

	termos = tipos_processuais()
	assuntos_list = assuntos_proc()

	for public,num,est in tqdm(zip(planilha["publicacao"],planilha["numero_processo"],planilha["estado"])):
		
		
		###### parte de verificar os tipos processuais 
		try:
			# docum = open("teste_2.txt", encoding ="utf-8")
			# public = docum.read()
			# print(public[6].encode())
			publis = re.sub(r"\n"," ",public)# eliminar as quebras de linhas para pontecializar o regex
			# print(publis)
			# z = input("")
			# procurar apenas no começo da publicação
	

			if len(publis) <= 1000: # se a publicação tiver até 1000 caracteres, procura no texto todo
				publis = publis
				# public_pt_final = publis 
			else:	
				vlr = int(len(publis)*0.10)
				if vlr < 350: # se tiver mais de mil até 3500, procura nos 350 primeiro caracteres
					vlr = 350
				publis = publis[0:vlr] # fora isso, pesquisar nos 10% primeiros caracteres da publicação
				# public_pt_final = publis[vlr:] # ou nos 10% no caso da variável da data da decisão
			
			trecho_publis = publis.lower()
			# print(trecho_publis)

			tipo = "" # tipo recebe valor em branco

			# itera sobre o dicionário de tipos processuais
			for n in range(len(termos)):
				rgx = termos [n]
				rgx = re.sub(r"\n"," ",rgx)
				# tenta encontrar o tipo na publicação
				try:
					if re.search(rgx, trecho_publis, re.IGNORECASE): 
						tipo = termos[n]# se encontrar normaliza para minúscula e grava na variável
						# print(tipo)
						break
				except:
					pass

			# junta o a variável tipo na lista		
			tipos_proces.append(tipo.strip())
			# z=input("")
			

		# em caso de erro também insere o vazio 
		except:
			tipo = ""
			tipos_proces.append(tipo)
			


		########## assunto ##################	
		try:
			assunto = "" # tipo recebe valor em branco


			# itera sobre o dicionário de tipos processuais
			for l in range(len(assuntos_list)):
				rgx_as = assuntos_list[l]
				rgx_as = re.sub(r"\n"," ",rgx_as) #elimina eventuais quebras de linhas no regex tbem
				
				if re.search("assunto:",trecho_publis,re.MULTILINE):
					quebras = re.split("assunto:",trecho_publis)
					trecho_publis = quebras[1][:50]
				
				# tenta encontrar o tipo na publicação
				try:
					if re.search(rgx_as, trecho_publis, re.IGNORECASE): 
						assunto = assuntos_list[l] # se encontrar normaliza para minúscula e grava na variável
						# print(assunto,rgx_as, l)
						# z=input("")
						break
				except:
					pass

			# junta o a variável tipo na lista		
			assuntos.append(assunto)
		

		# em caso de erro também insere o vazio 
		except:
			assunto = ""
			assuntos.append(assunto)


	########### Parte de inserir a comarca
		try:
			# recebe o código e o Estado
			codigo = num[-4:]
			estado = est
			array_estado = Comarcas(estado) # retorna o array do Estado na função

			# itera no array do Estado até achar o código da comarca, caso não encontre insere o vazio por default
			for k in range(len(array_estado)):
				comarca = ""
				if array_estado[k][0] == codigo:
					comarca = array_estado[k][2]
					break
			comarcas.append(comarca)

		# em caso de algum erro insere o vazio
		except:
			comarca = ""
			comarcas.append(comarca)

		####### parte de buscar os advogados

		oab = sep_representante(public)
		oabs.append(oab) 

	
	# print("Temos",total, "não classificados.\n O total é",len(planilha["publicacoes"]),
	# 	"\n o percentual é",(total*100)/len(planilha["publicacoes"]))


	planilha ["tipos_processuais"] = tipos_proces
	planilha["comarcas"] = comarcas
	planilha["representantes"] = oabs
	planilha["assuntos"] = assuntos

	return planilha

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

	## lista para verificar as flags escolhidas
	caracteristicas =[]

	cabecalhos =[]

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
							cabec =[]	
					
							for x in range(len(lines)):
								spans = lines[x]["spans"] # separa os spans
								for u in spans:
									tam = str(u['size']).split(".")[0]
									flag =str(u['flags'])


									## para o teste previo de verificar as flags
									caracteristicas.append((tam,flag))

									if tam == "8" and flag == "0" or tam == "8" and flag =="16": 
										txt_block.append(u['text'].strip()) # separa todos os textos de cada bloco e salva na lista para unificação
										if tam == "8" and flag =="16": # se for o cabeçalho
											cabec.append((u['text'].strip())) # separa numa lista específica
								
									## para verificar o que aparece nos padrões das flags
							
									# if tam == "5" and flag == "0":
									# 	print("\n\n PADRÃO 2\n\n",u['text'])
									# 	z = input("")
									# elif tam == "8" and flag == "0":
									# 	print("\n\n PADRÃO 3\n\n",u['text'])	
									# 	z = input("")
									# elif tam == "5" and flag == "0":
									# 	print("\n\n PADRÃO 4\n\n",u['text'])	
									# 	z = input("")
							

							# unifica os textos de cada bloco e salva o número da página, nome do arquivo, a data e o cabeçalho separado

							if len(txt_block) > 0:
								txt_fim = " ".join(txt_block)
								txt_unific.append(txt_fim)
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
								
							if len(cabec) > 0:	
								cabecalhos.append(cabec[0])
							else:
								cabec =[" "]
								cabecalhos.append(cabec[0])
										
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


	Juntar_blocks(numeros_paginas,nome_doc, nomes_pastas, txt_unific,ano, cabecalhos)								
	return numeros_paginas,	nome_doc, nomes_pastas, txt_unific
	

###############################################################################

###### Função para separar, unificar e selecionar as publicações de interesse e Gerar um Banco de dados em excel #########

def Juntar_blocks(numeros_paginas,nome_doc, nomes_pastas, txt_unific,ano, cabecalhos):


	publicacoes = []
	num_pags = []
	nome_docs = []
	nome_pst = []
	num_process =[]
	x = 0



	for txt,num,doc,pst,cab in zip(txt_unific,numeros_paginas,nome_doc,nomes_pastas,cabecalhos):

		## regra da pesquisa do número CNJ dentro do texto da publicação

		if len(txt) <= 1000: # se a publicação tiver até 1000 caracteres, procura no texto todo
			text = txt
		else:	
			vlr = int(len(txt)*0.10)
			if vlr < 400: # se tiver mais de mil até 4000, procura nos 4000 primeiro caracteres
				vlr = 400
			text = txt[0:vlr] # fora isso, pesquisar nos 10% primeiros caracteres da publicação


		## incício da busca

		
		if re.search('\d{2,7}(?:-|.{2}).\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}',text, re.IGNORECASE.MULTILINE): # pesquisa o padrão em todas as linhas da publicação (dentro do limite de caracteres)
			nm_proc = re.search('\d{2,7}(?:-|.{2}).\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}',text, re.IGNORECASE.MULTILINE).group().replace(" ","") # se encontrar o padrão completo, separa o número
			num_process.append(nm_proc) # salva na lista
			

			# salva nas listas a publicação e as demais informações dela (página, documento, pasta)	
			publicacoes.append(txt) 
			num_pags.append(num)
			nome_docs.append(doc)
			nome_pst.append(pst)
			
	
		# caso ele não encontre o padrão CNJ e essa publicação não seja a primeira da lista 
		else:
		
			if len(publicacoes)>=1 and re.search("^Disponibilizado -",txt,re.IGNORECASE) == None: #verifica se atingiu a quantidade máxima de unificações (4) sem encontrar um padrão CNJ ou se é a primeira da lista
				txt = publicacoes[-1]+" "+txt  # unifica o texto atual com a publicação anterior
				del publicacoes[-1] # deleta da lista a publicação anterior
				publicacoes.append(txt) # junta a nova publicação unificada na lista (o número da página e o nome do doc se mantém onde a publicação começa)
					
			else:
				pass
		
		


	###### PARA CONFERÊNCIA - DESCOMENTAR CASO QUEIRA VERIFICAR O CORTE FINAL DAS PUBLICAÇÕES NA ORDEM - APERTAR ENTER A CADA PUBLICAÇÃO
	# qtdade = 0
	# for item,num in zip(publicacoes,num_pags):
	# 	qtdade = qtdade+1
	# 	print("Quantidade avaliada:",qtdade)
	# 	print("página", num)
	# 	print(item)
	# 	print("-----------------")
	# 	z = input('')
	##################   FIM DO TRECHO PARA CONFERÊNCIA ##############################


	# gera o DF com as publicações e as demais informações

	df_textos_paginas = pd.DataFrame()
	df_textos_paginas["numero_processo"] = num_process
	df_textos_paginas["publicacao"] = publicacoes
	df_textos_paginas["numeros_paginas"] = num_pags
	df_textos_paginas["nome_documento"] = nome_docs
	df_textos_paginas["nomes_pastas"] = nome_pst
	df_textos_paginas["estado"] = "MS"	

	


	############ CONFERÊNCIA AMOSTRAL ALEATÓRIA - DESCOMENTAR CASO QUEIRA UMA AMOSTRA ALEATÓRIA DOS RECORTES  - APERTAR ENTER A CADA PUBLICAÇÃO


	# # # agrupa por nome do documento
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

	##################   FIM DO TRECHO PARA CONFERÊNCIA ##############################


	df_textos_paginas = classificacao_quali(df_textos_paginas)

	frag = df_textos_paginas["nomes_pastas"].str.split("-", n=2, expand = True)
	df_textos_paginas["dia"] = frag[0]
	df_textos_paginas["mes"] = frag[1]
	df_textos_paginas["ano"] = frag[2]

	df_textos_paginas["data_decisao"] = ""
	df_textos_paginas["orgao_julgador"] = ""

	df_textos_paginas = df_textos_paginas[["numero_processo", "estado","publicacao","numeros_paginas","tipos_processuais","assuntos","comarcas",
	"representantes","dia", "mes","ano","nome_documento","nomes_pastas","data_decisao","orgao_julgador"]]

	# gera o excel com o DF final

	df_textos_paginas.to_excel("Diarios_publicacoes_MS_"+ano+".xlsx", index = False)

	# converte para JSON

	result = df_textos_paginas.to_json(orient="records", force_ascii = False)
	parsed = json.loads(result)
	with open('data_MS_'+ano+'.json', 'w', encoding ='utf-8') as fp:
		json.dump(parsed, fp)

	# time.sleep(5)	

	# with open('data_AM.json', 'r', encoding ='utf-8') as fp:
	# 	data = json.loads(fp.read())
	# 	print(json.dumps(data, indent = 4, ensure_ascii=False))

	# print(json.dumps(parsed, ensure_ascii=False, indent=4)) 



################################################################################################################

def main():
	ano = input("Digite o ano com 4 dígitos (Ex:2012):")
	data_frames = Separar_textos_paginas(ano)

################################################################################################################


if __name__ == "__main__":
	main()