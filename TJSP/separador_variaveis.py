import re,os
import pandas as pd
import jellyfish
from tqdm import tqdm


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


separar_tipos_acao()