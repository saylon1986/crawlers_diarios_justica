import re,os
import pandas as pd
import jellyfish
from tqdm import tqdm
import glob
from array_Estados import Comarcas


def gera_dict():

	planilha = pd.read_excel("Diarios_publicacoes.xlsx", engine ='openpyxl')


	nomes_processuais =[]
	for item in planilha["Publicação"]:
		try:
			partes = item.split("-")
			txt = [partes[2]]#, partes[3]]
			for p in txt:
				if re.search('\d|:', p) == None:
					nomes_processuais.append(p.strip())
					# print(txt)
					# z=input("")
		except:
			pass



	dicion = pd.DataFrame()
	dicion ["Termos Processuais"] = nomes_processuais

	# print(dicion)

	contagem = pd.DataFrame(dicion.groupby(["Termos Processuais"])["Termos Processuais"].count())
	contagem.columns = ["quantidade"]
	contagem = contagem.reset_index()

	# print(contagem)


	# contagem_ajus =contagem.sort_values(by=['quantidade'],ascending=False,ignore_index=True)

	# print(contagem_ajus)

	dicion.drop_duplicates(subset=["Termos Processuais"], inplace= True)

	# print(len(dicion))

	dicion = dicion.merge(contagem, on = "Termos Processuais", how = "left").dropna()


	dicion.sort_values(by=['quantidade'],ascending=False,ignore_index=True, inplace=True)

	print(dicion)

	dicion.to_excel("Termos_processuais.xlsx", index = False)




def juntar_iguais(indexes, planilha):

	deletar = []

	for k in range(len(indexes)):


		# print("o valor era", planilha["quantidade"] [indexes[k][0]])
		# print("o segundo valor é", planilha["quantidade"][indexes[k][1]])
		planilha["quantidade"][indexes[k][0]] = planilha["quantidade"][indexes[k][0]] + planilha["quantidade"][indexes[k][1]] 
		# print("o valor é", planilha["quantidade"][indexes[k][0]])
		deletar.append(indexes[k][1])
		# z= input("")

	for item in deletar:
		planilha.drop(index = item, inplace=True)

	# print(planilha)


	return planilha





def limpar_dict():

	planilha = pd.read_excel("Termos_processuais_dicionario.xlsx", engine ='openpyxl')

	planilha ["Termos Processuais"] = planilha ["Termos Processuais"].str.lower().str.strip().str.replace("\n","")

	planilha = pd.DataFrame(planilha.groupby(["Termos Processuais"])["Termos Processuais"].count())
	planilha.columns = ["quantidade"]
	planilha = planilha.reset_index()

	
	
	indexes =[]
	for n in range(len(planilha["Termos Processuais"])):
		text = planilha["Termos Processuais"][n].strip()
		for z in range(n+1,len(planilha["Termos Processuais"])):
			text_2 = planilha["Termos Processuais"][z].strip()
			valor = jellyfish.jaro_distance(text, text_2)
			if valor >= 0.95:
				print(valor)
				print("o texto é:    *",text, "*      na posição", n)
				print("é semelhante ao:    *", text_2, "*       na posição",z)
				x = input("deseja juntar?")
				if x == "s":
					indexes.append(z)


	print(planilha)					

	for item in indexes:
		try:
			planilha.drop(index=item, inplace=True)
		except:
			pass





	print(planilha)

	# planilha.drop_duplicates(subset=["Termos Processuais"], inplace= True)

	# print(planilha)

	planilha.to_excel("Termos_limpos.xlsx", index = False)

# limpar_dict()


###########################

def separar_tipos_acao():

	termos = pd.read_excel("Termos_limpos_dicionario.xlsx", engine ='openpyxl')
	planilha = pd.read_excel("Diarios_publicacoes.xlsx", engine ='openpyxl')

	tipos_proces =[]
	total=0
	for z in tqdm(range(len(planilha["Publicação"]))):
		publis = planilha["Publicação"][z]
		publis = publis.replace("\n","")
		# print(publis.encode())
		# s= input("")
		tipo = "" 
		for n in range(len(termos["Termos Processuais"])):
			rgx = termos ["Termos Processuais"][n]
			rgx = rgx.replace("\n","")
			# print("estamos na publis",z,"testando o termo",rgx)
			try:
				if re.search(rgx, publis, re.IGNORECASE): 
					tipo = re.search(rgx, publis, re.IGNORECASE).group()
					tipo = tipo.lower()
					# print(tipo)
					break
			except:
				pass		
		# print("juntando", tipo)	
		# s = input("")
		tipos_proces.append(tipo)
		if tipo =="":
			total = total+1
		# print("-----------------")


	print("Temos", total, "não classificados")
	planilha ["Tipos processuais"] = tipos_proces

	print(planilha)

	# print(len(tipos_proces))
	# print(tipos_proces)	
	planilha.to_excel("Publis_c_tipos_process.xlsx", index = False)


# separar_tipos_acao()

###################################################################################

def Encontrar_data_decisao(trecho_publis):

	regex_meses = '(janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)'
	# tenta achar o nome do mês no formato da data na publicação
	if re.search(regex_meses, trecho_publis,re.IGNORECASE) != None:
		num_caract = re.search(regex_meses, trecho_publis,re.IGNORECASE).span()
		dt_ext = trecho_publis[num_caract[0]-8:num_caract[1]+10]
		if re.search("\)", dt_ext):
			print("data errada")
		else:
			print(" ********  ")
		print(dt_ext)
		print(trecho_publis)
		z = input("")
	
####################################################################################

def sep_representante(public):
# def sep_representante():

	rgx_estad = "(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO|DP)"

	# limpar o texto do ponto para separar melhor o número da OAB
	# public = "De ordem do Exmo. Sr. Des. Elci Simões de Oliveira - Relator nos autos Eletrônicos de Agravo de Instrumento nº 4006094- 78.2018.8.04.0000, em que é Agravante: Petros Fundação Petrobras de Seguridade Social (Advogado: Dr. Carlos Roberto Siqueira Castro (671A/AM). Agravado: Jean Savio Trindade Pereira (Advogada Dra. Rylene Álvares Bastos Rodrigues (10145/ AM). Fica o Agravado intimado, na pessoa de sua advogada para, querendo, apresentar Contrarrazões ao presente recurso, bem como o Agravante para conhecimento da Decisão  de ﬂ s. 194/195 , cujo teor ﬁ nal é o seguinte: “Posto isso, indeﬁ ro o pedido de efeito suspensivo. Intime-se o agravado para responder no prazo de 15 (quinze) dias, facultando-lhe juntar a documentação que entender necessária ao julgamento do recurso. A Secretaria para providências. Manaus, 25 de fevereiro de 2019.  Des. Elci Simões de Oliveira - Relator. Os autos acima citados encontram-se à disposição dos interessados Eletronicamente. Manaus, 7 de março de 2019 (as) Dra. Pollyana de Souza Bastos - Secretária. RPCR"
	# public ="r. Carlos Roberto Siqueira Castro (671A/AM). Agravado: Jean Savio Trindade Pereira (Advogada Dra. Rylene Álvares Bastos Rodrigues (10145/ AM)"
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

# sep_representante()


#####################################################################################


def classificacao_todas():

	lista_planilhas_a_ler = glob.glob("./planilhas_unificadas/*.xlsx")

	dados_planilhas_lidas = []

	todos_dados = pd.DataFrame()

	for planilha in lista_planilhas_a_ler:
	#	print("Nome da planilha a ler: ", planilha)
		dados_planilhas_lidas.append(pd.read_excel(planilha, dtype="object", engine ='openpyxl'))
	#	print("Lida!")

	todos_dados = todos_dados.append(dados_planilhas_lidas, ignore_index=True, sort=False)

	planilha = todos_dados

	# planilha = pd.read_excel("teste_oab.xlsx", engine ='openpyxl')

	termos = pd.read_excel("Termos_limpos_dicionario.xlsx", engine ='openpyxl')
	
	# print("a planinha tem",len(planilha["publicacoes"]),"\n")

	comarcas = []
	tipos_proces =[]
	oabs =[]
	total = 0

	for public,num,est in tqdm(zip(planilha["publicacoes"],planilha["Número do Processo"],planilha["Estado"])):
		
		
		###### parte de verificar os tipos processuais 
		try:	
			publis = public.replace("\n","") # eliminar as quebras de linhas para pontecializar o regex
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

			tipo = "" # tipo recebe valor em branco

			# itera sobre o dicionário de tipos processuais
			for n in range(len(termos["Termos Processuais"])):
				rgx = termos ["Termos Processuais"][n]
				rgx = rgx.replace("\n","") #elimina eventuais quebras de linhas no regex tbem
				
				# tenta encontrar o tipo na publicação
				try:
					if re.search(rgx, publis, re.IGNORECASE): 
						tipo = re.search(rgx, publis, re.IGNORECASE).group()
						tipo = tipo.lower() # se encontrar normaliza para minúscula e grava na variável
						# print(tipo)
						break
				except:
					pass		

			# junta o a variável tipo na lista		
			tipos_proces.append(tipo)
			if tipo =="": # contabiliza as que não encontrou
				total = total+1

		# em caso de erro também insere o vazio 
		except:
			tipo = ""
			tipos_proces.append(tipo)
			total = total+1	


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

	## parte de separar a data da decisão - FALHOU!!
		# public_pt_final = publis[-350:]
		# try:
		# data_decisao = Encontrar_data_decisao(public_pt_final)
		# except:
		# 	print("não tem")	
		# z= input("")

	####### parte de buscar os advogados
		try:
			oab = sep_representante(public)
		except:
			oab = []
			# print(public)
			# z=input("")
		oabs.append(oab) 	



	# insere as novas variáveis


	# print("Temos",total, "não classificados.\n O total é",len(planilha["publicacoes"]),
	# 	"\n o percentual é",(total*100)/len(planilha["publicacoes"]))


	planilha ["Tipos processuais"] = tipos_proces
	planilha["Comarcas"] = comarcas
	planilha["OABS"] = oabs	
	
	planilha.to_excel("todos_classificados.xlsx", index = False)



# classificacao_todas()



### para usar nos demais códigos dos Estados - importar essa função

def classificacao_quali(planilha):

	termos = pd.read_excel("Termos_limpos_dicionario.xlsx", engine ='openpyxl')
	
	# print("a planinha tem",len(planilha["publicacoes"]),"\n")

	comarcas = []
	tipos_proces =[]
	oabs =[]
	total = 0
	for public,num,est in tqdm(zip(planilha["publicacoes"],planilha["Número do Processo"],planilha["Estado"])):
		
		
		###### parte de verificar os tipos processuais 
		try:	
			publis = public.replace("\n","") # eliminar as quebras de linhas para pontecializar o regex
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

			tipo = "" # tipo recebe valor em branco

			# itera sobre o dicionário de tipos processuais
			for n in range(len(termos["Termos Processuais"])):
				rgx = termos ["Termos Processuais"][n]
				rgx = rgx.replace("\n","") #elimina eventuais quebras de linhas no regex tbem
				
				# tenta encontrar o tipo na publicação
				try:
					if re.search(rgx, publis, re.IGNORECASE): 
						tipo = re.search(rgx, publis, re.IGNORECASE).group()
						tipo = tipo.lower() # se encontrar normaliza para minúscula e grava na variável
						# print(tipo)
						break
				except:
					pass		

			# junta o a variável tipo na lista		
			tipos_proces.append(tipo)
			if tipo =="": # contabiliza as que não encontrou
				total = total+1

		# em caso de erro também insere o vazio 
		except:
			tipo = ""
			tipos_proces.append(tipo)
			total = total+1	


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

	## parte de separar a data da decisão - FALHOU!!
		# public_pt_final = publis[-350:]
		# try:
		# data_decisao = Encontrar_data_decisao(public_pt_final)
		# except:
		# 	print("não tem")	
		# z= input("")

	####### parte de buscar os advogados

		oab = sep_representante(public)
		oabs.append(oab) 	



	# insere as novas variáveis


	# print("Temos",total, "não classificados.\n O total é",len(planilha["publicacoes"]),
	# 	"\n o percentual é",(total*100)/len(planilha["publicacoes"]))


	planilha ["Tipos processuais"] = tipos_proces
	planilha["Comarcas"] = comarcas
	planilha["Representantes"] = oabs	
	
	# planilha.to_excel("todos_classificados.xlsx", index = False)
	return planilha